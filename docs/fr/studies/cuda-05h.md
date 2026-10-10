---
id: study-cuda-05h
title: "CUDA-05H — CPU, CUDA et Vulkan : une géométrie calculable et réfutable"
status: draft
classification: independent-public-numeric-witness
---
# CUDA-05H — CPU, CUDA et Vulkan : une géométrie calculable et réfutable

> **Recherche publique, expérience locale unique.** Une nouvelle implémentation sous licence MIT exécute une scène binaire identique avec un oracle Python, un kernel CUDA et un shader Vulkan. **Réplication externe : en attente.** Le moteur privé de blob.in n'a pas été publié ni reproduit ici.

## Hypothèse préenregistrée et calcul

Avant d'implémenter les kernels, nous avons fixé le protocole **CUDA-05H-P01** au commit `b89b266829b396d5b9569e0cbb2cd38a04f603bb` et une scène de 16 primitives sur une grille 96 × 64. Chaque primitive encode un centre, un rayon et une opération géométrique (`min` pour union, `max` pour intersection, `max(acc,-q)` pour soustraction). Le score `q = (x-cx)² + (y-cy)² - r²` est un **substitut géométrique quadratique entier**, **pas** le calcul de distance signée flottante original.

**Critère de succès :** exactement **6 144 valeurs `int32`**, soit **24 576 octets**, identiques CPU/CUDA/Vulkan, sans aucune tolérance. Un seul octet différent suffit à réfuter la parité. Vulkan doit exécuter sur un GPU matériel, non un rendu logiciel.

## Observations sur RTX 3070

| Backend | Exécution observée | Parité exacte |
|---|---|---|
| Python CPU | Référence recalculée indépendamment | PASS |
| CUDA compilé natif | GPU NVIDIA RTX 3070, synchronisation et copie | PASS |
| Vulkan/SPIR-V compilé natif | GPU RTX 3070, shader, fence et lecture mémoire | PASS |
| Bit inversé dans la sortie CUDA | Validateur distinct refuse le résultat | PASS |
| Sortie Vulkan tronquée | Validateur distinct refuse le résultat | PASS |

Les trois sorties produisent l'empreinte SHA-256 `613845b6341e4491efce3be997853467213ef6687770495b0d2515329678961b`. Le contrôleur indépendant passe **8/8 gates**, et le manifeste public vérifie les fichiers du kit et un nouveau calcul CPU sans exiger de GPU.

## Pour un laboratoire extérieur : reproduire ou contredire

**[Sources CPU, CUDA, GLSL et Vulkan, outils de compilation et protocole](https://github.com/tension-atoi/engineering-corpus/tree/main/research/blob-in/CUDA-05H)** · [Résultats numériques structurés](/evidence/cuda-05h-public-results.json) · [Déposer une contre-expérience](https://github.com/tension-atoi/engineering-corpus/issues/new/choose)

Sans GPU NVIDIA, on peut exécuter l'oracle CPU et vérifier l'intégrité du kit; on **ne peut pas** conclure à la parité CUDA/Vulkan. Une reproduction valable rapporte le GPU/driver, le compilateur, les paramètres de shader, les hashes des résultats, les contrôles et les tentatives échouées. Aucune mise à jour du VPS ou réinitialisation GPU n'est requise.

## Ce qui demeure hors preuve

Cette étude fournit un **témoin de calcul GPU indépendamment implémenté** : elle ne démontre pas l'équivalence du moteur SDF privé CUDA-02/03, la récupération des workers CUDA-05F, la sécurité d'exécution, ni la fiabilité sur d'autres GPU. Les sorties et journaux bruts du run original restent privés; un hash public ne les rend pas auditables par lui-même. Les chercheurs peuvent cependant produire leurs propres données à partir des sources intégrales du kit.

**Statuts explicites :** réplication externe `PENDING`; original CUDA-05F `BLOCKED_PRIVATE_RUNTIME_SOURCE`; parité CUDA-05F `NOT_RUN`; autorisation de production `DENIED`.
