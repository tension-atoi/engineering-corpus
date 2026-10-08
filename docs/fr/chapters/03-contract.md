---
id: 03-contract
title: "Architecture & contrats"
duration: 14
status: draft
category: core
---
# Architecture & contrats

> Statut : brouillon méthodologique, à adapter — non ratifié dans les projets consommateurs.

## Séparer les responsabilités
Une bibliothèque fournit des capacités ; un profil compose des politiques et des comportements ; une surface présente une vue ; l'autorité décide si une action peut s'exécuter. Ces catégories ne sont pas interchangeables.

| Responsabilité | Exemple de contrat | Refus explicite |
|---|---|---|
| Géométrie | rectangles et transformations typées | ne décide pas du contenu |
| Mouvement | chronologie, interruption, continuité | ne signe pas d'action système |
| Rendu | projection visible de l'état | n'invente pas la source de données |
| Contenu | état et identité des éléments | ne détermine pas une permission |
| Événements | ordre et causalité | ne dépasse pas un grant |
| Data providers | provenance, cadence, erreur | n'autorise pas une mutation |
| Policy/actions | vérification des capacités | n'impose pas un thème UI |

### Contrat d'interface
Définir `inputs`, `outputs`, `errors`, `ownership`, `lifecycle`, `concurrency`, `cancellation`, `deprecation`, et la surface `public/internal/experimental`.

### Exemple de transition
Lorsqu'une surface change d'ancrage pendant un mouvement, expliciter le point de départ observé, l'état cible, la règle d'interruption et les invariants géométriques. Une animation visuellement fluide n'est pas une preuve de correction des responsabilités.

### Exercice
Un menu animé veut lancer un processus. Où placer la permission ? Que devient l'animation si l'action est refusée ?

<details><summary>Auto-évaluation</summary>La permission est vérifiée à la frontière d'exécution, non dans la courbe d'animation. Le refus est un état métier explicite que le rendu peut refléter sans attribuer d'autorité au composant visuel.</details>
