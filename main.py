import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def afficher_regression_lineaire():
    # Génération de fausses données pour la démonstration
    np.random.seed(0)
    superficie = np.random.randint(50, 200, 100)
    prix = 50 + 2.5 * superficie + np.random.normal(0, 20, 100)

    # Calcul de la régression linéaire
    coef = np.polyfit(superficie, prix, 1)
    poly1d_fn = np.poly1d(coef)

    # Tracé de la régression linéaire
    fig = plt.figure(figsize=(6, 4), dpi=100)
    plt.plot(superficie, prix, 'bo', label='Données')
    plt.plot(superficie, poly1d_fn(superficie), 'r-', label='Régression linéaire')
    plt.xlabel('Superficie')
    plt.ylabel('Prix')
    plt.title('Régression linéaire : Prix en fonction de la superficie')
    plt.legend()
    plt.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

def rechercher():
    recherche = entry.get()
    ville = entry_ville.get()
    categorie = choix_categorie.get()
    # Insérer ici le code pour effectuer la recherche en fonction de la catégorie sélectionnée, la ville et le terme recherché
    print(f"Recherche en cours dans la catégorie '{categorie}' avec le terme '{recherche}' dans la ville '{ville}'")
    # Appel de la fonction pour afficher la régression linéaire
    afficher_regression_lineaire()

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Recherche")

# Cadre pour organiser les widgets
cadre = ttk.Frame(fenetre, padding="10")
cadre.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Barre de recherche
label_recherche = ttk.Label(cadre, text="Rechercher :")
label_recherche.grid(row=0, column=0, padx=5, pady=5)
entry = ttk.Entry(cadre, width=30)
entry.grid(row=0, column=1, padx=5, pady=5)

# Barre de recherche pour la ville
label_ville = ttk.Label(cadre, text="Ville :")
label_ville.grid(row=1, column=0, padx=5, pady=5)
entry_ville = ttk.Entry(cadre, width=30)
entry_ville.grid(row=1, column=1, padx=5, pady=5)

# Sélecteur de catégorie
label_categorie = ttk.Label(cadre, text="Catégorie :")
label_categorie.grid(row=2, column=0, padx=5, pady=5)
choix_categorie = ttk.Combobox(cadre, values=["Logement", "Véhicule"], width=27)
choix_categorie.current(0)  # Sélection par défaut
choix_categorie.grid(row=2, column=1, padx=5, pady=5)

# Bouton de recherche
bouton_rechercher = ttk.Button(cadre, text="Rechercher", command=rechercher)
bouton_rechercher.grid(row=3, column=0, columnspan=2, pady=10)

# Lancement de la boucle principale
fenetre.mainloop()
