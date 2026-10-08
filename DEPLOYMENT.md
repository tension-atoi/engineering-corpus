# Static publication

The canonical publication host is `docs.gnu6.live`. The repository keeps the
prebuilt site in `dist/`; the static host must serve those committed files without
running a documentation build on the server.

## Coolify Static

Select the repository, the reviewed source commit, build pack **Static**, Base
Directory `/dist`, and internal port `80`. Disable automatic deployment until the
release process pins and verifies a commit. Leave host-published ports, volumes,
environment variables, and Docker socket mounts empty. Configure the public domain
and HTTPS in Coolify's application settings.

[`deployment/nginx.conf`](deployment/nginx.conf) is a reviewed configuration
template. Coolify does not load it automatically by finding this repository path.
For it to take effect, open the Static application's Nginx configuration editor in
Coolify, generate the default configuration, copy the template into that editor,
save it, and build/redeploy the application. Coolify copies the saved configuration
into the static image during an image build; restarting an existing image does not
apply the change. Check the generated config's root and server-block format in the
target Coolify version before replacing its default.

This project uses a regular-file site, not an SPA. Keep unknown paths at HTTP 404 and
serve the bilingual `404.html` as its error body. Do not add an `/index.html` fallback.
The template disables access logs and only permits same-origin runtime resources.

## Release checks

Before deployment, qualify a clean source commit, verify that its committed `dist/`
matches the artifact manifest, and pin that exact commit in the deployment source.
After deployment, check HTTPS certificate and redirect, French and English routes,
stylesheet, script, font and SVG responses, exact 404 status, health state, response
headers, artifact hashes, and unaffected domains. Coolify's configured HTTP health
check requires `curl` or `wget` inside the final image; verify the binary and test the
same request from inside the container. The check's expected-status UI fields are not
a substitute for explicit HTTP assertions.

For a first release with no prior image, recovery means disabling the new domain route
or stopping the new resource and confirming the prior edge response. A content restore
requires a separately retained, approved static artifact and manifest; never assume a
previous image is available.

No deployment or DNS change is authorized by this repository's local checks.

Coolify references: [Static applications](https://coolify.io/docs/applications/builds/static),
[health checks](https://coolify.io/docs/applications/configuration/health-checks),
[general application settings](https://coolify.io/docs/applications/configuration/general).
