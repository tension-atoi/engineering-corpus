---
id: lab-change
title: "Atelier A — Modification qualifiée"
duration: 25
status: draft
category: lab
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
