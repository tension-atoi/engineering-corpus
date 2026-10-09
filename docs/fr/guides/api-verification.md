# Vérifier une interface avant de la documenter

Un guide pratique pour distinguer **symbole réellement disponible**, **comportement éprouvé** et **API seulement envisagée**. Son exemple est volontairement fictif : il ne documente aucune interface de production Gnosix.

## 1. Commencer par la source

Le [support d'atelier B](/fr/labs/02-api.html) décrit la démarche. Son programme [api_lab.py](/examples/api_lab.py) possède un inventaire de symboles et une assertion observable. Le cas `Queue.morph_to` est absent ; `Queue.enqueue` est présent dans le support.

Consulter les [sources épinglées dans le registre](/registry/guide-catalog.json) avant de conclure quoi que ce soit sur leur fraîcheur. La révision épinglée garantit un contenu inspectable, **pas** la stabilité d'un SDK.

## 2. Exécuter les deux cas, localement

Depuis la racine du dépôt `engineering-corpus`, avec Python 3 :

```sh
python3 examples/api_lab.py --symbol Queue.morph_to
# Attendu : code de sortie 1 (symbole absent)
python3 examples/api_lab.py
# Attendu : code de sortie 0
python3 scripts/test_labs.py
```

Le premier échec est **prévu**, et doit être distingué d'un échec de dépendances ou d'une panne de l'environnement. Ne transforme pas un script qui réussit en preuve de stabilité d'une API externe.

## 3. Relier contrat et preuve

Consigner : SHA du code étudié, symbole demandé, résultat et code de sortie, environnement d'essai, limites explicites. Classer séparément `public-stable`, `public-experimental` et `internal` ; aucun statut n'est accordé par la rédaction seule.

Pour comparer la méthode avec une interface Rust publique, consulter [EngineProvider v0](/fr/api.html). Cette référence reste **expérimentale**, non distribuée comme SDK, et ne décrit aucun endpoint HTTP. Les essais Python de ce guide ne qualifient pas cette interface Rust.

## 4. Réviser et publier

Rédiger la même conclusion en FR et en EN, avec liens réciproques et état de maturité. Ne pas publier de code, poids de modèles, identifiants ou fichiers privés. Les changements proposés passent par une revue de source distincte.

**Limite de preuve :** ce guide explique et exerce une méthode pédagogique avec un programme fictif ; il ne constitue ni une certification, ni un tutoriel d'installation du produit Gnosix.
