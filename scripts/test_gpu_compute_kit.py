#!/usr/bin/env python3
"""Source-static GPU witness cross-check; never pretends to execute GPUs in a docs build."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'research'/'blob-in'/'CUDA-05H'
PRE='b89b266829b396d5b9569e0cbb2cd38a04f603bb'

def check():
    validator=subprocess.run(['python3',str(KIT/'validate_public.py')],
                              text=True,capture_output=True,timeout=25)
    assert validator.returncode==0 and 'CUDA05H_PUBLIC_PASS' in validator.stdout,validator.stderr
    frozen=subprocess.check_output(['git','-C',str(ROOT),'show',
        PRE+':research/blob-in/CUDA-05H/PREREGISTRATION.md'])
    assert frozen==(KIT/'PREREGISTRATION.md').read_bytes()
    fixture=subprocess.check_output(['git','-C',str(ROOT),'show',
        PRE+':research/blob-in/CUDA-05H/primitives.bin'])
    assert fixture==(KIT/'primitives.bin').read_bytes()
    published=(KIT/'PUBLIC-RESULTS.json').read_bytes()
    assert (ROOT/'dist'/'evidence'/'cuda-05h-public-results.json').read_bytes()==published
    data=json.loads(published)
    assert data['schema']=='gnu6.blobin.gpu.public.v1'
    assert data['protocol_commit']==PRE
    assert data['cuda05f_gpu_parity']=='NOT_RUN'
    assert data['cuda05f_runtime_replication']=='BLOCKED_PRIVATE_RUNTIME_SOURCE'
    assert data['production_authorization']=='DENIED'
    assert data['external_replication']=='PENDING'
    assert len(data['gate_results'])==8 and set(data['gate_results'].values())=={'PASS'}
    for lang in ('fr','en'):
        page=(ROOT/'dist'/lang/'studies'/'cuda-05h.html').read_text()
        assert PRE in page and 'CUDA-05H' in page
        assert '/evidence/cuda-05h-public-results.json' in page
        assert 'github.com/tension-atoi/engineering-corpus/tree/main/research/blob-in/CUDA-05H' in page
        assert page.count('<h1')==1
        index=(ROOT/'dist'/lang/'challenges.html').read_text()
        assert f'/{lang}/studies/cuda-05h.html' in index
    for path in (ROOT/'dist'/'research',KIT/'raw.json',KIT/'cpu.bin',KIT/'cuda.bin',KIT/'vulkan.bin'):
        assert not path.exists(),path
    print('CUDA05H_SITE_CROSSCHECK_PASS pages=2 prereg=PINNED source=12 manifest=PASS gpu_claim=BOUNDED')
if __name__=='__main__':check()
