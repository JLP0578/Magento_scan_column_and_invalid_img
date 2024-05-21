# External
from os.path import join, dirname
from dotenv import load_dotenv
import os
import csv

# doenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), ".env"))


# Internal
import outils


def get_store_to_parse(env, store_selected):
    #  TODO: Bug: quand il y a plusieurs store seule le premier est retourné par la requete alors que quand on l'execute en bdd il y a biens tout les stores demandé
    if store_selected == "0":
        query = (
            "SELECT store_id, store.code, store.name, store.website_id, store_website.name as domaine"
            + " FROM store"
            + " INNER JOIN store_website on store.website_id = store_website.website_id"
            + " WHERE store_id NOT IN (%s)"
        )
        data = str(os.environ.get("EXCLUDE_STORE"))
    else:
        query = (
            "SELECT store_id, store.code, store.name, store.website_id, store_website.name as domaine"
            + " FROM store"
            + " INNER JOIN store_website on store.website_id = store_website.website_id"
            + " WHERE store_id NOT IN (%s) AND store_id IN (%s)"
        )
        data = (str(os.environ.get("EXCLUDE_STORE")), str(store_selected))

    datas = outils.recuperer_donnees_bdd_distante(env, query, data)

    return datas


def get_treated_elements(env, store):
    log_datas = outils.is_log_for_store(env, store)
    if log_datas == "":
        pack_1000 = []
    else:
        directoryLog = outils.get_directory_log(env)
        nameLog = outils.get_log_name(store)
        datas = outils.read_file(directoryLog + "/" + nameLog)
        if isinstance(datas, list) and len(datas) == 1 and datas[0][0] == "entity_id":
            pack_1000 = []
        else:
            # Récupérer tous les éléments de la colonne 'entity_id'
            pack_1000 = [row[0] for row in datas]

    return pack_1000


def get_uri_from_store(env, store_selected, treated):
    if len(treated) == 0:
        requete = (
            "SELECT cpe.entity_id, MIN(ur.request_path) as request_path, COUNT(*)"
            + " FROM catalog_product_entity cpe"
            + " INNER JOIN url_rewrite ur on cpe.entity_id = ur.entity_id"
            + ' WHERE ur.entity_type = "product"'
            + " AND ur.store_id NOT IN (%s)"
            + " AND ur.store_id IN (%s)"
            + " AND cpe.entity_id NOT IN (SELECT child_id FROM catalog_product_relation)"
            + " AND ur.request_path not like %s"
            + " AND cpe.type_id != 'grouped'"
            + " GROUP BY cpe.entity_id"
            + " ORDER BY cpe.entity_id"
        )
        data = (
            str(os.environ.get("EXCLUDE_STORE")),
            str(store_selected[0]),
            f"%{str(os.environ.get("EXCLUDE_URI"))}%"
        )
    else:
        requete = (
            "SELECT cpe.entity_id, MIN(ur.request_path) as request_path, COUNT(*)"
            + " FROM catalog_product_entity cpe"
            + " INNER JOIN url_rewrite ur on cpe.entity_id = ur.entity_id"
            + ' WHERE ur.entity_type = "product"'
            + " AND cpe.entity_id NOT IN (%s)"
            + " AND ur.store_id NOT IN (%s)"
            + " AND ur.store_id IN (%s)"
            + " AND cpe.entity_id NOT IN (SELECT child_id FROM catalog_product_relation)"
            + " AND ur.request_path not like %s"
            + " AND cpe.type_id != 'grouped'"
            + " GROUP BY cpe.entity_id"
            + " ORDER BY cpe.entity_id"
        )
        data = (
            ", ".join(treated),
            str(os.environ.get("EXCLUDE_STORE")),
            str(store_selected[0]),
            f"%{str(os.environ.get("EXCLUDE_URI"))}%",
        )
        

    datas = outils.recuperer_donnees_bdd_distante(env, requete, data)

    return datas


def split_array_equally(arr, nb_part):
    # Calculer la taille de chaque partie
    part_size = len(arr) // nb_part
    remainder = len(arr) % nb_part  # Nombre d'éléments restants

    # Initialiser une liste pour stocker les parties
    parts = []

    # Diviser le tableau en parties
    start_index = 0
    for i in range(nb_part):
        # Calculer la taille de la partie en fonction de la division équitable
        size = part_size + (1 if i < remainder else 0)
        # Ajouter la partie au tableau
        parts.append(arr[start_index : start_index + size])
        start_index += size

    return parts
