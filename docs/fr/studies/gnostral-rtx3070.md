---
id: study-gnostral-rtx3070
title: "Gnostral — qualification RTX 3070 : MoE et placement sous pression mémoire"
status: draft
classification: bounded-local-inference-experiment
---
# Gnostral — MoE et placement sous contrainte mémoire

> Étude locale expérimentale répétée, **sans reproduction externe vérifiée**. Aucune qualification de production ni autorisation de superviseur GPU.

## Q-010 : poids MoE CPU Q2_K/Q3_K sans copies répétées

Même Qwen3-30B-A3B Q2_K sur RTX 3070 8 Gio, trois lancements par voie avec sorties complètes.

| Médiane | Strata baseline | Candidat Q-010 |
|---|---:|---:|
| Six contrôles techniques | 9,51 tok/s | 20,18 tok/s |
| VRAM totale au pic | 2 344 Mio | 2 351 Mio |
| RSS des processus | 22 094 Mio | 22 172 Mio |

Le rapport médian de débits est de **2,12×**, avec six paires de réponses identiques octet pour octet. Mais le **premier essai a échoué** au contrôle de restitution VRAM (+196 Mio pour une limite de 128 Mio). La répétition indépendante, sans modification des seuils, a passé tous les contrôles. Le code Rust unsafe de l'emprunt n'a pas encore fait l'objet d'un audit exhaustif. Aucune supériorité face à llama.cpp n'est démontrée.

## Q-011 : placement au chargement sensible à la VRAM

Une réservation CUDA externe de **2 048 Mio**, sans calcul concurrent continu, a réduit le placement GPU du même modèle de 48 couches :

| Trois démarrages | Contrôle | VRAM réservée |
|---|---|---|
| Couches GPU | 22, 21, 21 | 13, 12, 13 |
| Débit médian checklist | 20,88 tok/s | 20,15 tok/s |

**Adaptation au démarrage démontrée**, mais pas de déplacement à chaud de couches déjà chargées. PagedAttention était désactivé dans les deux configurations mixtes CPU/GPU.

## Méthode, limites, falsification

La VRAM représente toute la carte, bureau compris ; RSS ne correspond pas au PSS privé. Trois exécutions par condition ne généralisent pas au-delà de cette charge. Les réponses Q-011 varient entre essais ; la structure est contrôlée, non leur qualité générale. Les logs et poids GGUF originaux ne sont pas distribués avec cette étude ; les empreintes seules ne rendent pas une expérimentation privée reproductible.

**[Données publiques assainies](/evidence/gnostral-rtx3070-public-results.json)** · **[Registre scientifique](/fr/experiments.html)**

Statuts : réplication externe PENDING ; PagedAttention mixte NOT_QUALIFIED ; autorisation de production DENIED.
