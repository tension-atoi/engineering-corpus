"""Rebuild an exact clean Git HEAD with an isolated, offline pinned builder."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def hashes(directory):
    return {str(p.relative_to(directory)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob('*')) if p.is_file()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--wheels',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve(); output.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    if dirty: raise SystemExit('Refusing tracked dirty source; commit before qualification')
    record={'source_commit':head,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'environment':{'python':sys.version,'platform':platform.platform()},'steps':[],
            'limits':['Same-host reproducibility only','CPython 3.14 Linux x86_64 wheel lock',
                      'Browser and editorial gates recorded separately','No deployment or WCAG certification']}
    def run(command,cwd):
        env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONNOUSERSITE']='1'
        p=subprocess.run([str(x) for x in command],cwd=cwd,env=env,capture_output=True,text=True)
        record['steps'].append({'command':[str(x) for x in command],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        (output/'run.json').write_text(json.dumps(record,indent=2)+'\n')
        (output/'raw.log').write_text('\n'.join(json.dumps(x) for x in record['steps'])+'\n')
        if p.returncode: raise SystemExit(f'Qualification failed: {command}\n{p.stdout}{p.stderr}')
        return p.stdout
    with tempfile.TemporaryDirectory(prefix='corpus-clean-') as temporary:
        checkout=Path(temporary)/'checkout'
        run(['git','clone','--no-hardlinks','--no-checkout',ROOT,checkout],ROOT)
        run(['git','checkout','--detach',head],checkout)
        assert run(['git','status','--porcelain'],checkout).strip()==''
        before=hashes(checkout/'dist')
        run([sys.executable,'-m','venv',checkout/'.venv'],checkout)
        python=checkout/'.venv/bin/python'
        run([python,'-m','pip','install','--no-index','--find-links',args.wheels.resolve(),
             '--require-hashes','-r','requirements.lock'],checkout)
        run([python,'-m','pip','freeze','--all'],checkout)
        run([python,'scripts/check.py'],checkout)
        run([python,'scripts/build.py'],checkout)
        first=hashes(checkout/'dist')
        if first!=before: raise SystemExit('Generated artifact differs from committed dist')
        run([python,'scripts/build.py'],checkout)
        second=hashes(checkout/'dist')
        if second!=first: raise SystemExit('Second build drift')
        run([python,'scripts/check.py'],checkout)
        run([python,'scripts/test_hub.py'],checkout)
        run([python,'scripts/test_checks.py'],checkout)
        run([python,'scripts/test_labs.py'],checkout)
        run([python,'examples/workspace_lab.py','--output',Path(temporary)/'workspace-evidence'],checkout)
        workspace=json.loads((Path(temporary)/'workspace-evidence/workspace-run.json').read_text())
        # Raw sandbox traces are retained, but the temporary fictional repositories are not packaged.
        (output/'workspace-run.json').write_text(json.dumps(workspace,indent=2)+'\n')
        run(['git','diff','--exit-code','--','docs','dist','scripts','examples'],checkout)
        record.update({'result':'PASS','clean_checkout':True,'isolated_environment':True,
                       'committed_dist_matches':True,'rebuilds_identical':True,'dist_sha256':second,
                       'wheel_sha256':hashes(args.wheels.resolve())})
    (output/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'QUALIFICATION_OK source_commit={head} files={len(second)}')


if __name__=='__main__': main()
