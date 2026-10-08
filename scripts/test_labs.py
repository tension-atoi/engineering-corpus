"""Scenario oracles, including expected failures, without network."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
cases = [(['examples/change_lab.py', '--broken'], 1, 'expected one r1 action'),
         (['examples/change_lab.py'], 0, '"denied_action_count": 0'),
         (['examples/api_lab.py', '--symbol', 'Queue.morph_to'], 1, 'unknown symbol'),
         (['examples/api_lab.py'], 0, 'Queue.enqueue')]
records = []
for args, expected, text in cases:
    r = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
    output = r.stdout+r.stderr
    records.append({'command': args, 'exit_code': r.returncode, 'expected_exit': expected, 'output': output})
    assert r.returncode == expected and text in output, records[-1]
path = ROOT/'evidence/runs/labs'
path.mkdir(parents=True, exist_ok=True)
(path/'run.json').write_text(json.dumps(records, indent=2)+'\n')
logs = ROOT/'evidence/logs'; logs.mkdir(parents=True, exist_ok=True)
(logs/'labs.log').write_text('\n'.join(x['output'] for x in records))
print('LABS_OK positive=2 expected_negative=2')
