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

import dash



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
