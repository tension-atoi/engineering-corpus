---
id: lab-workspace
title: Atelier C — Workspace Hygiene & Git Topology
duration: 40
status: draft
category: lab
method_id: EC-L03
classification: recommendation
prerequisites:
- Git 2.30+
- Python 3.10+
- Chapitre 08
artifacts:
- Inventaire Git
- Hashes des octets préservés et index
- Ascendance dans les deux sens
success_criteria:
- Fichiers sales et index inchangés ; divergence prouvée dans les deux sens
references:
- git-worktree
- git-merge-base
---
# Atelier C — Workspace Hygiene & Git Topology

## Problème et invariants
Courier possède une modification indexée, une modification non indexée et une note non suivie. Tu dois créer une tranche depuis une baseline explicite sans déplacer, effacer ou committer ces travaux. Les worktrees partagent objets et refs : ce ne sont pas des frontières de sécurité.

## Exécuter sur dépôts fictifs seulement
Depuis la racine, utilise un répertoire de preuves vide choisi pour l’atelier :

```bash
python3 examples/workspace_lab.py --output evidence/runs/workspace-trial
```

[Télécharger le support](/examples/workspace_lab.py). Le script crée un nouveau dépôt temporaire sous ce répertoire ; il n’accepte aucun dépôt existant comme cible et conserve les worktrees pour inspection. Il neutralise les configurations Git globales et les hooks. Aucun réseau ni accès à un dépôt privé.

## Méthode opérationnelle
1. Lire `git status --porcelain`, `git rev-parse HEAD` et `git worktree list --porcelain` dans le dépôt fictif indiqué par le manifeste.
2. Comparer les hashes de tracked.txt et notes.txt et le contenu `git show :tracked.txt` ; la sauvegarde des octets n’est pas une sauvegarde de l’index.
3. Lire les deux commits indépendants créés depuis la baseline. Aucun travail sale n’est transféré vers les worktrees.
4. Examiner `git merge-base --is-ancestor baseline slice` : code 0. Examiner slice → other et other → slice : code 1 dans les deux sens ; un autre code est une erreur, pas une divergence.
5. Vérifier `git rev-list --left-right --count slice...other` : 1 et 1. Le merge-base commun doit égaler la baseline.
6. Comparer fichiers, index, statut et HEAD avant/après. Conserver le dépôt pour contestation ; aucune suppression forcée.

## Exercice et contre-exemple
Prédis l’ascendance si une branche part du commit slice au lieu de la baseline, puis adapte une copie du support. Les deux branches existent ne signifie pas qu’elles divergent. Un reset --hard ou clean -fd peut détruire des travaux ; il n’est jamais un outil de prévol dans cet atelier.

<details><summary>Auto-évaluation</summary>Le manifeste contient trois commits exacts, l’index et les hashes préservés, les quatre contrôles d’ascendance, la divergence 1/1 et les logs bruts. Pour la variante descendante, slice est ancêtre de la nouvelle branche (0), le sens inverse retourne 1. Distingue échec attendu et erreur Git.</details>

## Qualification et limites
Un PASS prouve le scénario fictif, pas tous les conflits, sous-modules, fichiers ignorés, filtres Git ni récupérations après panne. Le support conserve les données ; il ne démontre pas la restauration d’un dépôt réel. Pour retirer un worktree d’exercice, vérifier qu’il est propre puis utiliser git worktree remove sans --force ; conserver les notes et logs utiles.
