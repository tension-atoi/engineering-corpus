---
id: lab-change
title: Atelier A — Modification qualifiée
duration: 25
status: draft
category: lab
method_id: EC-L01
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
# Atelier A — Qualifier une modification

**Scénario fictif :** un composant d'interface doit changer d'ancrage pendant une transition, sans perdre son état ni exécuter une action privilégiée.

| Étape | Production attendue |
|---|---|
| 1. Mandat | Délimiter paths, HEAD, interdictions |
| 2. Contrat | Définir cible, interruption, cycle de vie et autorité |
| 3. Oracle | Faire échouer un test sur interruption/reprise |
| 4. Implémentation | Réaliser une tranche minimale dans un worktree |
| 5. Vérification | Tests unitaires, intégration, captures, diff |
| 6. Publication | Séparer preuve comportementale et marketing |

### Piège à détecter
Une animation visuellement convaincante peut masquer une exécution d'action déclenchée deux fois. L'oracle doit isoler cette causalité.

<details><summary>Critères de réussite</summary>Aucun changement de production ; un contrat d'interruption explicite ; un test qui prouve l'unicité des actions ; un jeu de preuves horodatées ; un rollback démontrable.</details>

## Essai reproductible
Depuis la racine du dépôt, sans installation ni modèle :

```bash
python3 examples/change_lab.py --broken
# expected exit 1
python3 examples/change_lab.py
# expected exit 0
python3 scripts/test_labs.py
```

[Télécharger le support](/examples/change_lab.py)

## Observation et exercice
Le cas fautif répète r1 après interruption ; le cas corrigé déduplique r1 et refuse r2. Change les cibles et ajoute une identité indépendante : prédis la liste d’actions avant d’exécuter.

## Preuves et limites
Conserve commandes, sorties, codes de retour et HEAD. Le RED doit échouer sur le doublon ou symbole inconnu, jamais sur un environnement cassé. Ces supports n’exécutent aucune action système ni moteur graphique, et ne certifient aucune API externe.
