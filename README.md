# API de Recherche de Séries (API-search_series)

Ce projet est une API de recherche de séries utilisant le modèle BM25 pour le classement des documents, intégré avec une interface FastAPI pour les interactions et MongoDB pour le stockage des données.

C'est un projet universitaire avec pour sujet la réalisation d'un site vitrine pour les séries TV. En utilisant les fichiers de sous-titres de 126 séries, nous avons développé un backend robuste qui offre deux fonctionnalités clés : une fonction de recherche et une fonction de recommandation de séries.

# Auteurs

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
- Uvicorn
- Spacy, avec les modèles `fr_core_news_sm` et
`en_core_web_sm` pour la tokenisation et l’analyse
linguistique.
- MongoDB
- Pymongo
- Langdetect

Pour installer les dépendances nécessaires, exécutez :

```bash
## Cration de l'environnement virtuel
python3 -m venv mon_env
cd mon_env
```

Mettre les fichiers du projet dans le dossier “mon_env” puis faire:

```bash
## Entrer dans l'environnement virtuelle
source bin/activate
```

```bash
## Installer toutes les bibliothèques requises
pip install -r requirements.txt
```

Modifier `main.py` à la ligne 20 si vous voulez modifier pour mettre votre propre base de données

```python
# Connexion à MongoDB
# pour la BD locale : mongodb://localhost:27017
# pour la BD distante : mongodb+srv://riperpro:IBkTL4m1H4zZvzsl@cluster0.urnuehu.mongodb.net/BD_DataVisualizer?retryWrites=true&w=majority
client = MongoClient("mongodb+srv://riperpro:IBkTL4m1H4zZvzsl@cluster0.urnuehu.mongodb.net/BD_DataVisualizer?retryWrites=true&w=majority")
db = client['SAE']
collection = db['motsTF']
```

La base de données est générée à partir d’un fichier index_inversé_MongoDB.json généré par `process.py` qui traite tous les sous-titres donnés.

```json
index_inversé_MongoDB.json :
{
  "_id": "stanton",
  "document_frequency": 20,
  "documents": {
      "24": 123,
      "charmed": 2,
      "cold case": 4,
      "criminal minds": 7,
      "dirt": 2,
      "ghost whisperer": 4,
      "gossip girl": 6,
      "greys anatomy": 5,
      "heroes": 8,
      "jericho": 6,
      "life": 4,
      "ncis": 8,
      "oz": 61,
      "prison break": 16,
      "smallville": 2,
      "stargate atlantis": 4,
      "the o.c": 4,
      "the shield": 2,
      "veronica mars": 5,
      "californication": 1
  }
} ...
```

## Démarrage

Pour lancer l’API :

```bash
## Entrer dans l'environnement virtuel
source bin/activate
```

```bash
## Lancer le serveur
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Arrêt

Pour arrêter le serveur faire CTRL+C
