#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent public package and CPU-only reference audit, no GPU required."""
from hashlib import sha256
from pathlib import Path
import copy
import json
import re
import struct

HERE=Path(__file__).resolve().parent
PRE='b89b266829b396d5b9569e0cbb2cd38a04f603bb'
SCENE='77759079523ca127a4c24617b42a05a08c5a7c03ebdeb36b092b9ed91387fc86'
OUTPUT='613845b6341e4491efce3be997853467213ef6687770495b0d2515329678961b'
EXPECTED={'README.md','PREREGISTRATION.md','CONTRACT.json','primitives.bin',
          'oracle.py','cuda.cu','compute.comp','vulkan.c','run.py',
          'verify.py','validate_public.py','PUBLIC-RESULTS.json'}
def hashbytes(data):return sha256(data).hexdigest()
def verify_result(d,c):
    assert d['schema']=='gnu6.blobin.gpu.public.v1'
    assert d['experiment_id']==c['experiment_id']=='CUDA-05H-P01'
    assert d['protocol_commit']==PRE
    assert d['contract_sha256']==hashbytes((HERE/'CONTRACT.json').read_bytes())
    assert d['fixture_sha256']==SCENE
    assert d['output_sha256']=={'cpu':OUTPUT,'cuda':OUTPUT,'vulkan':OUTPUT}
    assert d['sample_count']==96*64
    assert d['sample_encoding']=='signed-int32-le'
    assert set(d['gate_results'])==set(c['required_gates'])
    assert set(d['gate_results'].values())=={'PASS'}
    assert d['external_replication']=='PENDING'
    assert d['cuda05f_gpu_parity']=='NOT_RUN'
    assert d['cuda05f_runtime_replication']=='BLOCKED_PRIVATE_RUNTIME_SOURCE'
    assert d['production_authorization']=='DENIED'
    assert d['review_status']=='draft'
    assert re.fullmatch('[0-9a-f]{64}',d['private_raw_sha256'])
    assert 'not private CSG signed-distance' in d['workload']

def main():
    public_path=HERE/'PUBLIC-RESULTS.json';public=json.loads(public_path.read_text())
    contract=json.loads((HERE/'CONTRACT.json').read_text())
    verify_result(public,contract)
    scene=(HERE/'primitives.bin').read_bytes()
    assert len(scene)==256 and hashbytes(scene)==SCENE
    prim=list(struct.iter_unpack('<iiii',scene)); assert len(prim)==16 and prim[0][3]==0
    # Third, public-only implementation of the deterministic integer oracle.
    values=[]
    for index in range(6144):
        x=index%96;y=index//96
        value=None
        for cx,cy,r,op in prim:
            q=(x-cx)**2+(y-cy)**2-r**2
            value=q if value is None else (min(value,q) if op==0 else
                                          max(value,q) if op==1 else max(value,-q))
        values.append(value)
    assert hashbytes(struct.pack('<6144i',*values))==OUTPUT
    raw=public_path.read_text()
    assert all(s not in raw for s in ('host_uid_quad','/mnt/workbench','/home/',
           'apikey_','sk-proj-', '"env_vars"', '"raw_stdout"'))
    lines=(HERE/'SHA256SUMS.txt').read_text().splitlines();seen=set()
    for line in lines:
        hashed,filename=line.split('  ',1)
        assert filename in EXPECTED and filename not in seen
        assert hashbytes((HERE/filename).read_bytes())==hashed
        seen.add(filename)
    assert seen==EXPECTED
    assert not (HERE/'raw.json').exists() and not (HERE/'cpu.bin').exists()
    forged=copy.deepcopy(public);forged['production_authorization']='APPROVED'
    try:verify_result(forged,contract)
    except AssertionError:pass
    else:raise AssertionError('forged authority accepted')
    forged=copy.deepcopy(public);forged['cuda05f_gpu_parity']='PASS'
    try:verify_result(forged,contract)
    except AssertionError:pass
    else:raise AssertionError('forged private runtime claim accepted')
    print('CUDA05H_PUBLIC_PASS 6144_cpu_values exact_reference=PASS sources=12 hashes=PASS falsifiers=2 rejected')
if __name__=='__main__':main()
