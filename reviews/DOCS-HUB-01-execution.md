# DOCS-HUB-01 — Portail documentaire fédérateur

**Mandat opérateur :** transformer `docs.gnu6.live` en portail gnu.in.labs pour corpus, SDK, API, guides et releases ; premiumiser le rendu conformément au design system et aux constats navigateur. Le premier parcours conserve le nom **« Corpus Méthodologique & Hygiène Mental »** (orthographe opérateur, sans normalisation éditoriale implicite). La ludification est une direction future, non une fonction déjà disponible.

**Baseline :** `tension-atoi/engineering-corpus`, `main @ fcf9eeb02c8e087cf046a71c2ac9c2b96f6bae19` au lancement de ce mandat. `docs.gnu6.live` sert ce dépôt via une application Static Coolify indépendante, `/dist`, sans build dynamique ni CI GitHub obligatoire.

**Architecture d'autorité :** le dépôt `engineering-corpus` reste propriétaire de son contenu et de sa compilation ; le portail pourra fédérer plusieurs sources documentaires, mais n'aspire ni secrets, ni documents privés, ni spécifications non publiées. Chaque contenu externe doit porter une provenance vérifiable. Coolify publie un SHA revu et épinglé ; pas de publication automatique par simple push. Aucun changement aux routes/domaines des autres applications.

## Décisions de produit

1. Une page d'accueil de **hub**, pas une fausse page API ; distinguer catalogue des surfaces effectivement disponibles.
2. Le corpus demeure indépendant et immédiatement accessible via ses URLs FR/EN existantes. Ne pas renommer le dépôt ou la clé `engineering-corpus:study:v0.1` sans migration explicite.
3. L'apparition de sections SDK/API/Guides/Releases **ne signifie pas** disponibilité d'une API, d'un SDK, d'un support ou d'une release.
4. Le corpus reste `DRAFT / ADOPTION_PENDING`. Les sources externes ont un état individuel : `published`, `experimental`, `draft`, `retired`, `unavailable`.
5. Les interfaces affichent des vérités observées, pas des confirmations déduites d'une action : statut et provenance sont visibles.
6. **Design system :** `gnosix_DS` V3.4.1, tokens et sémantiques explicitement ratifiés. Pas de CHIP décoratif, de gradient générique ni de cards répétitives sans utilité. Space Grotesk reste la police définie par cette baseline ; tout changement de famille fera l'objet d'une décision distincte.
7. **Décision CTA :** le plein Signal Orange `#FF6A00` + anthracite respecte la direction normative de la palette, mais rend mal sur le site réel. Plutôt que d'installer du texte clair insuffisamment contrasté sur ce fond, employer un substrat anthracite/surface sombre + texte Shell White et utiliser Signal Orange comme encadrement, repère directionnel et état de focus. Les états hover/active/focus doivent rester lisibles. Orange = direction, pas remplissage obligatoire.

## Séquence de livraison

| Tranche | Branche | Commits prévus | Production | Définition de terminé |
|---|---|---|---|---|
| **01A — CTA & contrat** | `feat/docs-hub-01a-cta-contract` | 1. `docs(docs-hub): ratify execution plan`; 2. `fix(ui): replace unreadable filled-orange primary CTA` | Déploiement manuel possible seul | Les CTA visibles FR/EN et `study-button` conservent leurs liens, labels et interactions ; surfaces sombres, texte clair, accent Orange, focus discernable ; desktop + 375 px ; pas de régression de build |
| **01B — Information architecture** | `feat/docs-hub-01b-navigation` (depuis `main` après 01A) | 1. navigation hub ; 2. home hub ; 3. migration de navigation du corpus | PR autonome | Le portail annonce les sections réelles, distingue contenu disponible / futur, liens existants résolus, FR primaire et EN équivalent, progression intacte |
| **01C — Inventaire de provenance SDK/API** | `feat/docs-hub-01c-source-registry` | 1. contrat registre ; 2. extraction de sources publiques vérifiées ; 3. génération statique des références disponibles | PR autonome | Chaque page SDK/API générée possède source, SHA ou version, état, mainteneur, périmètre et date de vérification ; aucune référence simulée. Si aucune source qualifiée, page d'inventaire indiquant explicitement `Aucune référence publique qualifiée` |
| **01D — Guides & releases** | `feat/docs-hub-01d-guides-releases` | 1. guides sourcés ; 2. releases vérifiées ; 3. pages de version et liens | PR autonome | Guides reliés à un artefact connu, release attribuée à un tag/repository réel, mentions de compatibilité sourcées |
| **01E — Parcours enrichis** | Phase ultérieure, non bloquante | Décision UX + prototypes | À décider | Modèle de progression et défis fondé sur l'apprentissage, sans certifications ni XP artificiels ; consentement pour tout stockage hors navigateur |

**Important :** 01B peut introduire des chemins de hub `/fr/` et `/en/`; ne pas déplacer les chemins du corpus avant d'avoir implémenté redirections exactes et contrôlé les URL publiées. Aucune SPA catch-all qui transforme les 404 en HTTP 200. Pour de nouvelles racines, choisir un contrat d'URL explicite, puis le documenter avant le code.

## Contrat de sources 01C

Un enregistrement candidat est un objet versionné avec au minimum :

```json
{
  "id": "stable-source-id",
  "kind": "sdk|api|guide|release",
  "owner": "nom du projet",
  "source_repository": "URL publique vérifiée",
  "source_ref": "SHA ou tag vérifié",
  "source_path": "chemin source existant",
  "version": "version réellement déclarée",
  "lifecycle": "published|experimental|draft|retired|unavailable",
  "visibility": "public",
  "locale": "fr|en",
  "last_verified": "date ISO liée à une vérification réelle",
  "route": "/chemin attribué, non présumé"
}
```

Ce schéma est une **proposition à implémenter**, pas une assertion qu'il existe déjà des SDK ou des API publics. Rejeter les chemins secrets, credentials, sources non approuvées et URL non résolues. Les enregistrements sans preuve restent candidats et ne s'affichent pas comme références actives.

## Contrats de conception / QA proportionnée

- Tout contrôle sert une mutation précise ; pas de campagne de gate non sollicitée.
- Frontières de tests : builder statique, liens internes FR/EN, page 404 stricte, contraste des éléments réellement rendus, clavier, un viewport mobile représentatif.
- Vérification source : le CSS servi en production correspond à la modification approuvée ; l'image Coolify vient du commit `main` choisi.
- Contenu : ne pas afficher un bouton qui prétend ouvrir une surface non développée ; distinguer « en préparation » d'un lien accessible.
- CTA principal et boutons de progression : même rôle = même grammaire de surface, mais un état complété utilise une hiérarchie secondaire sans masquer le statut.
- Ne pas surcharger la racine du dépôt de rapports. Ajouter les seules preuves utiles dans `evidence/runs/docs-hub-01*/` après assainissement ; journal brut local ignoré.
- Si la publication échoue : retirer/annuler uniquement la nouvelle image ou rétablir l'image précédente du **même** conteneur, sans modifier Traefik, DNS ni les autres applications.

## Rôles agents sans chevauchement

- **Surface / design :** tokens, composants, focus, captures du site réel. Livrer styles/markup sans inventaire externe.
- **Documentation / registry :** découvrir et qualifier les sources publiques SDK/API ; ne pas éditer les styles.
- **Release / opérateur :** intégrer une PR cohérente, épingler son SHA Coolify, déployer et constater. Aucun agent ne suppose autorité sur les autres applications.

## Convention des états

`PLANNED` → `IMPLEMENTED_LOCAL` → `REVIEWED_ON_PR` → `MERGED` → `DEPLOYED` → `OBSERVED_ON_PUBLIC_SITE`.

N'afficher que le dernier état démontré, pas l'état visé. Avant fusion, lire l'ensemble des PR ouvertes et refuser les anciennes branches divergentes. Le worker conserve tout autre worktree et ne modifie pas `corpus-01e-final-browser-qualification`.

## Handoff immédiat

Commencer par **01A** et publier la correction CTA seule. Ensuite proposer un wireframe fonctionnel de home hub (FR/EN) avant de créer les sections de références. L'expansion des disciplines et la ludification ne dépendent pas du correctif CSS ; ne pas les utiliser comme condition de publication.
