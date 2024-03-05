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

HEADLESS_MODE = True      
JSON_FILE = "search-leboncoin.json"
SEARCH_TERM = "maison"
VERBOSE = False

new_directory = "C:\Maxime\Informatique perso\scrapping sites annonce"
os.chdir(new_directory)

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


def traitement():
    df = pd.read_json(JSON_FILE)


    def extract_value(row, key):
        for dico in row["attributes"]:
            if dico["key"] == key:
                return dico["value"]
        return None  # If the key is not found, return None or another default value

    def extract_value2(row, key):
        return row["location"][key]

    # Apply the function to create a new column "surface_hab"
    df["surface_hab"] = df.apply(lambda row: extract_value(row, "square"), axis=1)
    df["surface_tot"] = df.apply(lambda row: extract_value(row, "land_plot_surface"), axis=1)
    df["nb_piece"] = df.apply(lambda row: extract_value(row, "rooms"), axis=1)
    df["nb_chambre"] = df.apply(lambda row: extract_value(row, "bedrooms"), axis=1)
    df["longitude"] = df.apply(lambda row: extract_value2(row, "lng"), axis=1)
    df["latitude"] = df.apply(lambda row: extract_value2(row, "lat"), axis=1)

    nice_coords = (43.7102, 7.26195)
    df["distance"] = df.apply(lambda row: math.sqrt((row["latitude"] - nice_coords[0])**2 + (row["longitude"] - nice_coords[1])**2), axis=1)

    df["price"] =df["price_cents"]/100
    df = df[~df['subject'].str.contains('terrain', case=False)]

    df.to_csv (r'search-leboncoin.csv', index = None)



def affiche(interactif=False):
    # Chargement des données
    data = pd.read_csv("search-leboncoin.csv")

    data['first_publication_date'] = pd.to_datetime(data['first_publication_date'], format="%Y-%m-%d %H:%M:%S")

    # Filtrage des données
    filtered_data = data[(data['surface_hab'] <= 4000) &   
                         (data['price'] > 15000)]

    prix_min =900000
    prix_max =1200000
    surface_min = 0
    surface_max = 280

    # # Ajout de la condition pour le critère
    critere = ((filtered_data['price'] > prix_min) & (filtered_data['price'] < prix_max) & 
            (filtered_data['surface_hab'] > surface_min) & (filtered_data['surface_hab'] < surface_max) )


    if not interactif : 
        # Création du graphique interactif
        fig = px.scatter(filtered_data, x='surface_hab', y='price', color='distance', size=critere.map({True: 0.5, False: 0.01}) , 
                        title='Prix vs Surface habitable',
                        labels={'surface_hab': 'Surface habitable', 'price': 'Prix'}, 
                        hover_data={'subject': True, 'url': True},
                        trendline="ols", trendline_scope="overall", trendline_color_override="black")
        # Affichage du graphique
        fig.show()


    else : 
        print("je suis la ")

        f = go.FigureWidget([go.Scatter(x=filtered_data["surface_hab"], y=filtered_data["price"], mode='markers')])

        help(go.FigureWidget)

        scatter = f.data[0]
        colors = ['#a3a7e4'] * len(filtered_data)
        scatter.marker.color = colors
        # scatter.marker.size = critere.map({True: 2, False: 1})
        f.layout.hovermode = 'closest'

        print('ok')
        def do_click(trace, points, state):
            print('22222222222')
            if points.point_inds:
                ind = points.point_inds[0]
                url = filtered_data.url.iloc[ind]
                webbrowser.open_new_tab(url)

        scatter.on_click(do_click)
        f
        

        from dash import Dash, dcc, html

        app = Dash()

        app.layout = html.Div([
            dcc.Graph(figure=f)
        ])

        # app.run_server(debug=True)  # Turn off reloader if inside Jupyter

                

# lbc(20)
# traitement()

affiche(interactif=True)


