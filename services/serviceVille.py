import os

import pandas as pd


def verif(ville):
    csv_file_name = os.path.join("data", "cities.csv")
    data = pd.read_csv(csv_file_name)

    return ville in data["label"].values


def zip_coordonnees(ville):
    csv_file_name = os.path.join("data", "cities.csv")
    data = pd.read_csv(csv_file_name)
    row = data.loc[data["label"] == ville]
    return (
        row["zip_code"].tolist()[0],
        row["latitude"].tolist()[0],
        row["longitude"].tolist()[0],
    )
