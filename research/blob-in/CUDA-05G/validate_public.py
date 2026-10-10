#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Public-only, offline verification: no private raw trace is required."""
from hashlib import sha256
from pathlib import Path
import json
import re

HERE = Path(__file__).resolve().parent
EXPECTED = {
    'README.md','PREREGISTRATION.md','CONTRACT.json',
    'AMENDMENT-01.md','AMENDMENT-02.md',
    'server.pl','client.pl','acquire.py','verify.py','validate_public.py',
    'PUBLIC-RESULTS.json'
}

def validate_claim(public, contract):
    assert contract['schema']=='gnu6.blobin.replication.v1'
    assert public['schema']=='gnu6.blobin.replication.public.v1'
    assert contract['experiment_id']==public['experiment_id']=='CUDA-05G-P01'
    assert public['protocol_commit']=='396c36e7aef2271544bb98d025129c6de1a73547'
    assert public['contract_sha256']==sha256((HERE/'CONTRACT.json').read_bytes()).hexdigest()
    assert set(public['gate_results'])==set(contract['required_gates'])
    assert set(public['gate_results'].values())=={'PASS'}
    assert public['attempts']==4 and public['socket_accepts']==3
    assert public['cuda05f_gpu_parity']=='NOT_RUN'
    assert public['cuda05f_runtime_replication']=='BLOCKED_PRIVATE_RUNTIME_SOURCE'
    assert public['production_authorization']=='DENIED'
    assert public['review_status']=='draft_pending_external_replication'
    assert re.fullmatch('[0-9a-f]{64}',public['raw_sha256'])
    assert re.fullmatch('sha256:[0-9a-f]{64}',public['instrument_image_digest'])

def verify():
    contract=json.loads((HERE/'CONTRACT.json').read_text())
    public=json.loads((HERE/'PUBLIC-RESULTS.json').read_text())
    validate_claim(public,contract)
    forbidden=('peer_uid=', 'host_uid_quad','/mnt/workbench','/home/tension_atoi',
               'jordan.p@','"host_caller"','"host_gid"','"socket_owner"')
    assert all(word not in (HERE/'PUBLIC-RESULTS.json').read_text() for word in forbidden)
    manifest=(HERE/'SHA256SUMS.txt').read_text().splitlines()
    found=set()
    for line in manifest:
        hashed,filename=line.split('  ',1)
        assert filename in EXPECTED and filename not in found
        assert sha256((HERE/filename).read_bytes()).hexdigest()==hashed
        found.add(filename)
    assert found==EXPECTED
    assert not (HERE/'raw.json').exists()
    altered=json.loads(json.dumps(public))
    altered['production_authorization']='APPROVED'
    try:validate_claim(altered,contract)
    except AssertionError:pass
    else:raise AssertionError('production forgery accepted')
    altered=json.loads(json.dumps(public))
    altered['cuda05f_gpu_parity']='PASS'
    try:validate_claim(altered,contract)
    except AssertionError:pass
    else:raise AssertionError('GPU overclaim accepted')
    print('CUDA05G_PUBLIC_KIT_PASS manifest=11 sanitized=YES scope=IPC_ONLY GPU=NOT_RUN falsifiers=2 rejected')
if __name__=='__main__':verify()
