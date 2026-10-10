---
id: independent-challenges
title: "Répliquer. Réfuter. Faire progresser la preuve."
status: draft
---
# Répliquer. Réfuter. Faire progresser la preuve.

Une invitation aux scientifiques indépendants : nos résultats sont des **hypothèses contestables**, pas des vérités à approuver. Nous cherchons des reproductions, des contre-exemples, des méthodes alternatives et des résultats négatifs documentés.

**Statut : brouillon scientifique ouvert aux critiques.** [Le corpus GitHub](https://github.com/tension-atoi/engineering-corpus) est public et ses Issues accueillent les critiques et contre-exemples authentifiés. Certains kits sont encore incomplets : nous les signalons explicitement. Gitea reste un miroir secondaire envisagé, **pas** la plateforme de soumission.

## Quatre défis scientifiques

### CUDA-05D — Identités et namespaces Linux

La question : un UID 0 *à l'intérieur* d'un namespace peut-il correspondre à un principal hôte différent selon le mapping ? Notre expérience ponctuelle ne démontrait **pas** cette distinction. Un contre-exemple valable doit montrer l'UID effectivement observé côté serveur avec `SO_PEERCRED`, et un témoin.

[Étude et limites](/fr/studies/cuda-05d.html) · [Données publiques limitées](/evidence/cuda-05d-public-results.json)

### CUDA-05E — Autorisation IPC et refus DAC

La question : un service réellement exécuté sous un autre UID hôte peut-il refuser à la fois un client connecté mais non autorisé, et un client bloqué avant la connexion par DAC ? Nous avons observé ce comportement dans un laboratoire Docker jetable. Nous invitons à rechercher les conditions qui le contredisent.

**Nouveau : [kit CUDA-05G de contre-expérience indépendante](/fr/studies/cuda-05g.html)**. Code et protocole publics; un seul essai local, réplication externe toujours en attente.

[Protocole préenregistré](/challenges/protocols/CUDA-05E-PREREG.md) · [Étude et limites](/fr/studies/cuda-05e.html) · [Données publiques limitées](/evidence/cuda-05e-public-results.json)

### CUDA-05F — Superviseur Rust, GPU et résilience

La question : les garanties d'identité et de révocation tiennent-elles *ensemble* lorsque de vrais workers CUDA/Vulkan fonctionnent et échouent ? Dix gates opérationnels ont passé en laboratoire, mais trois acquisitions antérieures ont révélé des défaillances. Le code du runtime complet n'est **pas** encore ouvert à une reproduction indépendante.

[Protocole préenregistré](/challenges/protocols/CUDA-05F-PREREG.md) · [Étude et contre-preuves conservées](/fr/studies/cuda-05f.html) · [Contrat expérimental](/experiments/GPU-EVIDENCE-CONTRACT-v1.json)

### CUDA-05H — Témoin GPU numérique ouvert

Peut-on reproduire, sur du vrai matériel, 6 144 résultats entiers identiques entre CPU, CUDA et Vulkan ? **Kit MIT autonome publiable**, avec source et oracle; une seule expérience locale réussie, réplication extérieure en attente. **Il ne remplace pas la preuve du moteur privé de blob.in.**

[Étude et protocole CUDA-05H](/fr/studies/cuda-05h.html) · [Résultats structurés](/evidence/cuda-05h-public-results.json)

## Comment participer scientifiquement

Une contradiction recevable doit identifier le claim et sa version Git, décrire l'environnement et les contrôles, conserver la méthode et les observations brutes (y compris les erreurs), présenter le critère réfuté, et proposer un moyen raisonnable de réexécuter l'expérience. L'auteur original doit pouvoir répondre sans effacer ni réécrire le résultat initial.

Le [contrat de contribution proposé](/challenges/CONTRIBUTING.md) et le [registre des défis](/challenges/registry.json) sont consultables. **[Soumettre une réplication ou une réfutation sur GitHub](https://github.com/tension-atoi/engineering-corpus/issues/new/choose)** (compte GitHub requis). Les issues publiques accueillent les objections, mais la réplication de CUDA-05F reste limitée par les sources non publiées.

## Notre engagement

Nous distinguerons toujours **observation**, **réplication indépendante**, **réfutation**, **revue** et **autorisation de production**. Une objection documentée doit demeurer adressable même si elle contredit nos résultats. Une empreinte SHA-256 ne rend pas des données privées accessibles, et aucun verdict local ne représente une vérité universelle.
