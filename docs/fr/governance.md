---
id: governance
title: Gouvernance
status: draft
category: governance
---
# Gouvernance et contestation

## Classifications et autorité
| Classe | Sens | Décision |
|---|---|---|
| proposed-principle | Proposition de méthode à tester | Pas de ratification implicite |
| external-standard | Texte normatif externe identifié | Citer organisme, version et portée ; pas de conformité automatique |
| recommendation | Conseil contextualisé | Publier prérequis et exceptions |
| ratified-decision | Décision propre au corpus | Requiert propriétaire, date, portée et ADR accepté |

Les huit méthodes et trois ateliers restent `draft`. CORPUS-01 est une revue d’auteur de leur qualité éditoriale, pas un passage automatique à `adopted`. Aucune décision méthodologique ratifiée n’est introduite dans cette édition.

## Proposer ou contester
Ouvre une issue avec identité EC-M/EC-L, édition/commit, affirmation contestée, contre-exemple reproductible et conséquence. Une objection peut contester l’oracle lui-même. Fournis des données fictives et une proposition de correction FR/EN.

Le mainteneur accuse réception, nomme un relecteur, consigne preuves et désaccords, puis répond : accepté, amendement requis, différé avec raison, ou rejeté avec raison. L’objection demeure consultable. Une PR acceptée enregistre la décision dans le dépôt ; elle ne ratifie aucune politique d’un autre projet.

## États et éditions
`draft → reviewed → adopted → deprecated → retired` ; `rejected` conserve une proposition refusée. `reviewed` nécessite un relecteur nommé et la portée de sa revue. `adopted` nécessite un propriétaire et un ADR ; son autorité se limite au corpus. Un projet consommateur ratifie séparément ses adaptations.

Les éditions documentaires sont identifiées par catalogue, commit, notes de changement et manifeste. Une correction compatible incrémente le patch ; une nouvelle méthode incrémente la version mineure ; un changement incompatible de contrat impose une nouvelle édition majeure et un guide de migration. Cette convention est une proposition de gouvernance pour revue, pas une release déjà publiée.

## Gate de publication
Build propre isolé, dérive nulle, vérification des liens/métadonnées, ateliers positifs et négatifs, revue FR/EN, matrice navigateur et limites explicites. Les preuves ciblent un HEAD exact. La fusion n’est pas le déploiement. Domaine officiel futur : `docs.gnu6.live`.

## Vie privée et étude locale
La progression est une préférence locale au navigateur, partageable entre FR/EN et effaçable via les données du site. Elle n’est ni une attestation ni une preuve de compétence. En stockage bloqué, elle reste dans la page courante. Aucun compte ni service cloud n’est requis.

## Contribution
Joindre problème, baseline, sources, exemple/contre-exemple, FR/EN, résultats et limites. Ne pas soumettre de code privé, secrets, poids de modèles ou traces personnelles. Un tutoriel guide l’apprentissage ; une référence décrit un contrat ; un guide donne une méthode ; un runbook encadre une opération autorisée.
