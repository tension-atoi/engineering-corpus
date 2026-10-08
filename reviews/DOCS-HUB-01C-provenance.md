# DOCS-HUB-01C — Registre public SDK/API

**Périmètre :** source publique seulement, aucune revendication de service en production, aucune inspection de dépôt privé. Contrat versionné dans `docs/source-registry.json`, copie exacte publiée sous `/registry/source-catalog.json`.

## Inventaire vérifié — 2026-10-08

| Domaine | État | Preuve |
|---|---|---|
| SDK | Aucun SDK distribuable qualifié | Aucun dépôt identifié avec artefact SDK officiellement distribué et version qualifiée |
| API | Une référence de programmation Rust **expérimentale** | `gnostral.rs` / `EngineProvider v0` |
| API HTTP | Aucun endpoint public qualifié | Le `EngineProvider` est un trait Rust, pas un serveur |
| Guides / Releases | Hors tranche 01C | Aucune fiche présentée comme qualifiée |

### Source `gnostral-engine-provider-v0`

- Repository public : <https://github.com/tension-atoi/gnostral.rs>
- HEAD inspecté : `59a892d3e4dc56bd574e7d062f69f96b7b8193f0`
- Trait : `harness/engine-provider-contract/src/lib.rs`
- SHA-256 du fichier : `6e364db2676ce657f3ab986c1d0be2eca93cd389b426e7e5a26c3b27836f4cef`
- Manifeste : `harness/engine-provider-contract/Cargo.toml`
- SHA-256 du manifeste : `dfdb5bffcadec3f61ffd95c258e216193590360cf946922fec33cb39090197af`
- Version déclarée du crate : `0.0.1`; publication crates.io désactivée : `publish = false`.
- Type d'interface : Rust `pub trait EngineProvider`. Le fichier annonce explicitement un *reference model*, non un runtime. L'architecture de supervision n'est pas ratifiée (voir `docs/ARCHITECTURE.md` upstream).
- Transport : aucune API HTTP ni RPC exposée par ce contrat. Adapteurs async/streaming hors du trait présenté.
- Statut éditorial : **EXPERIMENTAL / PUBLIC_SOURCE_VERIFIED / NOT_DISTRIBUTED**.

Les empreintes ont été observées sur les URLs brutes GitHub référencées à ce commit et les chemins exacts ont été comparés à la branche publique. **Ces contrôles prouvent la présence des octets publics ; ils ne qualifient pas l'interopérabilité d'un SDK, un endpoint, la compatibilité de runtime, un support ou une garantie de stabilité.**

## Contrat de publication

1. Toute nouvelle source exige : propriétaire, dépôt réellement public, SHA Git complet, chemin exact, hash SHA-256 du fichier, nature de l'interface, statut de cycle de vie, et version justifiée par un manifeste quand elle existe.
2. Aucun chemin local de poste, secret, configuration Authentik, adresse d'administration ou dépôt non public.
3. Un résultat `source_verified` ne vaut jamais `stable`, `released` ou `operational`.
4. Le générateur statique consomme les fichiers JSON déjà versionnés et n'effectue pas de récupération réseau à la construction ni dans le navigateur.
5. Un domaine sans contenu distribué peut ouvrir une **page d'inventaire vide explicite**. Il ne peut pas annoncer un installateur ou une API fonctionnelle.
6. Les liens sources externes autorisés sur les pages API pointent vers le code public épinglé sur GitHub.
7. Ne pas casser `/fr/index.html`, `/en/index.html`, les chapitres ni la clé locale de progression du corpus.

## Reproduction minimale de la provenance

Sur un poste connecté (pas pendant le build statique) :

```sh
git ls-remote https://github.com/tension-atoi/gnostral.rs.git refs/heads/main
curl -fsSL https://raw.githubusercontent.com/tension-atoi/gnostral.rs/59a892d3e4dc56bd574e7d062f69f96b7b8193f0/harness/engine-provider-contract/src/lib.rs | sha256sum
curl -fsSL https://raw.githubusercontent.com/tension-atoi/gnostral.rs/59a892d3e4dc56bd574e7d062f69f96b7b8193f0/harness/engine-provider-contract/Cargo.toml | sha256sum
```

**Restriction temporelle :** le HEAD du dépôt pourrait avancer après la vérification. Le registre conserve un commit immuable ; actualiser une référence nécessite une nouvelle inspection du diff et des empreintes.
