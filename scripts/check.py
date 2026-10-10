#!/usr/bin/env python3
"""Source/static coherence only; no general certification."""
from pathlib import Path
from validate import check
from test_study_evidence import main as verify_study
from test_experiment_registry import main as verify_experiments
from test_challenges import main as verify_challenges
from test_replication_kit import check as verify_cuda05g
from test_gpu_compute_kit import check as verify_cuda05h
from test_gnu6_design import main as verify_design
from test_spine import main as verify_spine
from test_context import main as verify_context
from test_shell_export import main as verify_shell_export
import sys
errors, summary = check(Path(__file__).resolve().parents[1])
if errors:
    for error in errors: print('FAIL', error)
    sys.exit(1)
verify_study()
verify_experiments()
verify_challenges()
verify_cuda05g()
verify_cuda05h()
verify_design()
verify_spine()
verify_context()
verify_shell_export()
print('CORPUS_CHECK_OK', ' '.join(f'{key}={value}' for key,value in summary.items()), 'scope=source_static_and_experiment_provenance')
