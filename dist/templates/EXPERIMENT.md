# EXPERIMENT — Contrat de recherche / Research contract

> **Statut / Status:** modèle de travail; ni accréditation, ni approbation de production.
> Remplir les champs **avant** la collecte; commiter une version immuable. / Fill in **before** acquisition; commit an immutable revision.

## 1. Question, frontière et décision / Question, boundary, decision

- `experiment_id`:
- `source_commit`:
- `research_question`:
- `decision_if_supported`:
- `decision_if_refuted`:
- `decision_if_inconclusive`:
- `owner` / `reviewer`:
- `environment`: OS, kernel, hardware, drivers, runtime versions, isolation scope.
- `publication_classification`: private / restricted / public-sanitized.

## 2. Hypothèses réfutables / Falsifiable hypotheses

| ID | Null / H0 | Alternative / H1 | Mesure observable / Observable | Seuil fixé d'avance / Preregistered threshold |
|---|---|---|---|---|
| H01 | … | … | … | … |

**Ne pas reformuler H0/H1 après les résultats. / Do not revise hypotheses after seeing data.**

## 3. Plan de tests / Protocol

- Population, unité d'observation, critères d'inclusion/exclusion / Population, observation unit, inclusion/exclusion:
- Témoin positif et contrôle négatif / Positive control and negative control:
- Procédure et commandes exactes / Procedure and exact commands:
- Nombre de répétitions, ordre, randomisation et warmup (si pertinents) / Repeats, order, randomization, warmup (if relevant):
- Métrique, unité, estimand, méthode statistique (si mesurée) / Metric, unit, estimand, statistical method (if measured):
- Erreurs, crashs, timeouts et valeurs manquantes / Errors, failures, timeouts, missing values:
- Facteurs de confusion et limites d'environnement / Confounders and environmental limits:
- **STOP:** conditions d'arrêt sans escalade de privilèges ni destruction de données / Stop conditions:

## 4. Acquisition et conservation / Acquisition and custody

- `raw_data_schema` + unités + exemples conformes:
- `raw_data_file`, `sha256`, UTC, exit codes, version de l'instrument:
- `protocol_commit` (antérieur aux mesures / earlier than data):
- `instrument_commit`:
- `analysis_commit` (peut différer de l'instrument / may differ):
- `deviations_from_prereg` avec raisons et date / with reason and date:
- `reproduction_command`:
- `independent_validator`: idéalement différent du code producteur / preferably separate from producer.
- `falsifier`: altérer une valeur sans toucher la source et vérifier le refus / tamper a copied value and verify rejection.

**Une empreinte ne révèle pas un fichier inaccessible. / A digest does not reveal unavailable source evidence.**

## 5. Registre d'affirmations / Claims ledger

| Claim ID | Classe E0–E6 (sens local) | Source brute | Transformation | Résultat / Verdict | Limite | Public ? |
|---|---|---|---|---|---|---|
| C01 | … | … | … | Supported / Refuted / Inconclusive | … | No |

Ne jamais confondre **test réussi**, **observé en matériel réel**, **intégré** et **exploité**. / Do not equate a passing test, real-hardware observation, integration and sustained operation.

## 6. Revue et publication / Review and release

- Vérification des données manquantes, de la sélection, du dénominateur et des versions / Missingness, selection, denominator, version checks:
- Interprétation alternative + expérience discriminante / Alternative interpretation and discriminating experiment:
- `review_status`: draft / reviewed / approved / blocked.
- `public_projection`: whitelist de champs non sensibles / non-sensitive field whitelist.
- `source_visibility`: accès vérifiable ou non / independently accessible or not.
- `publication_gate`: **BLOCK** until claims, evidence, scope, privacy and ownership all pass.
- `next_experiment`: conditions qui modifieraient la décision / conditions that would change the decision.

**Échec du gate ≠ échec de la méthode scientifique. / A blocked release gate is not a failed scientific method.**
