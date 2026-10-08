---
id: lab-api
title: Atelier B — API vérifiable
duration: 25
status: draft
category: lab
method_id: EC-L02
classification: recommendation
prerequisites:
- Python 3.10+
- Chapitres 01–06
artifacts:
- Logs RED/GREEN
- Conclusion bornée
success_criteria:
- Échec attendu du cas négatif ; code 0 pour le cas positif
references:
- python-unittest
---
# Atelier B — Publier une API sans hallucination

**Scénario fictif :** un agent produit une page SDK à partir d'une bibliothèque fictive.

1. Épingler le commit et extraire les exports publics (`rustdoc` et extraction d'API selon compatibilité toolchain).
2. Déclarer le statut de chaque interface : `public-stable`, `public-experimental`, `internal`.
3. Faire produire une proposition de guide à un LLM local isolé.
4. Compiler un exemple minimal depuis `examples/` et vérifier les symboles utilisés.
5. Relier toute affirmation à une preuve de type E1, E2 ou supérieure adaptée.
6. Produire FR + EN, liens réciproques et notes de version.

<details><summary>Critères de réussite</summary>Pas de symboles inventés, aucun accès cloud implicite, exemples qui compilent, classification publiée avec limites et revue humaine documentée.</details>

## Essai reproductible
Depuis la racine du dépôt, sans installation ni modèle :

```bash
python3 examples/api_lab.py --symbol Queue.morph_to
# expected exit 1
python3 examples/api_lab.py
# expected exit 0
python3 scripts/test_labs.py
```

[Télécharger le support](/examples/api_lab.py)

## Observation et exercice
Le cas négatif demande Queue.morph_to, absent de l’inventaire AST ; le cas positif utilise Queue.enqueue et vérifie son résultat. Ajoute un export fictif et son exemple, puis une signature inconnue. Le support Python réduit les prérequis ; le transfert vers Rust exige une preuve séparée avec toolchain épinglée. Le LLM est optionnel : rédige le guide à partir de l’inventaire si aucun modèle autorisé n’est disponible.

## Preuves et limites
Conserve commandes, sorties, codes de retour et HEAD. Le RED doit échouer sur le doublon ou symbole inconnu, jamais sur un environnement cassé. Ces supports n’exécutent aucune action système ni moteur graphique, et ne certifient aucune API externe.
