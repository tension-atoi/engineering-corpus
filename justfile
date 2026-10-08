# No network, installs, GitHub CI, or production mutations.
serve:
    python3 -m http.server 8080 --directory dist

build:
    python3 scripts/build.py

check:
    python3 scripts/check.py

verify:
    python3 scripts/check.py
    python3 scripts/build.py
    python3 scripts/check.py
