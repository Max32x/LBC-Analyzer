import os
import sys

import json
import pandas as pd

import unittest
from unittest.mock import patch


current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from services.serviceTraitement import traitement
from services.serviceScrapping import scrapping



class TestTraitement(unittest.TestCase):
    def test_traitement(self):
        recherche = ''
        ville = 'paris'
        id_category = ''
        rayon = 0
        nb_pages = 1

        scrapping(recherche, ville, id_category, rayon=rayon, nb_pages=nb_pages)
        traitement(recherche, ville)  

        json_file_name = f"{recherche}-{ville}-search-LBC.json"
        json_path = os.path.join(parent_dir, 'data_search', json_file_name)

        csv_file_name = f"{recherche}-{ville}-search-LBC.csv"
        csv_path = os.path.join(parent_dir, 'data_search', csv_file_name)

        # Vérification des colonnes dans le fichier CSV
        df = pd.read_csv(csv_path)

        expected_columns = ['price', 'surface_hab', 'surface_tot', 'nb_piece', 'nb_chambre', 'kilometrage', 'annee_vehicule', 'longitude', 'latitude', 'distance']
        self.assertTrue(all(col in df.columns for col in expected_columns), "Les colonnes attendues ne sont pas présentes dans le fichier CSV.")

        # Nettoyage après le test
        os.remove(json_path)   
        os.remove(csv_path)

if __name__ == "__main__":
    unittest.main()