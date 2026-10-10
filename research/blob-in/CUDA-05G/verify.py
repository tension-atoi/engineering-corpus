#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independently validate raw CUDA-05G Linux credential observations.

Never imports acquire.py or the Perl server. Raw data remains local/private.
Writes a fixed, de-identified public projection; no inferred GPU claims.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parent
PROTOCOL = '396c36e7aef2271544bb98d025129c6de1a73547'

def digest(data):
    return sha256(data).hexdigest()

def ensure(value, label):
    if not value: raise ValueError('EVIDENCE_GATE_FAIL: '+label)

def qualify(raw):
    ensure(raw['schema']=='gnu6.blobin.replication.raw.v1', 'schema')
    ensure(raw['experiment_id']=='CUDA-05G-P01', 'experiment id')
    ensure(raw['protocol_commit']==PROTOCOL, 'preregistration commitment')
    ensure(raw['contract_sha256']==digest((BASE/'CONTRACT.json').read_bytes()), 'contract digest')
    ensure(raw['image']=='postgres:16', 'instrument image does not match recorded amendment')
    ensure(re.fullmatch(r'sha256:[0-9a-f]{64}',raw['image_digest']) is not None, 'image digest malformed')
    ids=raw['identities'];caller=ids['host_caller'];service=ids['service'];group=ids['host_gid']
    ensure(caller>0 and caller not in (service,ids['unauthorized'],ids['dac_outsider']), 'host identity overlap')
    ensure(service==65534 and ids['unauthorized']==65533 and ids['dac_outsider']==65532,
           'fixture identity assignment')
    obs=raw['observations'];steps=raw['commands']
    ensure(steps['setup']['code']==steps['server_start']['code']==0, 'setup/launch')
    config=steps['inspect']['stdout'].strip().split('|')
    ensure(len(config)==4 and config[:3]==[f'{service}:{group}','', 'none']
           and steps['inspect']['code']==0, 'container identity, user namespace and network')
    ensure(obs['host_uid_quad']==[service]*4, 'actual host UID quartet')
    ensure(obs['dir']=={'uid':service,'gid':group,'mode':'0o710'},'directory DAC')
    ensure(obs['socket']=={'uid':service,'gid':group,'mode':'0o660'},'socket DAC')
    for stage in ('allowed_before','allowed_after'):
        ensure(obs[stage]=={'code':0,'response':'ALLOWED'},stage+' response')
    denied=obs['connected_unauthorized']
    ensure(denied['code']==0 and denied['stdout'].strip()=='DENIED', 'connected unauthorized denial')
    outsider=obs['dac_outsider']
    ensure(outsider['code']!=0 and 'CONNECT_FAILED Permission denied' in outsider['stderr'],
           'DAC denial must originate at socket connect, not blocked script load')
    ensure(steps['server_running_after_wait']['code']==0 and
           steps['server_running_after_wait']['stdout'].strip()=='false','service still running')
    ensure(steps['service_exit']['code']==0 and steps['service_exit']['stdout'].strip()=='0',
           'service exit')
    ensure(steps['server_logs']['code']==0 and not steps['server_logs']['stderr'], 'server logs')
    lines=steps['server_logs']['stdout'].splitlines()
    ensure(len(lines)==5 and lines[0]=='READY mode=0660 limit=3' and
           lines[-1]=='EXIT clean=PASS count=3','finite three-accept server log')
    for index,(uid,decision) in enumerate(((caller,'ALLOWED'),(ids['unauthorized'],'DENIED'),
                                           (caller,'ALLOWED'))):
        match=re.fullmatch(r'PEER index=(\d+) uid=(\d+) gid=(\d+) decision=(ALLOWED|DENIED)',lines[index+1])
        ensure(match is not None and (int(match[1]),int(match[2]),int(match[3]),match[4])==
               (index,uid,group,decision), f'server-observed SO_PEERCRED index {index}')
    for key in ('container','ownership'):
        ensure(raw['cleanup'][key]['code']==0,'cleanup '+key)
    return {key:'PASS' for key in (
        'actual_host_uid','socket_dac','permitted_before','connected_denied_uid',
        'dac_denied_before_accept','permitted_after','service_cleanup',
        'reproduction_is_gpu_independent')}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--raw',type=Path,required=True,help='Private raw.json outside public source')
    parser.add_argument('--public',type=Path,help='Write only allowlisted public result JSON')
    args=parser.parse_args()
    raw_bytes=args.raw.read_bytes()
    raw=json.loads(raw_bytes)
    states=qualify(raw)
    contract=json.loads((BASE/'CONTRACT.json').read_text())
    ensure(set(states)==set(contract['required_gates']), 'missing contract gates')
    ensure(set(states.values()).issubset(set(contract['valid_states'])), 'invalid gate value')
    # Deliberately distort independent source-of-truth fields. Both must be refused.
    forged=json.loads(raw_bytes)
    forged['observations']['host_uid_quad']=[raw['identities']['host_caller']]*4
    try: qualify(forged)
    except ValueError: pass
    else: raise RuntimeError('FALSIFIER_FAILED forged host UID')
    forged=json.loads(raw_bytes)
    forged['commands']['server_logs']['stdout']=forged['commands']['server_logs']['stdout'].replace(
        f"uid={raw['identities']['unauthorized']} gid=",f"uid={raw['identities']['host_caller']} gid=")
    try: qualify(forged)
    except ValueError: pass
    else: raise RuntimeError('FALSIFIER_FAILED forged peer UID')
    payload={
        'schema':'gnu6.blobin.replication.public.v1',
        'experiment_id':raw['experiment_id'],
        'protocol_commit':PROTOCOL,
        'contract_sha256':raw['contract_sha256'],
        'raw_sha256':digest(raw_bytes),
        'observed_utc':raw['observed_utc'],
        'instrument_image_digest':raw['image_digest'],
        'method':'Independent Perl service/clients + Python acquisition, rootful disposable Docker, network disabled',
        'gate_results':states,
        'attempts':4, 'socket_accepts':3,
        'negative_trial_history':['Initial image unavailable: BLOCKED before measurement',
                                  'First actual socket trial: invalid host pathname and DAC script witness'],
        'cuda05f_gpu_parity':'NOT_RUN',
        'cuda05f_runtime_replication':'BLOCKED_PRIVATE_RUNTIME_SOURCE',
        'production_authorization':'DENIED',
        'review_status':'draft_pending_external_replication',
        'limitations':['Only one completed independent fixture trial; no statistical confidence estimate',
                       'The rootful Docker daemon remains privileged and out of scope',
                       'This independently tests Linux IPC identity, not the real Rust supervisor',
                       'Original CUDA-05F Rust runtime and raw observations are private',
                       'No GPU kernel, Vulkan/CUDA rendering, physical device loss or native provider loading was tested',
                       'Private raw data remains outside Git; its checksum is not an externally auditable dataset',
                       'Host and container environments can differ; external replication is pending']}
    ensure(payload['production_authorization']==contract['production_authorization'], 'authority')
    if args.public:
        args.public.parent.mkdir(parents=True,exist_ok=True)
        args.public.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    print('CUDA05G_INDEPENDENT_VALIDATION_PASS gates=8/8 controls=4 server_accepts=3 falsifiers=2 rejected gpu=NOT_RUN release=DENIED')

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,OSError,RuntimeError) as error:sys.exit('CUDA05G_VALIDATION_FAIL '+str(error))
