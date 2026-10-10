"""Reject deployment of the unratified full-screen radial bridge."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
LOCK=json.loads((ROOT/'site/motion/no-veil.lock.json').read_text())
def main():
    assert LOCK['version']=='1.1.2'
    for name,digest in LOCK['files'].items():
        for folder in ('site','dist'):
            data=(ROOT/folder/'motion'/name).read_bytes()
            assert hashlib.sha256(data).hexdigest()==digest,(folder,name)
            assert b'data-g6-bridge' not in data,(folder,name)
            assert b'bridge.cover' not in data,(folder,name)
            assert b'bridge.reveal' not in data,(folder,name)
    for path in list((ROOT/'dist').glob('fr/**/*.html'))+list((ROOT/'dist').glob('en/**/*.html')):
        content=path.read_text()
        assert "script-src " + chr(39) + "self" + chr(39) in content, path
    print('GNU6_NO_VEIL_STATIC_PASS',len(LOCK['files']),'assets')
if __name__=='__main__': main()
