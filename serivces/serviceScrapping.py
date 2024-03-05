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




def lbc(max):

    items = list()

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=HEADLESS_MODE,slow_mo=10)
 
        for k in range(1,max+1):

            print(k)
            time.sleep(10)

            page = browser.new_page()
            page.goto(f"https://www.leboncoin.fr/recherche?category=8&text=maison&locations=Nice__43.722754661301785_7.246854356769285_8588_30000&page={k}")
            

            time.sleep(1)

            try:
                time.sleep(2)
                accept_cookies_button = page.locator("button#didomi-notice-agree-button")
                accept_cookies_button.click()

            except :
                pass
        
            try : 
                # Get HTML source code
                html_source_code = page.content()

                # Parsing HTML
                soup = BeautifulSoup(html_source_code, "html.parser")

                
                json_content = soup.find("script", {"type":"application/json"}).text
                datas = json.loads(json_content)
                items += datas["props"]["pageProps"]["searchData"]["ads"]
            except:
                print(f"pass {k}")
                pass

        print(f"Écriture des données dans le fichier : {JSON_FILE}")
        


        print("Fichier enregistré dans :", os.getcwd())
        print("Nombre d'annonces :", len(items))

        with open(JSON_FILE, mode="w") as jsonfile:
            json.dump(items, jsonfile, indent=2)

        browser.close()
