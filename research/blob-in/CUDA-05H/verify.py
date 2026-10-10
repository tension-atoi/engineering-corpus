#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent GPU numeric comparison; no import of run.py or GPU executables."""
from pathlib import Path
from hashlib import sha256
import argparse
import copy
import json
import struct
import sys

HERE=Path(__file__).resolve().parent
PRE='b89b266829b396d5b9569e0cbb2cd38a04f603bb'
SCENE='77759079523ca127a4c24617b42a05a08c5a7c03ebdeb36b092b9ed91387fc86'
KEYS=('fixture_integrity','cpu_oracle','cuda_device_hardware','vulkan_device_hardware',
      'cuda_bitwise_parity','vulkan_bitwise_parity','mutation_bitflip_rejected',
      'mutation_truncation_rejected')
def digest(data):return sha256(data).hexdigest()
def qualify(record,files):
    def gate(ok,label):
        if not ok:raise ValueError('CUDA05H_GATE_FAIL '+label)
    contract=json.loads((HERE/'CONTRACT.json').read_text())
    gate(record['schema']=='gnu6.blobin.gpu.raw.v1' and
         record['experiment_id']==contract['experiment_id']=='CUDA-05H-P01','identity')
    gate(record['protocol_commit']==PRE,'preregistered commit')
    gate(record['contract_sha256']==digest((HERE/'CONTRACT.json').read_bytes()),'contract')
    scene=(HERE/'primitives.bin').read_bytes()
    gate(len(scene)==16*16 and digest(scene)==SCENE==record['fixture_sha256'],'fixture')
    prim=list(struct.iter_unpack('<iiii',scene))
    gate(len(prim)==16 and prim[0][3]==0 and all(0<=x<96 and 0<=y<64 and
          3<=r<=19 and 0<=op<=2 for x,y,r,op in prim),'primitive bounds')
    steps=record['steps']
    gate(all(steps[key]['exit']==0 for key in
        ('compile_cuda','compile_spirv','compile_vulkan','cpu','cuda','vulkan')),'execution')
    gate('CUDA05H_HARDWARE' in steps['cuda']['stderr'] and
        'CUDA05H_DISPATCH_COMPLETED output_samples=6144' in steps['cuda']['stderr'],
        'real CUDA device and synchronization')
    gate('CUDA05H_VULKAN_HARDWARE' in steps['vulkan']['stderr'] and
        'type=2' in steps['vulkan']['stderr'] and
        'CUDA05H_VULKAN_DISPATCH_COMPLETED output_samples=6144' in steps['vulkan']['stderr'],
        'real discrete Vulkan hardware and synchronization')
    # Recompute expected bytes independently; don't trust the CPU binary itself.
    expected=[]
    for y in range(64):
        for x in range(96):
            acc=None
            for cx,cy,r,op in prim:
                value=(x-cx)*(x-cx)+(y-cy)*(y-cy)-r*r
                acc=value if acc is None else (min(acc,value) if op==0 else
                    max(acc,value) if op==1 else max(acc,-value))
            expected.append(acc)
    oracle=struct.pack('<6144i',*expected)
    gate(len(oracle)==24576 and files['cpu']==oracle,'CPU independently recomputed')
    for name in ('cpu','cuda','vulkan'):
        blob=files[name]
        gate(len(blob)==24576,'output bytes '+name)
        gate(record['outputs'][name]['size']==24576 and
            record['outputs'][name]['sha256']==digest(blob),'output source hash '+name)
    gate(files['cuda']==oracle,'cuda complete byte parity')
    gate(files['vulkan']==oracle,'vulkan complete byte parity')
    return {k:'PASS' for k in KEYS}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--raw',type=Path,required=True)
    ap.add_argument('--public',type=Path)
    args=ap.parse_args()
    record=json.loads(args.raw.read_text())
    files={k:(args.raw.parent/(k+'.bin')).read_bytes() for k in ('cpu','cuda','vulkan')}
    states=qualify(record,files)
    mutation=copy.deepcopy(files)
    corruption=bytearray(mutation['cuda']);corruption[172]^=0x1
    mutation['cuda']=bytes(corruption)
    try:qualify(record,mutation)
    except ValueError:pass
    else:raise RuntimeError('CUDA_MUTATION_UNDETECTED')
    mutation=dict(files);mutation['vulkan']=mutation['vulkan'][:-4]
    try:qualify(record,mutation)
    except ValueError:pass
    else:raise RuntimeError('VULKAN_TRUNCATION_UNDETECTED')
    contract=json.loads((HERE/'CONTRACT.json').read_text())
    if set(states)!=set(contract['required_gates']):raise RuntimeError('GATE_INVENTORY_MISMATCH')
    public={
        'schema':'gnu6.blobin.gpu.public.v1',
        'experiment_id':'CUDA-05H-P01','protocol_commit':PRE,
        'contract_sha256':digest((HERE/'CONTRACT.json').read_bytes()),
        'fixture_sha256':SCENE,'source_manifest_version':'CUDA05H.V1',
        'private_raw_sha256':digest(args.raw.read_bytes()),
        'output_sha256':{name:digest(files[name]) for name in ('cpu','cuda','vulkan')},
        'sample_count':6144,'sample_encoding':'signed-int32-le',
        'gate_results':states,
        'device_observed':'NVIDIA GeForce RTX 3070 CUDA and Vulkan native compute',
        'run_utc':record['utc'],'external_replication':'PENDING',
        'cuda05f_gpu_parity':'NOT_RUN',
        'cuda05f_runtime_replication':'BLOCKED_PRIVATE_RUNTIME_SOURCE',
        'production_authorization':'DENIED','review_status':'draft',
        'workload':'integer quadratic-distance CSG proxy, not private CSG signed-distance engine',
        'limitations':[
         'One qualified run on one local RTX 3070; no independent external reproductions',
         'Integer proxy intentionally excludes floating-point SDF, CUDA-05F supervisor and provider',
         'Actual real GPU execution and CPU-byte parity only; device loss and worker fault isolation NOT_TESTED',
         'Compiler/driver versions and raw outputs are retained privately; public digest is not public access',
         'Vulkan device selection requires discrete/integrated GPU; no proof of cross-vendor portability',
         'No benchmark or performance advantage is claimed',
         'Private CUDA-02/03/05F runtime code is not copied or relicensed']}
    if args.public:
        if args.public.resolve().parent!=HERE:raise RuntimeError('PUBLIC_REPORT_MUST_BE_IN_KIT')
        args.public.write_text(json.dumps(public,sort_keys=True,indent=2)+'\n')
    print('CUDA05H_INDEPENDENT_PASS gates=8/8 samples=6144 bitwise=CPU_CUDA_VULKAN mutations=2 REJECTED')
if __name__=='__main__':
    try:main()
    except (OSError,KeyError,ValueError,RuntimeError) as e:sys.exit('CUDA05H_VERIFY_FAIL '+str(e))
