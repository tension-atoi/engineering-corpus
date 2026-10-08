# Deployment proposal (not executed)

**Target hostname (proposed only):** `doc.gnu6.live`.

1. Run `python scripts/check.py` and `python scripts/build.py` inside a clean, isolated builder.
2. Review `dist/` files for secrets, unapproved references, license notices, and potentially misleading claims.
3. Copy **only `dist/`** to a static HTTP server. Caddy, Nginx or an existing static-files deployment can serve it.
4. Add HTTPS, a content security policy and cache rules for immutable assets at deployment time.
5. Validate FR and EN routes, no unexpected network requests, mobile navigation and offline readability.
6. Record deployment commit, artifact sha256, operator approval and rollback artifact.

Do not let a docs build container inherit Docker socket, SSH keys, source-workspace credentials, or production secrets. No DNS, VPS or Coolify configuration is modified by this repository.

**Rollback:** switch the web server to the prior approved static artifact, validate the routes, and log the rollback decision. A rebuild is not a rollback because dependencies and sources may have changed.
