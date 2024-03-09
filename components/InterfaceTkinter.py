import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from serivces.serviceScrapping import scrapping
from serivces.serviceTraitement import traitement
from serivces.serviceAffichage import affiche
from serivces.serviceVille import verif,zip_coordonnees

class FenetreRecherche(tk.Tk):
    def __init__(self):
        super().__init__()

        # Création de la fenêtre principale
        self.title("LBC Analyzer")

        # Cadre pour organiser les widgets
        cadre = ttk.Frame(self, padding="10")
        cadre.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Barre de recherche
        self.label_recherche = ttk.Label(cadre, text="Rechercher :")
        self.label_recherche.grid(row=0, column=0, padx=5, pady=5)
        self.entry_search = ttk.Entry(cadre, width=30)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)

        # Barre de recherche pour la ville
        label_ville = ttk.Label(cadre, text="Ville :")
        label_ville.grid(row=1, column=0, padx=5, pady=5)
        self.entry_ville = ttk.Entry(cadre, width=30)
        self.entry_ville.grid(row=1, column=1, padx=5, pady=5)

        # Sélecteur de catégorie
        label_categorie = ttk.Label(cadre, text="Catégorie :")
        label_categorie.grid(row=2, column=0, padx=5, pady=5)
        self.choix_categorie = ttk.Combobox(cadre, values=["Logement", "Véhicule", "Aucune"], width=27)
        self.choix_categorie.current(0)  # Sélection par défaut
        self.choix_categorie.grid(row=2, column=1, padx=5, pady=5)

        # **New Slider**
        self.label_prix = ttk.Label(cadre, text="Rayon :")
        self.label_prix.grid(row=3, column=0, padx=5, pady=5)
        self.rayon_slider = ttk.Scale(cadre, from_=0, to=200, orient=tk.HORIZONTAL)
        self.rayon_slider.set(20) #Vaaleur par defaut
        self.rayon_slider.grid(row=3, column=1, padx=5, pady=5)

        # Bouton de recherche
        bouton_rechercher = ttk.Button(cadre, text="Rechercher", command=self.rechercher)
        bouton_rechercher.grid(row=4, column=0, columnspan=2, pady=10)

    def rechercher(self):
        recherche = self.entry_search.get().lower()
        ville = self.entry_ville.get().lower()
        choix_categorie= self.choix_categorie.get().lower()
        rayon = int(self.rayon_slider.get()*1000)

        # Verifier si ville en base de données et 
        # Recuperer les coordonnées GPS
        if verif(ville):
            print(f"Recherche en cours avec le terme '{recherche}' dans la ville '{ville}' dans la categorie '{choix_categorie}'")

            zip_code, latitude, longitude = zip_coordonnees(ville)
            scrapping(recherche, ville, category=choix_categorie, zip_code=zip_code, rayon= rayon, latitude=latitude, longitude=longitude)
            traitement(recherche , ville, latitude, longitude)
            affiche(recherche, ville, category=choix_categorie)

        elif ville == "" :
            print(f"Recherche en cours avec le terme '{recherche}' dans toute la France dans la categorie '{choix_categorie}'")

            scrapping(recherche, ville, category=choix_categorie, zip_code="", rayon= "", latitude="", longitude="")
            traitement(recherche , ville, latitude="", longitude="")
            affiche(recherche, ville, choix_categorie)

        else : 
            print("Nom de la ville non reconnu")



if __name__ == "__main__":
    app = FenetreRecherche()
    app.mainloop()
