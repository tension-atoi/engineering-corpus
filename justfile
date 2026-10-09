# No network, installs, GitHub CI, or production mutations.
serve:
    python3 scripts/serve.py --port 8080

build:
    python3 scripts/build.py

check:
    python3 scripts/check.py

verify:
    python3 scripts/check.py
    python3 scripts/build.py
    python3 scripts/check.py
    python3 scripts/test_hub.py
    python3 scripts/test_checks.py
    python3 scripts/test_labs.py

check-negative:
    python3 scripts/test_checks.py

labs:
    python3 scripts/test_labs.py
