---
id: 08-hygiene
title: "Hygiène, release & rollback"
duration: 15
status: draft
category: core
---
# Hygiène, release & rollback

> Statut : brouillon méthodologique, à adapter — non ratifié dans les projets consommateurs.

## L'hygiène est un gate continu
Ne pas masquer les problèmes dans une campagne finale. Définir des contrôles locaux rapides, un inventaire de dépendances, la traçabilité des migrations et un protocole de retour arrière.

| Fréquence | Gate | Preuve |
|---|---|---|
| chaque diff | format, lint, diff-check, secrets | sortie + statut |
| chaque tranche | tests ciblés + adjacents | environnement + commandes |
| chaque jalon | invariants, API diff, doc | rapport de qualification |
| mensuelle | licences, dépendances, sécurité | inventaire/version |
| pré-release | artefacts, signatures/sha256, rollback | gate signé |
| post-release | santé, observabilité, réversibilité | trace d'exploitation |

### Dépendances
Introduire une dépendance seulement avec justification, licence, provenance, version contrôlée, plan de suppression et évaluation d'autorité (réseau, fichiers, processus). Ne pas mettre à jour silencieusement une dépendance critique.

### Release séparée
`merge` ne signifie pas `deploy`. Une release exige son propre paquet, une preuve de provenance, la décision humaine et une stratégie de repli testée.

### Exercice
Un build vert mais non reproductible est prêt à être déployé. Quelle décision ?

<details><summary>Auto-évaluation</summary>Bloquer la promotion, figer les dépendances, comparer le résultat en environnement propre et produire un nouvel artefact vérifié. Garder l'ancien artefact pour retour arrière.</details>
