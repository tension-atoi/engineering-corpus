# Scientific Evidence Pipeline — DOCS-HUB-01G

**Version:** `gnu6.gpu-evidence-contract.v1` · **Current status:** DRAFT / internal source-to-site qualification. This is a publication boundary, not an automated authority issuer.

## FR — Chaîne causale reproductible

L'objectif n'est pas de générer des histoires de réussite. Le corpus doit enregistrer **les distinctions que la réalité nous force à faire** : ce qui a été prévu, mesuré, réfuté, réparé puis qualifié dans un périmètre précis. Une expérience négative reste une preuve durable.

| Étape | Production déterministe | Contrôle d'entrée / sortie |
|---|---|---|
| 00. Prérégistration | Hypothèse H0/H1, matrice des observations, gate négatif, seuils, règle STOP | Commit Git existant **avant** les données |
| 01. Contrat commun | `GPU-EVIDENCE-CONTRACT-v1.json` identique, SHA-256 sur les deux branches | Schéma et 11 identifiants de gate immuables durant la campagne |
| 02. Acquisition | Événements serveur, versions d'environnement, UID noyau, calcul GPU, oracles CPU, erreurs et exit codes | Données brutes datées et amendements explicités |
| 03. Analyse | Transformation interprétée `RAW → DERIVED` | Aucun état manquant implicitement PASS |
| 04. Falsification | Évaluateur **différent du producteur**, recalcul de l'identité et des transitions, mutation contrôlée des faits | Rejet de valeurs forgées; manifestes SHA-256 |
| 05. Projection publique | `DERIVED → PUBLIC` par allowlist stricte et inspection de la source Git | Pas de PID/UID locaux, secrets, commandes privées ni droit de production |
| 06. Edition documentaire | Registre JSON versionné, pages FR/EN, preuves de build et navigateur | Brouillon non ratifié; revue humaine indépendante requise |

**Gates de recherche CUDA-05F :** 10 contrôles opérationnels réussis dans le dernier essai intégré, **plus un gate `release_authority=NOT_QUALIFIED`**. La règle de publication publique est donc **DENIED**. Le site peut construire un brouillon local sans qu'un service puisse être mis en production.

**Corpus E0–E6 :** cette classification est une convention éditoriale interne. E4 ici signifie une observation instrumentée ponctuelle, pas une certification indépendante E5/E6.

### Reproduction locale, lecture des sources sans accélération de l'autorité

```bash
# Requires the still-private local CUDA-05F evidence repository.
python3 scripts/ingest_gpu_experiment.py \
  --source /path/to/CUDA-05/methodology \
  --source-commit <pinned-source-commit> \
  --write
python3 scripts/build.py
python3 scripts/check.py
node scripts/qualify_evidence_browser.cjs
```

L'ingesteur exécute le validateur indépendant de la source privée **avant** toute mutation du registre. Il exige également que le JSON public soit identique aux bytes du commit source, que les données brutes correspondent à leur SHA et que le contrat partagé soit identique. `--write` produit uniquement des artefacts locaux; un déploiement exige une décision humaine distincte.

**Aucune garantie de réplication externe :** la trace brute est privée. Le checksum permet de détecter une modification *si la trace devient accessible*, mais n'autorise pas à prétendre qu'elle est vérifiable publiquement.

## EN — Integrity and decision contract

Scientific outputs are versioned separately from authority. The upstream worker supplies raw observations and a bounded public projection; a separate, fail-closed local importer verifies:

- Pre-data Git protocol provenance and **identical shared contract bytes**;
- Upstream source commit equality, raw-data SHA and independent source verifier success;
- Strict public allowlist, exactly eleven gate identities, valid state vocabulary and explicit **NOT_QUALIFIED** for release authority;
- A machine-readable provenance receipt and a bilingual study index;
- Static build integrity, negative-falsifier tests and responsive browser rendering.

The importer refuses any output that converts a laboratory `PASS` into `production_authorization=APPROVED`, omits a required gate, or changes the contract hash. An untested case stays `NOT_RUN` or `NOT_QUALIFIED`, never implicit green.

**Validity limits:** the producer and docs reviewer currently share one workstation under the operator's control. The "independent" verifier is separately implemented and deliberately falsified, not an external peer-reviewed replication. The rootful Docker daemon, same-UID worker compromise, signed binary provenance and actual GPU device loss remain outside the qualified perimeter.

**Decision boundary:** Source observation and local static rendering are allowed under this research task. Public publishing, service integration and sustained operations remain blocked until an explicit review and operator action.
