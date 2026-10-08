---
id: lab-api
title: "Atelier B — API vérifiable"
duration: 25
status: draft
category: lab
---
# Atelier B — Publier une API sans hallucination

**Scénario fictif :** un agent produit une page SDK à partir d'une bibliothèque Rust locale.

1. Épingler le commit et extraire les exports publics (`rustdoc` et extraction d'API selon compatibilité toolchain).
2. Déclarer le statut de chaque interface : `public-stable`, `public-experimental`, `internal`.
3. Faire produire une proposition de guide à un LLM local isolé.
4. Compiler un exemple minimal depuis `examples/` et vérifier les symboles utilisés.
5. Relier toute affirmation à une preuve de type E1, E2 ou supérieure adaptée.
6. Produire FR + EN, liens réciproques et notes de version.

<details><summary>Critères de réussite</summary>Pas de symboles inventés, aucun accès cloud implicite, exemples qui compilent, classification publiée avec limites et revue humaine documentée.</details>
