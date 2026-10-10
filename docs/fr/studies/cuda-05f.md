---
id: study-cuda-05f
title: "CUDA-05F — Qualifier la chaîne GPU complète sans cacher ses échecs"
status: draft
classification: bounded-internal-observation
---
# CUDA-05F — Qualifier la chaîne GPU complète sans cacher ses échecs

> **Étude locale, octobre 2026 · Brouillon soumis à revue.** Le superviseur Rust et les workers CUDA/Vulkan ont été testés dans des conteneurs jetables. Une qualification de laboratoire ne vaut ni validation de sécurité globale ni autorisation de déploiement.

## La question

Les propriétés établies séparément en CUDA-05C et CUDA-05E sont-elles observables **ensemble dans le vrai service Rust** ? Il faut tester l'identité de service, l'IPC, la révocation et la récupération, tout en vérifiant réellement les sorties GPU contre une référence CPU.

Le protocole **CUDA-05F-P01** a été figé au commit `03ba7945fe6740b2cf35dc28656ba866f66c33fb` avant les acquisitions. Le contrat partagé `gnu6.gpu-evidence-contract.v1` impose 11 gates indépendants et interdit de transformer une réussite expérimentale en droit de publication ou d'exploitation.

## Résultats du quatrième run

| Contrôle observé | Résultat |
|---|---|
| Service sous une identité Linux hôte distincte | PASS |
| Client autorisé, client connecté refusé par `SO_PEERCRED`, et refus DAC | PASS |
| Rendu CUDA réel et comparaison numérique à l'oracle CPU | PASS |
| Rendu Vulkan réel et comparaison numérique à l'oracle CPU | PASS |
| Crash du worker, révocation, puis nouvel appel GPU | PASS sur les deux backends |
| Timeout du worker, révocation, puis nouvel appel GPU | PASS sur les deux backends |
| Remplacement du worker ou du fournisseur natif CUDA | Refus constaté, restauration vérifiée |
| Autorité de publication ou de production | **NOT_QUALIFIED** |

**10 des 11 gates sont qualifiés dans le périmètre opérationnel du laboratoire.** Le onzième gate n'a pas échoué par hasard : il reste ouvert car aucune approbation de production n'a été accordée.

## Trois expériences qu'il aurait été facile d'effacer

- **Run 01 — Vulkan RED.** Le service Rust utilisait un chemin de recherche dynamique ELF qui empêchait la détection de l'adaptateur Vulkan. Le test discriminant a opposé RUNPATH et RPATH, puis la correction a été documentée.
- **Run 02 — preuve d'identité incomplète.** Le serveur refusait le client, mais son journal ne conservait pas l'UID réellement observé par le noyau. Une modification ciblée a ajouté un événement `SO_PEERCRED` côté serveur.
- **Run 03 — cycle de vie IPC RED.** Dans un scénario de crash Vulkan, un client déconnecté a provoqué un `Broken pipe` fatal. Le superviseur a été corrigé pour révoquer le permis lorsqu'une réponse ne peut plus être livrée.

Le **run 04** a réexécuté les huit scénarios avec la méthode amendée. Ces quatre acquisitions sont archivées séparément : **elles ne constituent pas quatre répétitions équivalentes ni une statistique de fiabilité**.

## Chaîne de preuves et limites

Le service tournait comme **une autre identité hôte réelle** que son client autorisé. Le socket avait un répertoire contrôlé, et un client ayant accès au socket mais non autorisé a été refusé à partir de l'UID observé par le serveur. Chaque rendu passait par un worker sacrifiable, avec parité numérique CPU sur le GPU réel.

La reconstruction a passé **69 tests Rust cumulés**, puis un validateur indépendant a vérifié les événements bruts, les générations et les erreurs attendues. Il a également rejeté une fausse identité de service. Les résultats incluent un manifeste SHA-256, les versions d'environnement et les amendements méthodologiques.

**Ce que cela ne prouve pas :** résistance au démon Docker privilégié, isolement d'un worker hostile utilisant le même UID, signature fiable d'un fournisseur natif, perte physique GPU, disponibilité durable ou exploitation de Gnosix en production. Le refus d'un fournisseur corrompu est prouvé comportementalement; son message d'erreur interne n'était pas directement enregistré.

Les traces internes contiennent des identifiants Linux et restent privées. Les données consultables ici sont volontairement restreintes : **un hash de données privées ne permet pas au lecteur de les auditer**. Une reproduction externe indépendante reste à organiser.

**[Résultats structurés assainis](/evidence/cuda-05f-public-results.json)** · [Manifeste de provenance](/evidence/cuda-05f-manifest.json) · [Contrat expérimental](/experiments/GPU-EVIDENCE-CONTRACT-v1.json) · [Registre](/fr/experiments.html)

## Décision

**Classe :** E4 interne, observation d'une chaîne réelle en laboratoire, non ratifiée. **Publication :** brouillon pour revue scientifique indépendante. **Gate de déploiement :** `DENIED`. Le prochain essai doit confronter cette architecture à un worker réellement confiné et à une politique d'autorité de service indépendante; le reset du GPU servant le bureau reste exclu.
