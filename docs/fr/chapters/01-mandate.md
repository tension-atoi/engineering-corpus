---
id: 01-mandate
title: "Mandat & découpage"
duration: 12
status: draft
category: core
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
