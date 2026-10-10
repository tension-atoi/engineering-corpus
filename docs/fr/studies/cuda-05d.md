---
id: study-cuda-05d
title: "Quand « root » ne prouve pas une identité distincte"
status: draft
classification: bounded-internal-observation
---
# Quand « root » ne prouve pas une identité distincte

> **Étude expérimentale, 9 octobre 2026 · Non ratifiée · Reproductibilité externe partielle.** Cette page décrit un résultat borné sur une station Linux. Elle ne certifie ni l'isolation d'agents ni la sécurité d'un service de production.

## Question

Un processus lancé dans un espace de noms utilisateur en tant que `root` est-il nécessairement une **autre identité du point de vue du serveur hôte** ? L'expérience distingue l'identité affichée dans un espace de noms et l'identité noyau reçue par `SO_PEERCRED` sur un socket Unix.

## Ce qui était décidé avant de mesurer

Le protocole **CUDA-05D-P01** a été figé au commit `ee0ea36bae0950c04e13100c7f53cf7e643c82c4`, avant l'acquisition. Il prescrit une connexion témoin, une connexion sous `unshare --user --map-root-user`, un essai de mapping automatique des UID subordonnés et un verdict indépendant. Un véritable succès d'isolation aurait exigé **deux UID hôte distincts**, plus un service sous une seconde identité réelle et des scénarios d'autorisation et de refus.

Le plan prévoit explicitement `NOT_QUALIFIED` si ces éléments sont absents. Les critères ne sont donc pas abaissés en fonction du résultat.

## Trois observations, une seule machine

| Essai | Observation | Portée |
|---|---|---|
| Connexion témoin | L'UID vu par le serveur correspond à celui du processus hôte. | Contrôle de mesure réussi. |
| Namespace `--map-root-user` | Le processus voit UID 0 **à l'intérieur**, mais `SO_PEERCRED` reçoit **le même UID hôte que le témoin**. | Ce namespace ne crée pas une autre identité hôte dans cette configuration. |
| Mapping `--map-auto` | Exécution non aboutie ; erreur observée `newuidmap: Could not set caps`. | Le mapping subordonné n'est pas qualifié sur cet environnement. La cause profonde reste à investiguer. |

Les trois essais ont été tentés le **9 octobre 2026**, une seule fois sur cette machine. Le résultat ne généralise ni à tous les noyaux, ni aux installations rootless, ni aux systèmes disposant d'une délégation correcte des UID.

## Résultat, interprétation et autorité

**Observation (E4, interne) :** la comparaison des identités a été capturée via les credentials du noyau. **Interprétation :** un UID 0 affiché dans un user namespace ne prouve pas une séparation d'identité entre processus sur l'hôte. **Gate d'ingénierie :** `NOT_QUALIFIED` pour le superviseur dédié ; `DENIED` pour l'autorisation de production. Le code CUDA-05C démontre séparément la récupération après des pannes de processus enfants ; il ne démontre ni perte matérielle GPU, ni séparation des comptes hôte.

Cette étude est **reproductible en principe**, mais la source complète de l'expérience et ses traces brutes restent internes. Un hash seul ne permet pas à un tiers de vérifier le contenu d'une preuve indisponible. La donnée exportée contient seulement les décisions dérivées et l'empreinte de la trace interne, sans nom d'hôte, UID numérique ni PID.

**[Consulter les observations structurées](/evidence/cuda-05d-public-results.json)** · [Manifeste de provenance et statut de revue](/evidence/cuda-05d-manifest.json).

## Transférer la méthode

Le modèle réutilisable **[EXPERIMENT — contrat de recherche](/templates/EXPERIMENT.md)** sépare hypothèses fixées à l'avance, témoins, données brutes, transformations, évaluateur indépendant et droit de publication. Un résultat négatif doit être conservé, pas effacé.

## Conditions pour une nouvelle qualification

Créer un environnement **sacrifiable** possédant deux véritables comptes hôte, prouver une connexion autorisée et une connexion refusée au socket du superviseur, conserver les traces `SO_PEERCRED`, puis étudier les fautes GPU indépendamment, sans risquer la session graphique. Ajouter les journaux datés, codes de retour, schéma des données, résultats négatifs et procédure exacte de reproduction.

Une expérience qui échoue à démontrer son hypothèse apporte une information utile. Elle ne devient pas une preuve de conformité par une reformulation marketing.

## Contrôle de publication

**Classe :** E4 pour une observation interne ponctuelle, pas E5/E6. **Statut documentaire :** brouillon d'étude, sans revue indépendante. **Accès externe aux sources complètes :** indisponible pour le moment. Cette page n'attribue aucun droit à un agent.
