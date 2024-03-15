import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go


def affiche(recherche: str, ville: str, category=None, mode=1):
    # Chargement des données
    csv_file_name = os.path.join("data_search", f"{recherche}-{ville}-search-LBC.csv")
    data = pd.read_csv(csv_file_name)

    data["first_publication_date"] = pd.to_datetime(
        data["first_publication_date"], format="%Y-%m-%d %H:%M:%S"
    )

    if category in [8, 9, 10, 11, 12, 13]:
        x_name = "surface_hab"
    elif category in [1, 2, 3, 4, 5]:
        x_name = "kilometrage"
    else:
        x_name = "first_publication_date"

    if mode == 1:  # option pas trop mal
        fig = px.scatter(
            data,
            x=x_name,
            y="price",
            color="distance",
            labels={
                "surface_hab": "Surface habitable",
                "price": "Prix",
                "first_publication_date": "Date de publication",
                "kilometrage": "Kilometrage",
            },
            hover_data={"subject": True, "url": True},
            trendline="ols",
            trendline_scope="overall",
            trendline_color_override="black",
        )
        # Affichage du graphique
        fig.show()


if __name__ == "__main__":
    # affiche('maison', 'rennes', category= "logement",mode=4)
    affiche("z650", "rennes", category="véhicule", mode=1)
