# DOCS-HUB-01D — Guides vérifiables et registre de versions

**Base inspectée :** dépôt public tension-atoi/engineering-corpus, SHA 9edf055d14716ef9f42c2bed80b01848d7318673. Seules les sources déjà publiques sont reprises. Cette tranche ne revendique aucune publication HTTP tant qu'un déploiement et une observation séparés ne sont pas prouvés.

## Sources

- Guide api-verification : deux textes FR/EN, état DRAFT, limites explicites ; aucune API Gnosix prétendument opérationnelle.
- Atelier pédagogique réellement existant : docs/fr/labs/02-api.md et docs/en/labs/02-api.md ; scripts examples/api_lab.py et scripts/test_labs.py. Les quatre chemins sont épinglés au commit ci-dessus, avec SHA-256 par fichier dans docs/guide-registry.json.
- Les exemples emploient une interface Python **fictive** Queue. Le RED attendu (Queue.morph_to, code 1) et GREEN attendu (Queue.enqueue, code 0) ne qualifient ni Rust, ni service HTTP, ni accès distant.
- Aucun tag dans git ls-remote --tags origin au 2026-10-08. docs/release-registry.json annonce **zéro** release et limite sa portée au dépôt engineering-corpus. Il ne prononce rien sur les autres projets.

## Surface produite

- Index : /fr/guides.html et /en/guides.html.
- Détail bilingue : /fr/guides/api-verification.html et /en/guides/api-verification.html.
- Registre vide de releases : /fr/releases.html et /en/releases.html.
- JSON : /registry/guide-catalog.json et /registry/release-catalog.json.
- Aucune migration des chemins existants, de la clé navigateur de progression, ni des pages SDK/API.
- Les liens de provenance sont des URLs HTTPS GitHub épinglées ; génération et navigateur restent sans requête distante.

## Qualification

Le builder consomme des sources JSON et Markdown versionnées. scripts/test_hub.py vérifie langues, routes, SHA Git, empreintes, états et absence de releases fictives. scripts/validate.py vérifie les liens et ressources, CSP et balises H1. Le test Hub participe désormais à la qualification en checkout propre.

**Limites ouvertes :** aucun SDK distribuable ; aucun guide d'intégration réelle au runtime Gnosix ; aucun tag de release ; aucune qualification humaine de l'expérience. L'entrée d'un produit supplémentaire requiert une décision de publicité et une provenance indépendante.
