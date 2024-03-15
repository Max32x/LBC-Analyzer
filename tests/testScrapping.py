import os
import sys
import unittest
import json

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from services.serviceScrapping import scrapping

class TestScrapping(unittest.TestCase):
    def test_scrapping(self):
        recherche = ''
        ville = 'rennes'
        id_category = ''
        rayon = 0
        nb_pages = 1

        items = scrapping(recherche, ville, id_category, rayon=rayon, nb_pages=nb_pages)

        # Vérifiez si le résultat est une liste
        self.assertIsInstance(items, list)

        # Vérifiez si la liste n'est pas vide
        self.assertGreater(len(items), 0)

        # Vérifiez si le fichier JSON a été créé
        json_file_name = f"{recherche}-{ville}-search-LBC.json"
        json_path = os.path.join(parent_dir, 'data_search', json_file_name)
        self.assertTrue(os.path.isfile(json_path))

        # Supprimez le fichier JSON créé pendant le test
        os.remove(json_path)

if __name__ == "__main__":
   unittest.main()