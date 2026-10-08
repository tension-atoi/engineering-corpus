---
id: 01-mandate
title: Mandat & découpage
duration: 12
status: draft
category: core
method_id: EC-M01
classification: proposed-principle
prerequisites:
- Bases de Git
- Lire le résultat d’un test
artifacts:
- MANDATE.md avec baseline, droits, oracle, exclusions et échéance ; inventaire des
  fichiers avant/après.
success_criteria:
- Le diff ne touche que le trieur ; le test vérifie l’ordre et la stabilité ; le propriétaire
  accepte explicitement le périmètre. Un inventaire de chemins seul ne prouve pas
  la qualité du tri.
references:
- git-worktree
---
# Mandat & découpage

> Statut : brouillon méthodologique, à adapter — non ratifié dans les projets consommateurs.

## Pourquoi un mandat ?
Une demande n'est pas une capacité d'action. Le mandat lie un objectif à un état de référence, à des droits limités et à des critères de clôture observables.

| Dimension | Question à résoudre | Pièce requise |
|---|---|---|
| Baseline | Quel dépôt, commit et worktree ? | Empreinte + `git status` |
| Périmètre | Quelles zones peut-on modifier ? | Chemins autorisés et exclusions |
| Autorité | Qui peut lire, écrire, exécuter ou publier ? | Octroi explicite, borné |
| Gate | Que signifie succès/échec ? | Tests RED/GREEN, résultats attendus |
| Sortie | Quels livrables peuvent être produits ? | Patch, preuve, doc, décision |

### Unités de travail
Un **programme** contient des chantiers ; un **chantier** contient des tranches causales ; une **tranche** possède un seul objectif vérifiable. Ne pas substituer une liste de tâches à une preuve de réalisation.

### Gate d'entrée
Une tranche peut commencer seulement si les inconnues dangereuses sont identifiées. Les hypothèses sont permises, mais doivent rester marquées comme telles.

### Exercice
Rédige un `MANDATE.md` pour un composant fictif de notification : implémenter une nouvelle méthode de tri sans toucher au service de stockage. Ajoute trois interdictions explicites.

<details><summary>Auto-évaluation</summary>Ton mandat doit nommer un commit, un périmètre de fichiers, les interdictions, un test déterministe, un critère d'arrêt et une sortie inspectable. Il ne doit pas autoriser tacitement le déploiement.</details>


## Problème traité
Un tri de notifications est demandé, mais le mot « améliorer » ne définit ni résultat ni périmètre.

## Méthode reproductible
1. Épingler HEAD et le statut Git
2. définir une entrée [urgent, normal, urgent], la sortie attendue et les chemins du trieur
3. nommer le responsable qui peut accepter le diff
4. écrire un critère d’arrêt si le stockage doit changer.

**Responsabilités :** l’auteur propose et enregistre les résultats ; le relecteur critique l’oracle ; le propriétaire du projet décide de l’adoption.

## Exemple, contre-exemple et échec
Bon exemple : conserver l’ordre des deux urgents et laisser le stockage intact. Contre-exemple : « optimiser tout le système ». Échec : une nouvelle exigence agrandit tacitement le mandat ; demander un amendement traçable.

## Artefacts et qualification
MANDATE.md avec baseline, droits, oracle, exclusions et échéance ; inventaire des fichiers avant/après.

Le diff ne touche que le trieur ; le test vérifie l’ordre et la stabilité ; le propriétaire accepte explicitement le périmètre. Un inventaire de chemins seul ne prouve pas la qualité du tri.

## Exercice de transfert
Applique la méthode au service fictif Courier. Produis les artefacts ci-dessus, puis invente un cas qui invalide une conclusion trop large.

<details><summary>Critères d’auto-évaluation</summary>Le cas est fictif et reproductible ; la baseline est nommée ; la procédure et le résultat attendu sont explicites ; un échec est conservé ; la conclusion cite les artefacts et leurs limites. Si un critère manque, corrige avant de déclarer la méthode appliquée.</details>
