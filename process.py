# Pour le traitement des mots et la tokenisation
# import os
# import json
# import re
# import spacy
#
# nlp_en = spacy.load("en_core_web_sm")
# nlp_fr = spacy.load("fr_core_news_sm")
#
# def lire_et_nettoyer_srt(chemin_fichier, langue):
#     if langue == "VO":
#         nlp = nlp_en
#     else:
#         nlp = nlp_fr
#
#     with open(chemin_fichier, 'r', encoding='utf-8', errors='ignore') as f:
#         data = f.read()
#
#     data = re.sub(r'\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', data)
#     data = re.sub(r'<.*?>', '', data)
#
#     doc = nlp(data)
#     mots = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
#     return mots
#
# def generer_index_inversé(chemin_racine):
#     index = {}
#
#     for lang_dir in ["VF", "VO"]:
#         lang_path = os.path.join(chemin_racine, lang_dir)
#         series = os.listdir(lang_path)
#         total_series = len(series)
#
#         for idx, serie in enumerate(series):
#             print(f"Traitement de {serie} ({lang_dir}) ... ({idx+1}/{total_series})")
#             serie_path = os.path.join(lang_path, serie)
#             if os.path.isdir(serie_path):
#                 for file in os.listdir(serie_path):
#                     if file.lower().endswith(".txt"):
#                         chemin_fichier = os.path.join(serie_path, file)
#                         mots = lire_et_nettoyer_srt(chemin_fichier, lang_dir)
#
#                         for mot in mots:
#                             if mot not in index:
#                                 index[mot] = {"document_frequency": 0, "documents": {}}
#                             if serie not in index[mot]["documents"]:
#                                 index[mot]["documents"][serie] = {"term_frequency": 0}
#                                 index[mot]["document_frequency"] += 1
#                             index[mot]["documents"][serie]["term_frequency"] += 1
#
#     return index
#
# chemin_racine = "./sous-titres"
# index = generer_index_inversé(chemin_racine)
#
# with open('index_inversé.json', 'w', encoding='utf-8') as json_f:
#     json.dump(index, json_f, ensure_ascii=False, indent=4)
# print("Indexation terminée !")

# Pour le traitement des mots et la tokenisation TEST 20 series
# import os
# import json
# import re
# import spacy
# import chardet
#
# nlp_en = spacy.load("en_core_web_sm")
# nlp_fr = spacy.load("fr_core_news_sm")
#
#
# def lire_et_nettoyer_srt(chemin_fichier, langue):
#     if langue == "VO":
#         nlp = nlp_en
#     else:
#         nlp = nlp_fr
#
#     with open(chemin_fichier, 'rb') as f:
#         rawdata = f.read()
#         result = chardet.detect(rawdata)
#         encoding = result['encoding']
#
#     with open(chemin_fichier, 'r', encoding=encoding, errors='ignore') as f:
#         data = f.read()
#
#     # Nettoyer le texte
#     data = re.sub(r'\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', data)
#     data = re.sub(r'<.*?>', '', data)
#
#     # Tokenize et filtrer
#     doc = nlp(data)
#     mots = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
#
#     return mots
#
#
# def generer_index_inversé(chemin_racine, max_series=3):
#     index = {}
#
#     for lang_dir in ["VF", "VO"]:
#         lang_path = os.path.join(chemin_racine, lang_dir)
#         series = os.listdir(lang_path)[:max_series]  # Limiter à max_series séries pour les tests
#         total_series = len(series)
#
#         for idx, serie in enumerate(series):
#             print(f"Traitement de {serie} ({lang_dir}) ... ({idx + 1}/{total_series})")
#             serie_path = os.path.join(lang_path, serie)
#             if os.path.isdir(serie_path):
#                 for file in os.listdir(serie_path):
#                     if file.lower().endswith(".txt"):
#                         chemin_fichier = os.path.join(serie_path, file)
#                         mots = lire_et_nettoyer_srt(chemin_fichier, lang_dir)
#
#                         for mot in mots:
#                             if mot not in index:
#                                 index[mot] = {"document_frequency": 0, "documents": {}}
#                             if serie not in index[mot]["documents"]:
#                                 index[mot]["documents"][serie] = {"term_frequency": 0}
#                                 index[mot]["document_frequency"] += 1
#                             index[mot]["documents"][serie]["term_frequency"] += 1
#
#     return index
#
#
# chemin_racine = "./sous-titres"
# index = generer_index_inversé(chemin_racine)
#
# with open('index_inversé.json', 'w', encoding='utf-8') as json_f:
#     json.dump(index, json_f, ensure_ascii=False, indent=4)
# print("Indexation terminée !")

# Traitement des mots et la tokenisation TEST series définies
#
# import os
# import json
# import re
# import spacy
# import chardet
# import random
#
# nlp_en = spacy.load("en_core_web_sm")
# nlp_fr = spacy.load("fr_core_news_sm")
#
#
# def lire_et_nettoyer_srt(chemin_fichier, langue):
#     if langue == "VO":
#         nlp = nlp_en
#     else:
#         nlp = nlp_fr
#
#     with open(chemin_fichier, 'rb') as f:
#         rawdata = f.read()
#         result = chardet.detect(rawdata)
#         encoding = result['encoding']
#
#     with open(chemin_fichier, 'r', encoding=encoding, errors='ignore') as f:
#         data = f.read()
#
#     # Nettoyer le texte
#     data = re.sub(r'\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', data)
#     data = re.sub(r'<.*?>', '', data)
#
#     # Tokenize et filtrer
#     doc = nlp(data)
#     mots = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
#
#     return mots
#
#
# def generer_index_inversé(chemin_racine, max_series=6):
#     index = []
#
#     always_include = ["friends", "breaking bad", "south park"]
#
#     all_series = []
#     for lang_dir in ["VF", "VO"]:
#         lang_path = os.path.join(chemin_racine, lang_dir)
#         all_series.extend(os.listdir(lang_path))
#
#     # Exclude always include series from all_series
#     remaining_series = [serie for serie in all_series if serie.lower() not in always_include]
#
#     # Randomly choose 3 series
#     random_chosen = random.sample(remaining_series, 3)
#
#     series_to_index = always_include + random_chosen
#
#     for lang_dir in ["VF", "VO"]:
#         lang_path = os.path.join(chemin_racine, lang_dir)
#
#         for idx, serie in enumerate(series_to_index):
#             if serie in os.listdir(lang_path):  # Make sure the serie exists in the current language folder
#                 print(f"Traitement de {serie} ({lang_dir}) ... ({idx + 1}/{max_series})")
#                 serie_path = os.path.join(lang_path, serie)
#                 if os.path.isdir(serie_path):
#                     for file in os.listdir(serie_path):
#                         if file.lower().endswith(".txt"):
#                             chemin_fichier = os.path.join(serie_path, file)
#                             mots = lire_et_nettoyer_srt(chemin_fichier, lang_dir)
#
#                             for mot in mots:
#                                 entry = next((item for item in index if item["_id"] == mot), None)
#
#                                 if not entry:
#                                     entry = {
#                                         "_id": mot,
#                                         "document_frequency": 1,
#                                         "documents": {serie: 1}
#                                     }
#                                     index.append(entry)
#                                 else:
#                                     if serie in entry["documents"]:
#                                         entry["documents"][serie] += 1
#                                     else:
#                                         entry["documents"][serie] = 1
#                                         entry["document_frequency"] += 1
#
#     return index
#
#
# chemin_racine = "./sous-titres"
# index = generer_index_inversé(chemin_racine)
#
# with open('index_inversé_MongoDB.json', 'w', encoding='utf-8') as json_f:
#     json.dump(index, json_f, ensure_ascii=False, indent=4)
# print("Indexation terminée !")

# Traitement des mots et la tokenisation de toutes les séries (trop long)
# import os
# import json
# import re
# import spacy
# import chardet
# import time
#
# nlp_en = spacy.load("en_core_web_sm")
# nlp_fr = spacy.load("fr_core_news_sm")
#
#
# def lire_et_nettoyer_srt(chemin_fichier, langue):
#     if langue == "VO":
#         nlp = nlp_en
#     else:
#         nlp = nlp_fr
#
#     with open(chemin_fichier, 'rb') as f:
#         rawdata = f.read()
#         result = chardet.detect(rawdata)
#         encoding = result['encoding']
#
#     with open(chemin_fichier, 'r', encoding=encoding, errors='ignore') as f:
#         data = f.read()
#
#     # Nettoyer le texte
#     data = re.sub(r'\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', data)
#     data = re.sub(r'<.*?>', '', data)
#
#     # Tokenize et filtrer
#     doc = nlp(data)
#     mots = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
#
#     return mots
#
#
# def generer_index_inversé(chemin_racine):
#     index = []
#
#     for lang_dir in ["VF", "VO"]:
#         lang_path = os.path.join(chemin_racine, lang_dir)
#         series_list = os.listdir(lang_path)
#
#         for idx, serie in enumerate(series_list):
#             print(f"Traitement de {serie} ({lang_dir}) ... ({idx + 1}/{len(series_list)})")
#             serie_path = os.path.join(lang_path, serie)
#             if os.path.isdir(serie_path):
#                 for file in os.listdir(serie_path):
#                     if file.lower().endswith(".txt"):
#                         chemin_fichier = os.path.join(serie_path, file)
#                         mots = lire_et_nettoyer_srt(chemin_fichier, lang_dir)
#
#                         for mot in mots:
#                             entry = next((item for item in index if item["_id"] == mot), None)
#
#                             if not entry:
#                                 entry = {
#                                     "_id": mot,
#                                     "document_frequency": 1,
#                                     "documents": {serie: 1}
#                                 }
#                                 index.append(entry)
#                             else:
#                                 if serie in entry["documents"]:
#                                     entry["documents"][serie] += 1
#                                 else:
#                                     entry["documents"][serie] = 1
#                                     entry["document_frequency"] += 1
#
#     return index
#
#
# start_time = time.time()
#
# chemin_racine = "./sous-titres"
# index = generer_index_inversé(chemin_racine)
#
# with open('index_inversé_MongoDB.json', 'w', encoding='utf-8') as json_f:
#     json.dump(index, json_f, ensure_ascii=False, indent=4)
#
# end_time = time.time()
#
# print(f"Indexation terminée en {end_time - start_time:.2f} secondes!")

import os
import json
import re
import spacy
import chardet
import time
from langdetect import detect
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor

nlp_en = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")


def detect_language(text):
    try:
        return detect(text)
    except:
        return None


def lire_et_nettoyer_series(chemin_fichier):
    with open(chemin_fichier, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

    with open(chemin_fichier, 'r', encoding=encoding, errors='ignore') as f:
        data = f.read()

    detected_language = detect_language(data)
    if detected_language == "en":
        nlp = nlp_en
    elif detected_language == "fr":
        nlp = nlp_fr
    else:
        return []

    # Nettoyer le texte avec une seule regex
    data = re.sub(r'\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n|<.*?>', '', data)

    doc = nlp(data)
    mots = [token.text.lower() for token in doc if
            token.is_alpha and not token.is_stop and token.pos_ in ["NOUN", "PROPN", "VERB"] and len(token.text) > 2]

    return mots


def process_serie(args):
    serie, serie_files, lang_dir = args
    print(f"Début du traitement de la série {serie} en {lang_dir}.")

    all_mots = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lire_et_nettoyer_series, serie_files))
    for mots in results:
        all_mots.extend(mots)

    print(f"Fin du traitement de la série {serie} en {lang_dir}.")
    return serie, all_mots


def generer_index_inverse(chemin_racine):
    index = defaultdict(lambda: {'document_frequency': 0, 'documents': defaultdict(int)})

    tasks = []

    for lang_dir in ["VF", "VO"]:
        lang_path = os.path.join(chemin_racine, lang_dir)

        # Liste toutes les séries (sans filtrage spécifique)
        series_list = os.listdir(lang_path)

        for serie in series_list:
            serie_path = os.path.join(lang_path, serie)
            serie_files = [os.path.join(serie_path, file) for file in os.listdir(serie_path) if
                           file.lower().endswith(".txt")]

            if serie_files:  # Ajoutez uniquement si la série contient des fichiers
                tasks.append((serie, serie_files, lang_dir))

    with ThreadPoolExecutor(max_workers=4) as executor:
        for serie, mots in executor.map(process_serie, tasks):
            word_counts = Counter(mots)
            for mot, count in word_counts.items():
                index_entry = index[mot]  # Référencez directement pour réduire les accès répétés
                if serie not in index_entry['documents']:
                    index_entry['document_frequency'] += 1
                index_entry['documents'][serie] += count

    return [{**{"_id": key}, **value} for key, value in index.items()]


start_time = time.time()

chemin_racine = "./sous-titres"
index = generer_index_inverse(chemin_racine)

with open('index_inversé_MongoDB_TEST.json', 'w', encoding='utf-8') as json_f:
    json.dump(index, json_f, ensure_ascii=False, indent=4)

end_time = time.time()

print(f"Indexation terminée en {end_time - start_time:.2f} secondes!")
