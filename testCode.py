# import json
# from rank_bm25 import BM25Okapi
# import re
#
# # Chargez les données depuis le fichier JSON
# with open("data_series.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
#
# # Préparez les données pour l'indexation par BM25
# corpus = []
# titles = []  # Pour stocker les titres des séries en parallèle avec le corpus
# for serie in data:
#     # Concaténation des phrases pour former un document par série
#     document = " ".join(serie["phrases"])
#     corpus.append(document)
#     titles.append(serie["nom"])  # Ajoutez le titre de la série à la liste
#
# # Tokenisation des documents du corpus
# tokenized_corpus = [doc.split(" ") for doc in corpus]
#
# # Création d'un objet BM25
# bm25 = BM25Okapi(tokenized_corpus)
#
#
# # Fonction de recherche
# def search(query):
#     tokenized_query = query.split(" ")
#     scores = bm25.get_scores(tokenized_query)
#
#     # Associe chaque score à son titre de série
#     scored_titles = [(score, title) for score, title in zip(scores, titles)]
#     # Trie les titres par score décroissant
#     scored_titles.sort(key=lambda x: x[0], reverse=True)
#
#     # Récupère les 3 meilleurs titres
#     top_titles = [title for _, title in scored_titles[:3]]
#
#     return top_titles
#
#
# # Test de la fonction de recherche
# query = "drug"
# series_results = search(query)
#
# print(f"Résultats pour la requête '{query}':")
# print(series_results)


# Pour télécharger les couvertures des séries
# import requests
# import os
# from pymongo import MongoClient
#
# client = MongoClient("mongodb://localhost:27017")
# db = client['SAE']
# collection = db['test']
#
# # Récupérer les noms de toutes les séries dans la collection
# pipeline = [
#     {"$project": {"documents": 1}},
#     {"$project": {"documents": {"$objectToArray": "$documents"}}},
#     {"$unwind": "$documents"},
#     {"$group": {"_id": "$documents.k"}}
# ]
# # series_list = {doc['_id'] for doc in collection.aggregate(pipeline)}
# series_list = ['robin hood', 'Masters of Science Fiction']
#
# def get_series_cover(series_name):
#     # Récupération des informations sur la série à partir de l'API TVmaze
#     response = requests.get(f'https://api.tvmaze.com/singlesearch/shows?q={series_name}')
#     if response.status_code == 200:
#         json_response = response.json()
#         image_url = json_response.get('image', {}).get('original')
#         return image_url
#     else:
#         print(f'Failed to retrieve info for {series_name}')
#         return None
#
#
# def download_image(url, folder, filename):
#     # Téléchargement de l'image
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(os.path.join(folder, filename), 'wb') as img_file:
#             img_file.write(response.content)
#     else:
#         print(f'Failed to download image from {url}')
#
#
# # Création du dossier pour stocker les images
# if not os.path.exists('img-series'):
#     os.makedirs('img-series')
#
# # Boucle sur la liste des séries et téléchargement des couvertures
# for series in series_list:
#     image_url = get_series_cover(series)
#     if image_url:
#         download_image(image_url, 'img-series', f'{series}.jpg')

import json
import math

# Charger l'index inversé
with open('index_inversé.json', 'r', encoding='utf-8') as f:
    index_inverse = json.load(f)

N = len(index_inverse)  # Nombre total de documents
k1 = 1.5  # Ces valeurs sont généralement utilisées dans la littérature BM25
b = 0.75

# Calculer la longueur moyenne des documents
avg_dl = sum(len(info['documents']) for term, info in index_inverse.items()) / N


def bm25(idf, tf, dl):
    # Calculer le score BM25 pour un terme
    return idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (dl / avg_dl)))


def recherche(query):
    mots = query.split()
    scores = {}

    # Liste des noms de toutes les séries dans l'index inversé
    all_series_names = {serie for term, info in index_inverse.items() for serie in info['documents']}

    # Pour chaque mot dans la requête
    for mot in mots:
        if mot in index_inverse:
            df = index_inverse[mot]['document_frequency']
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
            for serie, info in index_inverse[mot]['documents'].items():
                tf = info['term_frequency']
                dl = len(index_inverse[mot]['documents'])  # Longueur du document
                score = bm25(idf, tf, dl)
                # Cumuler les scores
                if serie in scores:
                    scores[serie] += score
                else:
                    scores[serie] = score

    # Si la requête correspond exactement à un nom de série, donner la priorité
    for serie_name in all_series_names:
        if serie_name.lower() == query.lower():
            scores[serie_name] = scores.get(serie_name, 0) + 1000  # valeur arbitrairement élevée pour garantir la première place

    # Classez les séries en fonction de leur score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Retournez les noms des séries
    top_series_names = [item[0] for item in sorted_scores]

    return top_series_names


# Test
query = "avion"
print(recherche(query))

import math
from pymongo import MongoClient
import time
import spacy

nlp_fr = spacy.load("fr_core_news_sm")


def extract_keywords(query):
    doc = nlp_fr(query)
    # Extraire les substantifs et les verbes
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "VERB"]]
    return keywords


# Connexion à MongoDB
"""
mongodb://localhost:27017 pour la BD locale
mongodb+srv://riperpro:IBkTL4m1H4zZvzsl@cluster0.urnuehu.mongodb.net/BD_DataVisualizer?retryWrites=true&w=majority pour la BD distante
"""
client = MongoClient("mongodb://localhost:27017")
db = client['SAE']
collection = db['test']

N = collection.count_documents({})  # Nombre total de documents

# Constantes BM25
k1 = 1.5
b = 0.75

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

avg_dl = sum(all_dls.values()) / len(all_dls) if all_dls else 0


def bm25(idf, tf, dl):
    return idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (dl / avg_dl)))


def recherche(query):
    start_time = time.time()

    # Extraire les mots-clés de la requête
    keywords = extract_keywords(query)
    print(f"Mots-clés extraits de la requête: {', '.join(keywords)}")

    # Concaténer les mots-clés pour former une nouvelle requête
    mots = keywords
    scores = {}

    # Récupérer les noms de toutes les séries dans la collection
    pipeline = [
        {"$project": {"documents": 1}},
        {"$project": {"documents": {"$objectToArray": "$documents"}}},
        {"$unwind": "$documents"},
        {"$group": {"_id": "$documents.k"}}
    ]
    all_series_names = {doc['_id'] for doc in collection.aggregate(pipeline)}

    print("Recherche des documents correspondants...")
    documents = list(collection.find({"_id": {"$in": mots}}))
    print(f"{len(documents)} documents trouvés.")

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

    print("Ajustement des scores basé sur les mots exacts ou la correspondance exacte de la série...")
    for serie_name in all_series_names:
        if serie_name.lower() in [mot.lower() for mot in mots]:
            scores[serie_name] = scores.get(serie_name, 0) + 2000
        elif serie_name.lower() == query.lower():
            scores[serie_name] = scores.get(serie_name, 0) + 1000

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    end_time = time.time()
    print(f"Recherche terminée en {end_time - start_time:.2f} secondes.")

    return sorted_scores


# Test
query = "avion île crash"
results = recherche(query)
for serie, score in results[:20]:  # Limiter à 20 résultats
    print(f"Série: {serie}, Score: {score}")



