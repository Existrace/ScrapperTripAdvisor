import csv
import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd


def scrap_data(browser):
    """ Fonction permettant de récupérer les informations nécessaire dans un lien """

    # Récupération du nom
    nom = browser.find_element_by_css_selector('.ui_header.h1').text

    # Récupération de l'adresse postale
    adresse = browser.find_element_by_class_name(
        'restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei').text

    # E-mail
    mail = browser.find_element_by_link_text('E-mail').get_attribute("href")
    # Enlève les parties inutiles de l'e-mail extraite
    mail = mail.replace('mailto:', '')
    mail = mail.replace('?subject=?', '')

    # Récupération du numéro de téléphone
    # L'adresse postale et le numéro partage les mêmes class CSS
    # alors j'ai été contraint de prendre le deuxième élement (à surveiller)
    result_num = browser.find_elements_by_class_name('ui_link')
    numero_tel = result_num[1].text

    # Insertion de toutes les données dans une liste
    data_all_array = [
        nom,
        adresse,
        mail,
        numero_tel
    ]

    return data_all_array


"""
----- Configuration -----
"""
# Chemin du driver chrome
path_driver = '/home/snourry/Documents/chromedriver_linux64/chromedriver'

# Configuration du Chrome headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path='/home/snourry/Documents/chromedriver_linux64/chromedriver',
                          options=chrome_options)

# Première page qui sera le point d'ancrage
url = "https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html"

# Execution de la première page
driver.get(url)
time.sleep(2)

"""
----- Récupération des liens de chaque restaurants de chaque page -----
"""
compteur = 1
timeout = 10
path_csv = "/home/snourry/Documents/drive-download-20200106T103458Z-001/linksNotDone.csv"

# Le chemin des liens des restaurants (Susceptile de changer, à surveiller)
# Attention il faut récupérer le href, pas le text
path_link = 'restaurants-list-ListCell__titleRow--3rRCX .restaurants-list-ListCell__restaurantName--2aSdo'

# Cette liste contiendra tous les liens destinés à être retranscrit dans le fichier CSV
fullLinks = []

# Il faut récupérer les liens de la page courange avant de cliquer sur suivant
print("Execution de la page N° 1")
list_links = driver.find_elements_by_class_name(path_link)
print("Nombre de liens récupérés sur la page " + str(compteur) + " : " + str(len(list_links)) + " liens.")
driver.implicitly_wait(10)
for link in list_links:
    fullLinks.append(link.get_attribute("href"))

# Récupération de tous les liens de toutes les pages
is_enable = True
while compteur <= 0:
    try:
        compteur = compteur + 1
        print("Execution de la page N° " + str(compteur))
        time.sleep(2)

        # Recherche de la page suivante grâce à son libellé directement
        next_page = driver.find_element_by_link_text('Suivant')
        WebDriverWait(driver, timeout)
        driver.get(next_page.get_attribute("href"))

        # Récupération des liens des autres pages
        list_links = driver.find_elements_by_class_name(path_link)

        print("Nombre de liens récupérés sur la page " + str(compteur) + " : " + str(len(list_links)) + " liens.")

        for link in list_links:
            fullLinks.append(link.get_attribute("href"))

    except StaleElementReferenceException:
        print("Pas d'autres pages trouvées.")
        is_enable = False
    except NoSuchElementException:
        print("Chemin non trouvé dans la page.")
        is_enable = False
    """
    finally:
        df = pd.DataFrame(fullLinks, columns=['Liens'])
        if df.to_csv(path_csv):
            print('Ecriture dans le fichier CSV')
    """

print("Lecture des pages terminé.")
"""
----- Parcours des liens et récupération des données  -----

Dans cette partie, on parcourt les liens récupérés
en récupérant les informations suivantes : 
- Nom du restaurant
- Adresse postale
- Numéro de téléphone
- E-mail
"""

"""
Idée : Chaque lien lu, il faut le mettre dans le csv. Si une exception est levée, on reprend le fil
du fichier csv
"""

list_all_data = []  # Liste qui va contenir toutes les données finales
print("Récupération des données contenues dans chaque lien...")
# Trouver un moyen pour slice fullLinks en seulement deux liens de restaurant (pour le test)
fullLinks = fullLinks[0:1]

for link in fullLinks:
    driver.get(link)
    time.sleep(3)
    print("Parcours du lien : " + driver.title)
    list_all_data = scrap_data(driver)

for data in list_all_data:
    print(data)

df = pd.DataFrame([list_all_data], columns=['Nom', 'Adresse postale', 'E-mail', 'Numéro'])
if df.to_csv(path_csv):
    print('Ecriture dans le fichier CSV : ' + path_csv)
