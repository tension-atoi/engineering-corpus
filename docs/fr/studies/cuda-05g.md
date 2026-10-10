---
id: study-cuda-05g
title: "CUDA-05G — Reproduire et contester une frontière Linux réelle"
status: draft
classification: independently-implemented-fixture-local-trial
---
# CUDA-05G — Reproduire et contester une frontière Linux réelle

> **Étude ouverte · essai local unique · reproduction externe en attente.** Ce kit est une **implémentation nouvelle et publiable**, non une libération du runtime privé blob.in. Il teste uniquement le contrôle des identités Unix et des permissions DAC étudié en CUDA-05E.

## L'hypothèse que vous pouvez mettre en défaut

Un serveur de socket Unix sous un véritable UID hôte distinct doit pouvoir autoriser un client prévu, rejeter **après connexion** un autre UID autorisé à accéder au socket, empêcher **avant connexion** un client sans permission DAC, puis continuer à servir le premier client. Une réussite n'est recevable que si le serveur enregistre lui-même les UID fournis par le noyau avec `SO_PEERCRED` et si l'UID hôte du service est contrôlé dans `/proc`.

**Protocole figé avant l'essai :** commit `396c36e7aef2271544bb98d025129c6de1a73547`, identifiant `CUDA-05G-P01`. Le code et le protocole sont couverts par la licence MIT du corpus.

## Ce que nous avons effectivement obtenu

| Contrôle | Observation |
|---|---|
| UID réel du service, différent du client | PASS dans le laboratoire local |
| Client autorisé initial | PASS |
| UID connecté mais non autorisé | Refus observé par le service |
| Client sans permission DAC | Connexion refusée **avant** le service |
| Client autorisé après refus | PASS |
| Nettoyage et terminaison du serveur | PASS |
| Falsifications du validateur | 2 incohérences rejetées |
| Calcul CUDA/Vulkan et superviseur Rust CUDA-05F | **NOT_RUN / BLOCKED** |

Un **seul essai complet** a passé. Les deux tentatives précédentes ont été archivées en tant qu'échecs de précondition ou de dispositif expérimental : image Docker indisponible; chemin Unix dépassant la limite Linux et témoin DAC mal construit. Les amendements ont été commités avant les relances, plutôt que d'être effacés.

## Reproduction externe : ouverte pour cette sous-hypothèse

Le kit contient du code source nouveau, les témoins positifs/négatifs, un orchestrateur hors réseau, un validateur indépendant de l'acquisition, son manifeste SHA-256 et les critères de contre-preuve.

**[Code, protocole et instructions sur GitHub](https://github.com/tension-atoi/engineering-corpus/tree/main/research/blob-in/CUDA-05G)** · [Résultats publics bornés](/evidence/cuda-05g-public-results.json) · [Soumettre une contre-preuve](https://github.com/tension-atoi/engineering-corpus/issues/new/choose)

Un lecteur peut relancer l'essai sur **son propre Linux avec Docker rootful**, observer les événements privés, puis proposer un résultat divergent, négatif ou inconclusif. Il ne faut pas attaquer un système réel en production pour éprouver l'hypothèse.

## Limites qu'aucune interface ne doit masquer

Le code indépendant et les données assainies sont publics, **mais un chercheur externe n'a pas encore soumis de réplication**. Un Docker rootful possède une autorité supérieure au service testé. Le pilote GPU, la parité CPU/CUDA/Vulkan, l'intégrité d'un fournisseur natif et les chemins de récupération CUDA-05F ne sont pas testés dans ce kit. Les données brutes originales restent privées; leur empreinte n'est pas un accès public à la preuve.

**Conclusion :** un artefact de falsification exploitable pour les garanties Linux IPC, pas une qualification indépendante du runtime GPU blob.in ni une autorisation de production.
