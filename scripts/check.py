#!/usr/bin/env python3
"""Source/static coherence only; no general certification."""
from pathlib import Path
from validate import check
import sys
errors, summary = check(Path(__file__).resolve().parents[1])
if errors:
    for error in errors: print('FAIL', error)
    sys.exit(1)
print('CORPUS_CHECK_OK', ' '.join(f'{key}={value}' for key,value in summary.items()), 'scope=source_and_static_coherence')
