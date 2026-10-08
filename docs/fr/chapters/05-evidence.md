---
id: 05-evidence
title: Preuves & vérité publique
duration: 16
status: draft
category: core
method_id: EC-M05
classification: proposed-principle
prerequisites:
- Bases de Git
- Lire le résultat d’un test
artifacts:
- EVIDENCE.json ; échantillons bruts ; calcul de médiane ; phrase de portée bornée.
success_criteria:
- Un autre lecteur retrouve 10 ms avec les cinq valeurs. Ce calcul pédagogique n’est
  pas un benchmark réel ; cinq mesures ne suffisent pas à estimer une p95 fiable.
references:
- python-statistics
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


## Problème traité
Le rapport fictif Beacon annonce une latence générale à partir d’un seul échantillon favorable.

## Méthode reproductible
1. Définir métrique, unité et population
2. figer code et environnement
3. effectuer un warmup puis au moins cinq répétitions
4. conserver tous les échantillons
5. calculer médiane et étendue
6. relier la phrase publique au manifeste et aux exclusions.

**Responsabilités :** l’auteur propose et enregistre les résultats ; le relecteur critique l’oracle ; le propriétaire du projet décide de l’adoption.

## Exemple, contre-exemple et échec
Exemple fictif [9,10,10,11,100] ms : médiane 10 ms, étendue 9–100 ms. Contre-exemple : retirer 100 sans règle préalable. Échec : comparer deux moteurs avec des paramètres différents ; déclarer la déviation et refaire une comparaison comparable.

## Artefacts et qualification
EVIDENCE.json ; échantillons bruts ; calcul de médiane ; phrase de portée bornée.

Un autre lecteur retrouve 10 ms avec les cinq valeurs. Ce calcul pédagogique n’est pas un benchmark réel ; cinq mesures ne suffisent pas à estimer une p95 fiable.

## Exercice de transfert
Applique la méthode au service fictif Courier. Produis les artefacts ci-dessus, puis invente un cas qui invalide une conclusion trop large.

<details><summary>Critères d’auto-évaluation</summary>Le cas est fictif et reproductible ; la baseline est nommée ; la procédure et le résultat attendu sont explicites ; un échec est conservé ; la conclusion cite les artefacts et leurs limites. Si un critère manque, corrige avant de déclarer la méthode appliquée.</details>
