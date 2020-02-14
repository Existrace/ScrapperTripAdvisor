import csv
import logging
import time
import utils
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

"""
Script qui parcours les pages de TripAdvisor
Ce script sera fait plus occasionnellement que le parcours des liens
Enregistre tous les liens récupérés dans un fichier CSV
"""

# Première page qui sera le point d'ancrage
url = "https://www.tripadvisor.fr/Restaurants-g187175-Toulouse_Haute_Garonne_Occitanie.html"

# Récupère la configuration du browser (Chrome headless)
browser = utils.setUp()

# Démarre par la première page du site
browser.get(url)
time.sleep(2)

"""
----- Récupération des liens de chaque restaurants de chaque page -----
"""
nb_page = 1
timeout = 10
path_waitingList = "/home/snourry/Documents/drive-download-20200106T103458Z-001/links_waitinglist.csv"

# Le chemin des liens des restaurants (Susceptile de changer, à surveiller)
# Attention il faut récupérer le href, pas le text
path_link = 'wQjYiB7z'

# Cette liste contiendra tous les liens destinés à être retranscrit dans le fichier CSV
fullLinks = []

try:
    # Il faut récupérer les liens de la page courante avant de cliquer sur suivant
    print("Parcours des pages du site pour récupérer les liens. Démarrage. \n")
    print("Execution de la page N° 1")
    list_links = browser.find_elements_by_class_name(path_link)
    print("Nombre de liens récupérés sur la page " + str(nb_page) + " : " + str(len(list_links)) + " liens. \n")
    browser.implicitly_wait(10)
    for link in list_links:
        fullLinks.append(link.get_attribute("href"))

    # Récupération de tous les liens de toutes les pages
    is_enable = True
    while is_enable:
        nb_page = nb_page + 1
        print("Execution de la page N° " + str(nb_page))
        time.sleep(2)

        # Recherche de la page suivante grâce à son libellé directement
        next_page = browser.find_element_by_link_text('Suivant')
        WebDriverWait(browser, timeout)
        browser.get(next_page.get_attribute("href"))

        # Récupération des liens des autres pages
        list_links = browser.find_elements_by_class_name(path_link)

        print("Nombre de liens récupérés sur la page " + str(nb_page) + " : " + str(len(list_links)) + " liens.")

        for link in list_links:
            fullLinks.append(link.get_attribute("href"))

except StaleElementReferenceException:
    print("Pas d'autres pages trouvées.")
    is_enable = False
except NoSuchElementException:
    print("Chemin non trouvé dans la page.")
    is_enable = False
except Exception as e:
    logging.exception(e)
    is_enable = False
finally:
    is_enable = False
    df = pd.DataFrame(fullLinks)
    df.to_csv(path_waitingList, header=False, index=False)
    print("Ecriture dans le fichier CSV " + path_waitingList)
    print("Nombre de pages parcourues au total : " + str(nb_page))

print("Fin du traitement. Liens totals récupérés : " + str(len(fullLinks)))
