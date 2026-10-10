# SHELL-SPINE-01 / CORPUS-EXPORT-01 — Contrat de fédération documentaire

2026-10-10 · [CHECKPOINT] Candidat architectural, non déployé.

## Autorité

- **engineering-corpus** : sources Markdown, statuts éditoriaux, éditions FR/EN, preuves, provenance, export versionné et publication statique autonome.
- **gnu6-live** : shell React persistant, routes intégrées, barre globale, interactions, lecteurs, menus, progression locale et qualification UX.
- **gnu6-design** : tokens, primitives et comportement Motion, toujours versionnés.
- **plateforme gnu6.live** : DNS, Coolify, proxy, redirections, publication et retour arrière. Aucun merge applicatif n'autorise directement un déploiement.
- Les sites produit comme Gnosix restent des autorités séparées.

## Artefact

'exports/gnu6-shell-documents.v1.json', schéma 'gnu6.corpus.semantic.v1', créé hors réseau depuis 18 documents sources réels (8 chapitres + index, FR et EN).

Chaque document est décrit par son identifiant, route interne, URL héritée, statut, source, SHA-256, ancres et arbre sémantique strictement validé. Aucun script, style, iframe, attribut événementiel ou lien javascript n'est accepté. Il s'agit de nœuds sémantiques et non de HTML exécutable.

Le consommateur doit verrouiller le SHA-256 exact de cet artefact et l'identité Git de l'édition. Aucun accès à GitHub ni aux dépôts sources n'est nécessaire à la lecture.

## Invariants

- L'export ne retire rien aux sources Markdown ni au générateur 'dist' existant.
- Les URLs de 'docs.gnu6.live' restent indépendantes pendant la transition; aucune redirection n'est autorisée ici.
- Les ancres historiques 'section-N' demeurent identiques.
- Les 18 documents pilotes ne représentent pas l'ensemble des pages Docs; l'intégrateur doit refuser les pages non prises en charge.
- Le shell persistant doit maintenir le même document navigateur, le même header et la même instance du cube entre ses propres routes.
- Pas d'iframe, de voile d'écran, de copie manuelle de texte ou de modification des sémantiques de Gnosix.
