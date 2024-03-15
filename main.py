from components.InterfaceTkinter import FenetreRecherche
from tests.testScrapping import TestScrapping


if __name__ == "__main__":

    app = FenetreRecherche()
    app.mainloop() 


#  pyinstaller --onefile main.py
#pip freeze -r requirements.txt | sed '/freeze/,$ d'
