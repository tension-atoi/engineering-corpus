---
id: 05-evidence
title: "Preuves & vérité publique"
duration: 16
status: draft
category: core
---
# Preuves & vérité publique

> Statut : brouillon méthodologique, à adapter — non ratifié dans les projets consommateurs.

## Faire correspondre l'affirmation à sa preuve
Une capture du bureau prouve une observation visuelle bornée ; un test Rust prouve un scénario exécutable ; un benchmark prouve une mesure reproductible **dans son environnement**. Aucun ne prouve la stabilité de toutes les API.

| Classe | Nature | Exemple de preuve | Limite |
|---|---|---|---|
| E0 | Intention | mandat signé | aucune exécution |
| E1 | Statique | symbole + commit | aucune réussite runtime |
| E2 | Exécutable | test reproductible | scénario borné |
| E3 | Mesuré | médiane, dispersion, machine | environnement limité |
| E4 | Observé | trace/screenshot daté | observation ponctuelle |
| E5 | Intégré | chemin causal multi-module | pas d'exploitation longue |
| E6 | Exploité | historique monitoré | pas de preuve universelle |

### Règle de publication
Toute affirmation forte pointe vers un enregistrement avec `claim_id`, `source_commit`, date UTC, environnement, commande, code de sortie, hash d'artefact, limites et relecteur. La preuve expirée doit être revalidée.

### Une mesure correcte
Publier la commande, le warmup, les répétitions, la machine, les limites CPU/GPU, la variance et les cas exclus. Ne pas confondre débit moyen et latence p95.

### Exercice
Un README affirme « 2 % GPU idle » après une seule capture. Quelle reformulation et quelle expérience exigées ?

<details><summary>Auto-évaluation</summary>Reformuler comme observation ponctuelle contextualisée. Exiger méthode, métrique définie, instrumentation, échantillons, machine, charge, référence et marge d'erreur avant une affirmation générale.</details>
