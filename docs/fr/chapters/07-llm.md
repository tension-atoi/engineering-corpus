---
id: 07-llm
title: LLM local & Copilot
duration: 15
status: draft
category: core
method_id: EC-M07
classification: proposed-principle
prerequisites:
- Bases de Git
- Lire le résultat d’un test
artifacts:
- Inventaire de contexte ; proposition étiquetée ; résultat du validateur déterministe
  ; limites de l’observation réseau.
success_criteria:
- Le validateur refuse un symbole inventé même si le texte est convaincant. Un test
  sans egress observé ne démontre pas que le fournisseur est local ; aucune configuration
  fournisseur réelle n’est certifiée ici.
references:
- python-unittest
---
# LLM local & Copilot

> Statut : brouillon méthodologique, à adapter — non ratifié dans les projets consommateurs.

## Un agent est un instrument contrôlé
Copilot, OpenCode ou un LLM local peut produire des hypothèses, diffs, guides et exemples. Les mécanismes de preuve restent indépendants du modèle.

### Séquence de travail
1. Exclure secrets et code privé non autorisé ; enregistrer le HEAD et les chemins.
2. Extraire les symboles et tests par outil déterministe ; réduire le contexte.
3. Transmettre seulement le contexte approuvé au modèle et à l'endpoint vérifié.
4. Demander une **proposition**, avec citations de fichiers/lignes et signalement des incertitudes.
5. Vérifier symboles, compilation, autorité et diff par des outils indépendants.
6. Revoir humainement avant toute intégration ou publication.

| Risque | Contrôle |
|---|---|
| Prompt sortant inconnu | contrôle réseau et configuration réelle |
| Dérive d'autorité | grants distincts pour lire, écrire, exécuter, publier |
| Hallucination | extraction déterministe et tests |
| Contexte excessif | minimisation + inventaire des fichiers transmis |
| Secret dans les logs | redaction avant partage + scanner local |
| Dépendance au fournisseur | entrée/sortie standardisées, fallback sans IA |

### Token hygiene
Partager des contrats ciblés et des diffs compacts au lieu du dépôt entier. Un résumé antérieur non ancré dans un commit n'est pas une source fiable.

### Exercice
Un plugin Copilot affiche un modèle local, mais ouvre une connexion cloud. Décris un test d'autorisation avant lecture de code privé.

<details><summary>Auto-évaluation</summary>Confirmer l'endpoint, les logs, la résolution DNS, le trafic sortant et l'identité du fournisseur ; refuser les transferts non approuvés et faire tourner l'essai sur données publiques fictives.</details>


## Problème traité
Le nom « local » affiché par un outil ne décrit pas forcément tous ses transferts.

## Méthode reproductible
1. Commencer sur données inventées
2. inventorier fichiers transmis, configuration et fournisseur
3. examiner les sorties observables
4. minimiser le contexte
5. exiger des références vérifiables
6. valider sans modèle
7. conserver un parcours manuel si le modèle est indisponible.

**Responsabilités :** l’auteur propose et enregistre les résultats ; le relecteur critique l’oracle ; le propriétaire du projet décide de l’adoption.

## Exemple, contre-exemple et échec
Bon exemple : deux signatures publiques fictives et un diff ciblé. Contre-exemple : transmettre le dépôt entier « pour être complet ». Échec : un prompt injecté demande de publier ; traiter le texte comme données et appliquer le mandat original.

## Artefacts et qualification
Inventaire de contexte ; proposition étiquetée ; résultat du validateur déterministe ; limites de l’observation réseau.

Le validateur refuse un symbole inventé même si le texte est convaincant. Un test sans egress observé ne démontre pas que le fournisseur est local ; aucune configuration fournisseur réelle n’est certifiée ici.

## Exercice de transfert
Applique la méthode au service fictif Courier. Produis les artefacts ci-dessus, puis invente un cas qui invalide une conclusion trop large.

<details><summary>Critères d’auto-évaluation</summary>Le cas est fictif et reproductible ; la baseline est nommée ; la procédure et le résultat attendu sont explicites ; un échec est conservé ; la conclusion cite les artefacts et leurs limites. Si un critère manque, corrige avant de déclarer la méthode appliquée.</details>
