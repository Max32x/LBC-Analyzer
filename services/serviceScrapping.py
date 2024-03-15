import json
import os

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scrapping(
    recherche: str,
    ville: str,
    id_category: str = "",
    zip_code: str = "",
    rayon=None,
    latitude="",
    longitude="",
    filtre_bool: bool = False,
    nb_pages: int = 5,
):
    items = list()

    with sync_playwright() as p:
        HEADLESS_MODE = True
        browser = p.firefox.launch(headless=HEADLESS_MODE, slow_mo=10)

        for page_index in range(1, nb_pages + 1):
            print("page : ", page_index)

            page = browser.new_page()

            if id_category == "":
                url = f"https://www.leboncoin.fr/recherche?text={recherche}&locations={ville}_{zip_code}__{latitude}_{longitude}_5000_{rayon}&page={page_index}"
            else:
                url = f"https://www.leboncoin.fr/recherche?category={id_category}&text={recherche}&locations={ville}_{zip_code}__{latitude}_{longitude}_5000_{rayon}&page={page_index}"

            if filtre_bool:
                url += "&search_in=subject"

            page.goto(url)

            print(page)

            try:
                # time.sleep(2)
                accept_cookies_button = page.locator(
                    "button#didomi-notice-agree-button"
                )
                accept_cookies_button.click()
            except:
                pass

            try:
                # Get HTML source code
                html_source_code = page.content()

                # Parsing HTML
                soup = BeautifulSoup(html_source_code, "html.parser")

                json_content = soup.find("script", {"type": "application/json"}).text
                datas = json.loads(json_content)
                items += datas["props"]["pageProps"]["searchData"]["ads"]

            except:
                print(f"La page {page_index} est vide ou bloquée")
                pass

        # Créer le dossier "data_seach" s'il n'existe pas
        data_folder = "data_search"
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Changer le chemin du fichier pour inclure le dossier "data"
        json_file_name = os.path.join(
            data_folder, f"{recherche}-{ville}-search-LBC.json"
        )

        with open(json_file_name, mode="w") as jsonfile:
            json.dump(items, jsonfile, indent=2)

        print("Fichier enregistré dans :", os.path.abspath(json_file_name))
        print("Nombre d'annonces :", len(items))
        browser.close()

        return items
