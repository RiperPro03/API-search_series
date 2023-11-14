from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import math
import spacy
from langdetect import detect
from typing import List, Dict

# ----------------- Initialisation ------------------------------------------------------------------------------------

app = FastAPI()

# Charger les modèles linguistiques Spacy pour le français et l'anglais
nlp_fr = spacy.load("fr_core_news_sm")
nlp_en = spacy.load("en_core_web_sm")

# Connexion à MongoDB
# pour la BD locale : mongodb://localhost:27017
# pour la BD distante : mongodb+srv://riperpro:IBkTL4m1H4zZvzsl@cluster0.urnuehu.mongodb.net/BD_DataVisualizer?retryWrites=true&w=majority
client = MongoClient("mongodb+srv://riperpro:IBkTL4m1H4zZvzsl@cluster0.urnuehu.mongodb.net/BD_DataVisualizer?retryWrites=true&w=majority")
db = client['SAE']
collection = db['motsTF']

# Récupérer les noms de toutes les séries dans la collection
pipeline = [
    {"$project": {"documents": 1}},
    {"$project": {"documents": {"$objectToArray": "$documents"}}},
    {"$unwind": "$documents"},
    {"$group": {"_id": "$documents.k"}}
]
all_series_names = {doc['_id'] for doc in collection.aggregate(pipeline)}

# Utilisez l'agrégation pour calculer les longueurs de tous les documents
pipeline = [
    {"$project": {"_id": 0, "documents": {"$objectToArray": "$documents"}}},
    {"$unwind": "$documents"},
    {"$group": {"_id": "$documents.k", "total": {"$sum": "$documents.v"}}}
]

# Remplir le dictionnaire all_dls avec les résultats
all_dls = {}
for doc in collection.aggregate(pipeline):
    all_dls[doc['_id']] = doc['total']

# Constantes BM25
k1 = 1.5
b = 0.75
# Longueur moyenne des documents
avg_dl = sum(all_dls.values()) / len(all_dls) if all_dls else 0
# Nombre total de documents
N = collection.count_documents({})


# ----------------- Fonctions -----------------------------------------------------------------------------------------
def bm25(idf, tf, dl):
    """
        Calcule le score BM25 pour un terme dans un document.

        Arguments:
        - idf (float) : L'inverse de la fréquence du document pour le terme.
        - tf (int)   : La fréquence du terme dans le document.
        - dl (int)   : La longueur du document.

        Variables globales:
        - k1 (float)   : Paramètre de saturation de la fréquence du terme. Par défaut, il est fixé à 1.5.
        - b (float)    : Paramètre qui décide du niveau d'importance de la longueur du document. Par défaut, il est fixé à 0.75.
        - avg_dl (int) : Longueur moyenne des documents.

        Retourne:
        float : Le score BM25 du terme pour le document donné.
        """
    return idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (dl / avg_dl)))


def detect_language(text):
    """
    Détecte la langue d'un texte.

    Arguments:
    - text (str): Le texte dont la langue doit être détectée.

    Retourne:
    str : Code de langue détecté (par exemple "fr" pour le français).
         En cas d'erreur, retourne "en" (anglais) par défaut.
    """
    try:
        return detect(text)
    except:
        return "en"


def extract_keywords(query):
    """
    Extrait les mots-clés pertinents d'une requête en fonction de la langue détectée.

    Arguments:
    - query (str): La requête à partir de laquelle extraire les mots-clés.

    Retourne:
    list : Liste des mots-clés extraits.
    """
    lang = detect_language(query)
    if lang == "fr":
        nlp = nlp_fr
    elif lang == "en":
        nlp = nlp_en
    else:
        nlp = nlp_en
    doc = nlp(query)
    keywords = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "VERB", "PROPN"]]
    if query not in keywords and query in all_series_names:
        keywords.insert(0, query)
    return keywords


def recherche(query):
    """
    Recherche et classe les séries en fonction des mots-clés extraits de la requête.

    Arguments:
    - query (str): La requête de recherche.

    Retourne:
    list : Liste de tuples avec le nom de la série et son score, triée par score décroissant.
    """
    mots = extract_keywords(query)
    scores = {}
    documents = list(collection.find({"_id": {"$in": mots}}))
    for document in documents:
        df = document['document_frequency']
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
        for serie, tf in document['documents'].items():
            dl = all_dls[serie]
            score = bm25(idf, tf, dl)
            if serie in scores:
                scores[serie] += score
            else:
                scores[serie] = score
    for serie_name in all_series_names:
        if mots and serie_name.lower() == mots[0].lower():
            scores[serie_name] = scores.get(serie_name, 0) + 2500
        elif serie_name.lower() in [mot.lower() for mot in mots]:
            scores[serie_name] = scores.get(serie_name, 0) + 2000
        elif serie_name.lower() == query.lower():
            scores[serie_name] = scores.get(serie_name, 0) + 1000

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_scores


def top_keywords(series_list, word_n):
    """
    Extrait les top_n mots-clés d'une liste de séries.

    Arguments:
    - series_list (list): Liste des noms de séries.
    - word_n (int): Nombre de mots-clés à extraire.

    Retourne:
    list : Liste des mots-clés extraits.
    """
    pipeline = [
        {"$match": {"$or": [{f"documents.{series_name}": {"$exists": True}} for series_name in series_list]}},
        {"$project": {
            "word": "$_id",
            "total_frequency": {"$sum": [f"$documents.{series_name}" for series_name in series_list]}
        }},
        {"$sort": {"total_frequency": -1}},
        {"$limit": word_n},
        {"$match": {"word": {"$regex": "^.{5,}$"}}}  # Filtrer les mots ayant 5 caractères ou plus
    ]

    results = list(collection.aggregate(pipeline))
    return [res["word"] for res in results]


# ----------------- API ------------------------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <h2>Bienvenue à l'API de recherche de séries !</h2>

    <p><strong>Utilisation:</strong></p>
    <ol>
        <li>
            Pour rechercher des séries, utilisez le endpoint <code>/search/</code> avec le paramètre <code>query</code> pour indiquer votre requête. 
            <br>Par exemple : <code>/search/?query=nom_de_la_série</code>
        </li>
        <li>
            Vous pouvez également limiter le nombre de résultats en utilisant le paramètre <code>top_n</code>. 
            <br>Par exemple : <code>/search/?query=nom_de_la_série&top_n=10</code> retournera les 10 meilleures séries basées sur votre recherche.
        </li>
        <li>Pour obtenir des séries similaires à une liste de séries, utilisez le endpoint <code>/similar_series/</code> et envoyez un POST avec une liste de noms de séries.
            <br>Par exemple : <code>/similar_series/</code> avec le corps <code>{"series_list": ["Lost", "The Walking Dead"]}</code> retournera les séries similaires à "Lost" et "The Walking Dead".
        </li>
        <li>
            Pour obtenir la liste de toutes les séries disponibles, utilisez le endpoint <code>/all_series/</code>.
        </li>
    </ol>
    """
    return HTMLResponse(content=html_content)


@app.get("/search/")
def search(query: str, top_n: int = None) -> Dict[str, List[str]]:
    """
    Moteur de recherche pour les séries.

    - **query**: La requête de recherche.
    - **top_n** (optional): Nombre de résultats à retourner. Si non défini, tous les résultats sont retournés.

    ### Exemple d'utilisation:
    - Pour obtenir tous les résultats : `/search/?query=lost`
    - Pour obtenir les 10 meilleurs résultats : `/search/?query=lost&top_n=10`
    """
    all_results = recherche(query)
    limited_results = all_results[:top_n] if top_n else all_results
    series_names = [serie[0] for serie in limited_results]

    return {"series": series_names}


@app.post("/similar_series/")
def similar_series(series_data: Dict[str, List[str]], top_n: int = None, word_n: int = 1000) -> Dict[str, List[str]]:
    """
    Recherche des séries similaires à partir d'une liste de séries.

    - **series_data**: Un dictionnaire avec la clé "series_list" contenant la liste des séries.
    - **top_n** (optional): Nombre de séries similaires à retourner. Si non défini, toutes les séries sont retournées.
    - **word_n** (optional): Nombre de mots-clés à utiliser pour la recherche. Si non défini, 1000 mots-clés sont utilisés.

    ### Exemple:
    POST /similar_series/
    {
        "series_list": ["lost", "breaking bad"]
    }
    """
    series_list = series_data.get("series_list", [])

    if not series_list:
        raise HTTPException(status_code=400, detail="La liste des séries ne peut être vide.")

    query = ' '.join(top_keywords(series_list, word_n))

    all_similar_series = [serie[0] for serie in recherche(query) if serie[0] not in series_list]
    best_series = all_similar_series[:top_n] if top_n else all_similar_series

    return {"series": best_series}


@app.get("/all_series/")
def all_series():
    """
    Retourne la liste de toutes les séries disponibles dans la base de données.
    """
    return {"series": list(all_series_names)}