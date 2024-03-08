import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from serivces.serviceScrapping import scrapping
from serivces.serviceTraitement import traitement
from serivces.serviceAffichage import affiche

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
        self.choix_categorie = ttk.Combobox(cadre, values=["Logement", "Véhicule"], width=27)
        self.choix_categorie.current(0)  # Sélection par défaut
        self.choix_categorie.grid(row=2, column=1, padx=5, pady=5)

        # Bouton de recherche
        bouton_rechercher = ttk.Button(cadre, text="Rechercher", command=self.rechercher)
        bouton_rechercher.grid(row=3, column=0, columnspan=2, pady=10)

    def rechercher(self):
        recherche = self.entry_search.get().lower()
        ville = self.entry_ville.get().lower()


        print(f"Recherche en cours avec le terme '{recherche}' dans la ville '{ville}'")

        scrapping(recherche, ville )
        traitement(recherche , ville)
        affiche(recherche, ville)
        # self.afficher_regression_lineaire()

    def afficher_regression_lineaire(self):
        # Génération de fausses données pour la démonstration
        np.random.seed(0)
        superficie = np.random.randint(50, 200, 100)
        prix = 50 + 2.5 * superficie + np.random.normal(0, 20, 100)

        # Calcul de la régression linéaire
        coef = np.polyfit(superficie, prix, 1)
        poly1d_fn = np.poly1d(coef)

        # Tracé de la régression linéaire
        fig = plt.figure(figsize=(6, 4), dpi=100)
        plt.plot(superficie, prix, 'bo', label='Données', picker=5)  # Activer la sélection des points avec un rayon de 5 pixels
        plt.plot(superficie, poly1d_fn(superficie), 'r-', label='Régression linéaire')
        plt.xlabel('Superficie')
        plt.ylabel('Prix')
        plt.title('Régression linéaire : Prix en fonction de la superficie')
        plt.legend()
        plt.grid(True)
        

        # Connexion de la fonction on_pick à l'événement de sélection de point
        fig.canvas.mpl_connect('pick_event', self.on_pick)
        plt.show()

    def on_pick(self, event):
        artist = event.artist
        xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
        x, y = artist.get_xdata(), artist.get_ydata()
        ind = event.ind
        print('Artist picked:', event.artist)
        print('{} vertices picked'.format(len(ind)))
        print('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
        print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
        print('Data point:', x[ind[0]], y[ind[0]])
        print()

if __name__ == "__main__":
    print('ayo')
    app = FenetreRecherche()
    app.mainloop()
