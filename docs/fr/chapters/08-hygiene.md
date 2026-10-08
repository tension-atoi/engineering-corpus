---
id: 08-hygiene
title: Hygiène, release & rollback
duration: 15
status: draft
category: core
method_id: EC-M08
classification: proposed-principle
prerequisites:
- Bases de Git
- Lire le résultat d’un test
artifacts:
- Inventaire Git ; hashes des travaux préservés ; log d’ascendance ; artefact précédent
  et candidat ; résultat du repli.
success_criteria:
- L’atelier C démontre la conservation des octets et la divergence de deux branches.
  Il ne simule pas tous les sous-modules, conflits, fichiers ignorés ou hooks d’un
  dépôt réel.
references:
- git-worktree
- git-merge-base
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


## Problème traité
Un changement de branche peut abandonner du travail non committé ; un build vert peut pointer vers un artefact différent de celui livré.

## Méthode reproductible
1. Inventorier HEAD, index, fichiers suivis/non suivis et worktrees
2. conserver les octets avant mutation
3. partir d’une baseline explicite
4. vérifier l’ascendance dans les deux sens
5. qualifier l’artefact final
6. répéter le repli sur une copie fictive.

**Responsabilités :** l’auteur propose et enregistre les résultats ; le relecteur critique l’oracle ; le propriétaire du projet décide de l’adoption.

## Exemple, contre-exemple et échec
Bon exemple : travailler dans un worktree distinct et garder les fichiers sales intacts. Contre-exemple : reset --hard pour obtenir un état « propre ». Échec : le même nom de branche est confondu avec le même commit ; comparer les identifiants exacts.

## Artefacts et qualification
Inventaire Git ; hashes des travaux préservés ; log d’ascendance ; artefact précédent et candidat ; résultat du repli.

L’atelier C démontre la conservation des octets et la divergence de deux branches. Il ne simule pas tous les sous-modules, conflits, fichiers ignorés ou hooks d’un dépôt réel.

## Exercice de transfert
Applique la méthode au service fictif Courier. Produis les artefacts ci-dessus, puis invente un cas qui invalide une conclusion trop large.

<details><summary>Critères d’auto-évaluation</summary>Le cas est fictif et reproductible ; la baseline est nommée ; la procédure et le résultat attendu sont explicites ; un échec est conservé ; la conclusion cite les artefacts et leurs limites. Si un critère manque, corrige avant de déclarer la méthode appliquée.</details>
