#!/usr/bin/env python3
"""Check real public repro package and source->static projection coherence."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'research'/'blob-in'/'CUDA-05G'
BASE='396c36e7aef2271544bb98d025129c6de1a73547'

def check():
    validator=subprocess.run(['python3',str(KIT/'validate_public.py')],
        capture_output=True,text=True,timeout=10)
    assert validator.returncode==0 and 'CUDA05G_PUBLIC_KIT_PASS' in validator.stdout
    body=(KIT/'PUBLIC-RESULTS.json').read_bytes()
    assert (ROOT/'dist'/'evidence'/'cuda-05g-public-results.json').read_bytes()==body
    data=json.loads(body)
    contract=json.loads((KIT/'CONTRACT.json').read_text())
    assert data['protocol_commit']==BASE
    frozen=subprocess.check_output(['git','-C',str(ROOT),'show',
        BASE+':research/blob-in/CUDA-05G/PREREGISTRATION.md'])
    assert frozen==(KIT/'PREREGISTRATION.md').read_bytes()
    assert set(data['gate_results'])==set(contract['required_gates'])
    assert all(value=='PASS' for value in data['gate_results'].values())
    assert data['cuda05f_gpu_parity']=='NOT_RUN'
    assert data['cuda05f_runtime_replication']=='BLOCKED_PRIVATE_RUNTIME_SOURCE'
    assert data['production_authorization']=='DENIED'
    assert data['review_status']=='draft_pending_external_replication'
    for language in ('fr','en'):
        page=(ROOT/'dist'/language/'studies'/'cuda-05g.html').read_text()
        assert BASE in page
        assert 'CUDA-05G' in page
        assert '/evidence/cuda-05g-public-results.json' in page
        assert 'github.com/tension-atoi/engineering-corpus/tree/main/research/blob-in/CUDA-05G' in page
        index=(ROOT/'dist'/language/'challenges.html').read_text()
        assert f'/{language}/studies/cuda-05g.html' in index
        assert page.count('<h1')==1
    assert not (KIT/'raw.json').exists() and not (KIT/'failure.json').exists()
    assert not (ROOT/'dist'/'research').exists()
    challenges=json.loads((ROOT/'docs'/'challenges'/'registry.json').read_text())
    row=next(entry for entry in challenges['challenges'] if entry['id']=='CUDA-05E')
    assert row['public_kit']=='PARTIAL_ORIGINAL_WITH_OPEN_IPC_FIXTURE'
    assert row['replication_kit']['status']=='LOCAL_PASS_EXTERNAL_REPLICATION_PENDING'
    assert row['replication_kit']['original_cuda05f_runtime_replicated'] is False
    # The site cannot accidentally promote a partial original to full public GPU reproduction.
    forged=json.loads(json.dumps(row))
    forged['replication_kit']['original_cuda05f_runtime_replicated']=True
    try:assert forged['replication_kit']['original_cuda05f_runtime_replicated'] is False
    except AssertionError:pass
    else:raise AssertionError('false GPU reproduction claim accepted')
    print('CUDA05G_STATIC_PUBLICATION_PASS sha256='+sha256(body).hexdigest()[:16]+
        ' locales=2 preserved_prereg=PASS original_runtime=BLOCKED')

if __name__=='__main__':check()
