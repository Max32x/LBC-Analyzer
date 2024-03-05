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



def traitement(recherche, ville):

    json_file_name = os.path.join("data_search", f"{recherche}-{ville}-search-LBC.json")
    
    df = pd.read_json(json_file_name)


    def extract_value(row, key):
        for dico in row["attributes"]:
            if dico["key"] == key:
                return dico["value"]
        return None  # If the key is not found,     return None or another default value

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

    csv_file_name = os.path.join("data_search", f"{recherche}-{ville}-search-LBC.csv")


    df.to_csv (csv_file_name, index = None)

    print("Traitement fini")
