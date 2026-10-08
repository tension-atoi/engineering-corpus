"""Negative controls prove the checker rejects specific malformed inputs."""
import json
from pathlib import Path
import shutil
import tempfile
from validate import check

ROOT=Path(__file__).resolve().parents[1]
fixtures=[('relative-link','dist/fr/index.html','</body>','<a href="missing.html">bad</a></body>','broken link'),
          ('fragment','dist/fr/index.html','</body>','<a href="index.html#missing">bad</a></body>','broken fragment'),
          ('status','docs/fr/chapters/01-mandate.md','status: draft','status: bogus','invalid status'),
          ('resource','dist/fr/index.html','</body>','<script src="https://example.invalid/x.js"></script></body>','external resource'),
          ('metadata','docs/fr/chapters/01-mandate.md','method_id: EC-M01','wrong_key: EC-M01','missing method_id'),
          ('css-resource','dist/style.css',':root{',':root{background:url(https://example.invalid/x);','external CSS resource')]
records=[]
for name,file,old,new,reason in fixtures:
    with tempfile.TemporaryDirectory(prefix='corpus-negative-') as directory:
        root=Path(directory)
        for folder in ('docs','dist','assets'): shutil.copytree(ROOT/folder,root/folder)
        path=root/file;text=path.read_text();assert old in text;path.write_text(text.replace(old,new))
        errors,_=check(root)
        assert any(reason in e for e in errors), (name,errors)
        records.append({'fixture':name,'expected_reason':reason,'errors':errors,'result':'PASS'})
out=ROOT/'evidence/runs/checker';out.mkdir(parents=True,exist_ok=True)
(out/'run.json').write_text(json.dumps(records,indent=2)+'\n')
logs=ROOT/'evidence/logs';logs.mkdir(exist_ok=True)
(logs/'checker.log').write_text(json.dumps(records,indent=2)+'\n')
print(f'CHECKER_NEGATIVE_OK fixtures={len(records)}')
