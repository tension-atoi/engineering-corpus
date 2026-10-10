#!/usr/bin/env python3
"""Source/static coherence only; no general certification."""
from pathlib import Path
from validate import check
from test_study_evidence import main as verify_study
from test_experiment_registry import main as verify_experiments
from test_challenges import main as verify_challenges
import sys
errors, summary = check(Path(__file__).resolve().parents[1])
if errors:
    for error in errors: print('FAIL', error)
    sys.exit(1)
verify_study()
verify_experiments()
verify_challenges()
print('CORPUS_CHECK_OK', ' '.join(f'{key}={value}' for key,value in summary.items()), 'scope=source_static_and_experiment_provenance')
