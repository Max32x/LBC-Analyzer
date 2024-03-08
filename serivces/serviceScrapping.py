import json
from pprint import pprint

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
import pandas as pd
import math
import time 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go

import webbrowser
import numpy as np


def scrapping(recherche, ville, rayon=None, nb_pages=5):
    items = list()

    with sync_playwright() as p:
        HEADLESS_MODE = True
        browser = p.firefox.launch(headless=HEADLESS_MODE, slow_mo=10)

        for page_index in range(1, nb_pages + 1):
            print("page : ",page_index)

            page = browser.new_page()
            page.goto(f"https://www.leboncoin.fr/recherche?text={recherche}&locations={ville}__undefined_undefined_undefined_{rayon}&page={page_index}")

            # time.sleep(1)
            #page.goto(f"https://www.leboncoin.fr/recherche?category=8&text={recherche}&locations={ville}__undefined_undefined_undefined_{rayon}&page={page_index}")

            try:
                # time.sleep(2)
                accept_cookies_button = page.locator("button#didomi-notice-agree-button")
                accept_cookies_button.click()
            except:
                pass

            try:
                # Get HTML source code
                html_source_code = page.content()

                # Parsing HTML
                soup = BeautifulSoup(html_source_code, "html.parser")

                json_content = soup.find("script", {"type": "application/json"}).text
                datas = json.loads(json_content)
                items += datas["props"]["pageProps"]["searchData"]["ads"]

            except:
                print(f"pass {page_index}")
                pass


        # Créer le dossier "data_seach" s'il n'existe pas
        data_folder = "data_search"
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Changer le chemin du fichier pour inclure le dossier "data"
        json_file_name = os.path.join(data_folder, f"{recherche}-{ville}-search-LBC.json")

        print(f"Écriture des données dans le fichier : {json_file_name}")

        with open(json_file_name, mode="w") as jsonfile:
            json.dump(items, jsonfile, indent=2)

        print("Fichier enregistré dans :", os.path.abspath(json_file_name))
        print("Nombre d'annonces :", len(items))
        browser.close()
        




