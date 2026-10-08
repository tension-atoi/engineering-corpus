# DOCS-HUB-01D-0 — Cartographie publique du programme

**Portée :** index de familles documentaires, pas registre intégral des travaux locaux. La présence d'un projet sur un poste n'est pas une autorisation de le publier.

## Contrat de provenance

Le catalogue `docs/ecosystem.json` classe six familles : produits et plateformes, interfaces et expérience, IA et orchestration, méthodologies et workflows, recherche et laboratoires, références développeurs.

Pour cette tranche, **seuls** les dépôts publics `tension-atoi/engineering-corpus` et `tension-atoi/gnostral.rs` ont été qualifiés comme sources utilisables. Leurs références Git sont épinglées dans le catalogue. Les familles sans dépôt publiquement qualifié restent descriptives et ne comportent aucun lien supposé vers une API, un produit ou un portail privé.

Le projet gnu.in.labs est plus vaste que ces deux dépôts ; ce catalogue **ne constitue pas un inventaire exhaustif**. Les domaines Gnosix, interfaces et moteur web ne doivent pas être considérés comme inexistants simplement parce qu'aucune source n'est publiée ici.

## Publication

- Génération 100 % statique en FR/EN : `/fr/ecosystem.html`, `/en/ecosystem.html`.
- Catalogue exploitable par machine : `/ecosystem/catalog.json`.
- Le corpus garde ses parcours, son état Draft et sa clé de progression.
- Aucune ingestion de repository privé, de fichier local sensible ou d'URL d'administration.
- Toute entrée future exige une décision de publicité, une provenance et une révision.
- Aucune liste dynamique GitHub au runtime : le portail est reproductible à partir du commit publié.

## Prochaines itérations

Relier progressivement les sources **explicitement autorisées**, puis établir pour chaque produit ses interfaces de documentation : guides, SDK, API, releases, décisions, contrats et preuves. Une mise à jour du catalogue ne ratifie pas la maturité d'un produit.
