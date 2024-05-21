# External
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import mysql.connector
import pprint
import time
import csv
import sys
import os

# doenv
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), ".env"))


def dd(*args):
    for arg in args:
        pprint.pprint(arg)
        print("-" * 40)
    sys.exit()


def has_transparent_background_from_url(image_url):
    try:
        # Télécharger l'image depuis l'URL
        response = requests.get(image_url)
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)

        # Vérifier si l'image a un fond transparent
        if image.mode == "RGBA":
            transparent_pixels = [p for p in image.getdata() if p[3] < 255]
            if transparent_pixels:
                return True
        return False
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement de l'image : {e}")
        return False


def recuperer_donnees_bdd_distante(env, requete_sql, data_sql):
    try:
        if env == "prod":
            connexion = mysql.connector.connect(
                host=os.environ.get("PROD_HOST"),
                user=os.environ.get("PROD_USER"),
                password=os.environ.get("PROD_PASSWORD"),
                database=os.environ.get("PROD_DATABASES"),
            )
        if env == "dev":
            connexion = mysql.connector.connect(
                host=os.environ.get("DEV_HOST"),
                user=os.environ.get("DEV_USER"),
                password=os.environ.get("DEV_PASSWORD"),
                database=os.environ.get("DEV_DATABASES"),
            )
        if env == "local":
            connexion = mysql.connector.connect(
                host=os.environ.get("LOCAL_HOST"),
                user=os.environ.get("LOCAL_USER"),
                password=os.environ.get("LOCAL_PASSWORD"),
                database=os.environ.get("LOCAL_DATABASES"),
            )

        curseur = connexion.cursor()
        print("[DATABASE] Connexion à la base de données ouverte en " + env)
        curseur.execute(requete_sql, data_sql)
        print("[DATABASE] Requête executée.")
        resultats = curseur.fetchall()

        return resultats

    except mysql.connector.Error as erreur:
        print("[DATABASE] Erreur lors de la récupération des données:", erreur)

    finally:
        if "connexion" in locals() and connexion.is_connected():
            curseur.close()
            connexion.close()
            print("[DATABASE] Connexion à la base de données fermée.")


def is_log_for_store(env, store):
    directoryLog = get_directory_log(env)
    nameLog = get_log_name(store)

    if os.path.exists("./logs") is not True:
        os.mkdir("./logs")

    if os.path.exists(directoryLog) is not True:
        os.mkdir("./logs/" + env)

    if os.path.exists(directoryLog + "/" + nameLog):
        # Load file
        result = read_file(directoryLog + "/" + nameLog)
    else:
        # create file
        header = ["entity_id"]
        create_file(directoryLog + "/" + nameLog)
        append_file(directoryLog + "/" + nameLog, header)
        result = ""

    return result


def is_output_for_store(env, store, type):
    directoryOutput = get_directory_output(env)
    nameOutput = get_file_output(store, type)

    if os.path.exists("./output") is not True:
        os.mkdir("./output")

    if os.path.exists(directoryOutput) is not True:
        os.mkdir("./output/" + env)

    if os.path.exists(directoryOutput + "/" + nameOutput):
        # Load file
        result = read_file(directoryOutput + "/" + nameOutput)
    else:
        # create file
        header = ["entity_id", "error_type"]
        create_file(directoryOutput + "/" + nameOutput)
        append_file(directoryOutput + "/" + nameOutput, header)
        result = ""

    return result


def get_directory_log(env):
    return "./logs/" + env


def get_log_extention():
    return ".csv"


def get_log_name(store):
    return "log_" + str(store[0]) + "_" + str(store[1]) + get_log_extention()


def get_directory_output(env):
    return "./output/" + env


def get_file_output(store, type):
    if type == 0:
        resultat = (
            "Resultat_KPUT_error_"
            + str(store[0])
            + "_"
            + str(store[1])
            + get_log_extention()
        )
    if type == 1:
        resultat = (
            "Resultat_KPUT_3_columns_"
            + str(store[0])
            + "_"
            + str(store[1])
            + get_log_extention()
        )
    if type == 2:
        resultat = (
            "Resultat_KPUT_translucent_"
            + str(store[0])
            + "_"
            + str(store[1])
            + get_log_extention()
        )

    return resultat


def read_file(file_name):
    result = []
    with open(file_name, "r", newline="") as fichier_csv:
        lecteur_csv = csv.reader(fichier_csv)
        for ligne in lecteur_csv:
            result.append(ligne)

    return result


def append_file(file_name, data_array):
    with open(file_name, "a", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(data_array)


def create_file(file_name):
    open(file_name, "w").close()


def update_log_by_store(env, store, commande):
    directoryLog = get_directory_log(env)
    nameLog = get_log_name(store)

    append_file(directoryLog + "/" + nameLog, [commande[0]])


def worker(env, store, i, tabs_uri):

    try:
        num = str(store[0])
        name = str(store[1])
        domain = "https://" + str(store[4]) + "/"

        print(f"Process {num}_{name}_{i} : Wake Up")

        # Chrome
        # options = ChromeOptions()

        # Firefox
        options = FirefoxOptions()

        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        # options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=CSSStyleSheet")

        # Chrome
        # driver = webdriver.Chrome(options=options)

        # Firefox
        driver = webdriver.Firefox(options=options)

        driver.get(domain)
        time.sleep(0.8)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "html-body"))
        )

        for uri in tabs_uri:
            try:
                entity_id = str(uri[0])
                entity_uri = str(uri[1])

                driver.get(domain + entity_uri)
                time.sleep(0.8)

                is_cms404 = True
                is_3_columns = True
                is_translucent = True
                is_error = True

                # PAGE LOADED
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "html-body"))
                    )
                except Exception as e:
                    print(
                        f"Process {num}_{name}_{i} : Une erreur sur {entity_id} - {e}"
                    )

                # CMS 404 - not redirected
                try:
                    cms404_text = driver.find_element(
                        By.CSS_SELECTOR,
                        "#maincontent div.column.main",
                    ).text
                    if cms404_text != "There was no 404 CMS page configured or found.":
                        is_cms404 = False
                except NoSuchElementException:
                    is_cms404 = False

                # 404 - redirected
                try:
                    error_text = driver.find_element(
                        By.CSS_SELECTOR,
                        "#maincontent div.column.main h1 span",
                    ).text
                    if error_text != "OUPS petite erreur 404":
                        is_error = False
                except NoSuchElementException:
                    is_error = False

                if is_cms404 == False or is_error == False:
                    # 3 COLUMNS
                    try:
                        driver.find_element(
                            By.CSS_SELECTOR,
                            "body.catalog-product-view.page-layout-3columns",
                        )
                    except NoSuchElementException:
                        is_3_columns = False
                    # TRANSLUCENT
                    try:
                        imgs = driver.find_elements(
                            By.CSS_SELECTOR,
                            "#maincontent div.column.main div.product.media div.gallery-placeholder div.fotorama__stage__frame.fotorama_vertical_ratio.fotorama__loaded.fotorama__loaded--img",
                        )
                        tab_translucent = []
                        for img in imgs:
                            href = img.get_attribute("href")
                            tab_translucent.append(
                                has_transparent_background_from_url(href)
                            )
                        if all(not elem for elem in tab_translucent):
                            is_translucent = False
                    except NoSuchElementException:
                        is_translucent = False
            except Exception as e:
                print(f"Process {num}_{name}_{i} : Une erreur sur {entity_id} - {e}")
            finally:
                if is_cms404 == True or is_error == True:
                    type_error = (
                        "The product is KPUT, 404 (diabled, not visible, other)"
                    )
                    is_output_for_store(env, store, 0)
                    append_file(
                        get_directory_output(env) + "/" + get_file_output(store, 0),
                        [entity_id, type_error],
                    )
                    message = " should be KPUT by 404 (diabled, not visible, other)"
                else:
                    if is_3_columns == False and is_translucent == False:
                        message = " should be OK"
                    if is_3_columns == True:
                        type_error = "The product has three columns"
                        is_output_for_store(env, store, 1)
                        append_file(
                            get_directory_output(env) + "/" + get_file_output(store, 1),
                            [entity_id, type_error],
                        )
                        message = " should be KPUT by 3 columns"
                    if is_translucent == True:
                        type_error = "The product has a translucent background image"
                        is_output_for_store(env, store, 2)
                        append_file(
                            get_directory_output(env) + "/" + get_file_output(store, 2),
                            [entity_id, type_error],
                        )
                        message = " should be KPUT by translucent image"

                print(f"Process {num}_{name}_{i} : " + str(entity_id) + message)
                update_log_by_store(env, store, uri)

        driver.quit()
    except Exception as e:
        print(f"Process {num}_{name}_{i} : Une erreur - {e}")
