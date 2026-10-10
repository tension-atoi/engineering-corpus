---
id: study-cuda-05e
title: "Quand le contrôle UID est réellement exercé"
status: draft
classification: bounded-internal-observation
---
# Quand le contrôle UID est réellement exercé

> **Étude expérimentale · 9 octobre 2026 · Brouillon soumis à revue.** Une observation de laboratoire Docker jetable, pas une certification de sécurité ni un déploiement du superviseur GPU.

## Question

Un service Linux exécuté sous une **identité hôte différente** de son client peut-il autoriser ce client, rejeter une autre identité qui dispose pourtant de l'accès au socket, et refuser un troisième client au niveau des permissions du système de fichiers ?

## Critères fixés avant l'essai

Le protocole **CUDA-05E-P01** était enregistré sous `84f82a786d80981edd824a2d9c81f4bbfd105c71` avant l'acquisition. Il distinguait trois barrières : identité réelle du service sur l'hôte, autorisation par `SO_PEERCRED` et contrôle d'accès DAC sur le socket.

Le premier essai a échoué **avant la moindre observation d'identité** : l'étape `chmod` ne possédait plus l'autorité requise après `chown`. Un amendement antérieur à la nouvelle acquisition, commité sous `fbd752d322a148f6d83279bef5cf04b4f9436374`, a inversé l'ordre des deux opérations sans ajouter de privilèges. Cet échec de précondition n'est pas effacé de l'historique scientifique.

## Résultats du nouvel essai

| Témoin ou traitement | Observation | Interprétation bornée |
|---|---|---|
| Service dans un conteneur Debian jetable | Son identité hôte différait de celle du client autorisé, confirmée par `/proc` et la configuration Docker. | Séparation réelle d'identités pour ce service de test. |
| Client autorisé | Connexion acceptée. | Chemin positif présent. |
| Client non autorisé, même groupe d'accès au socket | Connexion établie, puis refus par les credentials `SO_PEERCRED`. | Refus applicatif réellement exercé. |
| Client d'un groupe sans accès | Connexion interdite par les permissions avant `accept`. | Refus DAC distinct du refus applicatif. |
| Client autorisé après les refus | Connexion de nouveau acceptée. | Continuité de ce service de test. |

Le répertoire appartenait au service, avec le mode `0710` ; le socket utilisait `0660`. **Un seul essai terminé** a été réalisé, sans répétition statistique. Les tests sont indépendants des charges CUDA/Vulkan.

## Ce que cette preuve ne dit pas

Le démon Docker possède une autorité supérieure aux identités testées. Cette expérience ne qualifie donc **ni une isolation résistant à l'administrateur de l'hôte, ni le véritable service Rust CUDA-05C, ni une récupération après perte du GPU, ni la production**.

Les traces brutes, y compris les identifiants et les diagnostics des processus, demeurent privées. La projection publiable ne conserve que les verdicts bornés, l'empreinte de la trace originale et la provenance Git. **Une empreinte ne remplace pas un accès à la preuve brute** : la reproduction indépendante externe reste non démontrée.

**[Données publiques assainies](/evidence/cuda-05e-public-results.json)** · [Registre des expériences](/fr/experiments.html) · [Modèle expérimental réutilisable](/templates/EXPERIMENT.md)

## Prochaine expérience discriminante

Exécuter le **vrai superviseur Rust CUDA-05C** sous une identité de service dédiée, avec client autorisé et client refusé, sans exposer le bureau ni provoquer de reset GPU. Qualifier séparément les permissions IPC, le confinement des workers, les fichiers natifs et les conditions de récupération.

**Classe de preuve :** E4 interne, ponctuelle. **Gate production :** `DENIED`. **Statut :** `draft`, revue indépendante requise.
