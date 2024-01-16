# API de Recherche de Séries (API-search_series)

Ce projet est une API de recherche de séries utilisant le modèle BM25 pour le classement des documents, intégré avec une interface FastAPI pour les interactions et MongoDB pour le stockage des données.

C'est un projet universitaire avec pour sujet la réalisation d'un site vitrine pour les séries TV. En utilisant les fichiers de sous-titres de 126 séries, nous avons développé un backend robuste qui offre deux fonctionnalités clés : une fonction de recherche et une fonction de recommandation de séries.

# Authors

- [Christopher Asin](https://www.github.com/RiperPro03) [non-alternant]

- [Vincent Noguero](https://github.com/VINKYN) [non-alternant]


## Fonctionnalités

- **Recherche de séries** : Permet aux utilisateurs de trouver des séries en saisissant des mots-clés. Par exemple, les mots "crash", "avion", "île" devraient retourner la série "Lost" parmi les premiers résultats.
- **Recommandation de séries** : Suggère des séries similaires à une liste de séries données.

## Utilisation
L'API peut être interrogée directement via les endpoints suivants :

- ```/``` : Un endpoint GET qui affiche une page HTML avec des instructions de base.
- ```/search/?query=<query>&top_n=<number>``` : Un endpoint GET pour rechercher des séries avec le paramètre `query` pour indiquer votre requête et `top_n` pour limiter le nombre de résultats.
- ```/similar_series/``` : Un endpoint POST pour trouver des séries similaires basées sur une liste de séries. 
  - Par exemple : `/similar_series/` avec le corps ```{"series_list": ["Lost", "The Walking Dead"]}``` retournera les séries similaires à "Lost" et "The Walking Dead".
- ```/all_series/``` : Un endpoint GET qui retourne toutes les séries disponibles.


## Installation
### Prérequis

- Python 3.8+
- FastAPI
- Uvicorn (pour le déploiement local)
- Spacy, avec les modèles `fr_core_news_sm` et `en_core_web_sm` pour la tokenisation et l'analyse linguistique.
- MongoDB
- Pymongo
- Langdetect

Pour installer les dépendances nécessaires, exécutez :

```bash
## Cration de l'environnement virtuel
python3 -m venv mon_env
cd mon_env
```
Mettre les fichiers du projet dans le dossier mon_env puis faire:
```bash
## Entrer dans l'environnement virtuelle
source bin/activate
```
```bash
## Installer toutes les bibliothèques requises
pip install -r requirements.txt
```

## Démarrage
Pour lancer l'API :

```bash
## Entrer dans l'environnement virtuel
source bin/activate
```
```bash
## Lancer le serveur
uvicorn main:app --host 127.0.0.1 --port 8000 
```
