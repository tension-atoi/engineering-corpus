---
id: 07-llm
title: "LLM local & Copilot"
duration: 15
status: draft
category: core
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
