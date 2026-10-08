---
id: 03-contract
title: Architecture & contrats
duration: 14
status: draft
category: core
method_id: EC-M03
classification: proposed-principle
prerequisites:
- Bases de Git
- Lire le résultat d’un test
artifacts:
- CONTRACT.md ; table de transitions ; exemple exécutable de l’atelier A ; journal
  des identités d’action.
success_criteria:
- Une demande valide produit une action unique ; une demande refusée n’en produit
  aucune. Le modèle pédagogique ne prouve pas la continuité d’un vrai moteur graphique.
references:
- python-unittest
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


## Problème traité
Un menu fictif conserve son état pendant une interruption mais risque de déclencher deux fois la même action.

## Méthode reproductible
1. Nommer les états idle, moving, denied et done
2. préciser les entrées request_id/target
3. décider qui possède l’action
4. spécifier les doublons et l’annulation
5. écrire des oracles pour interruption, refus et reprise.

**Responsabilités :** l’auteur propose et enregistre les résultats ; le relecteur critique l’oracle ; le propriétaire du projet décide de l’adoption.

## Exemple, contre-exemple et échec
Bon exemple : une reprise change la cible mais conserve request_id. Contre-exemple : le renderer lance l’action à chaque frame. Échec : un retry possède une identité neuve et contourne la déduplication ; fixer le contrat du retry.

## Artefacts et qualification
CONTRACT.md ; table de transitions ; exemple exécutable de l’atelier A ; journal des identités d’action.

Une demande valide produit une action unique ; une demande refusée n’en produit aucune. Le modèle pédagogique ne prouve pas la continuité d’un vrai moteur graphique.

## Exercice de transfert
Applique la méthode au service fictif Courier. Produis les artefacts ci-dessus, puis invente un cas qui invalide une conclusion trop large.

<details><summary>Critères d’auto-évaluation</summary>Le cas est fictif et reproductible ; la baseline est nommée ; la procédure et le résultat attendu sont explicites ; un échec est conservé ; la conclusion cite les artefacts et leurs limites. Si un critère manque, corrige avant de déclarer la méthode appliquée.</details>
