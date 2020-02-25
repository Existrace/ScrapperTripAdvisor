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

# Après, ce tableau sera rempli par Crawler
urls = [
    "https://www.tripadvisor.fr/Restaurants-g2012251-Calvados_Basse_Normandie_Normandy.html",
    "https://www.tripadvisor.fr/Restaurants-g1880647-Manche_Basse_Normandie_Normandy.html",
    "https://www.tripadvisor.fr/Restaurants-g2005366-Seine_Maritime_Haute_Normandie_Normandy.html",
    "https://www.tripadvisor.fr/Restaurants-g1776023-Orne_Basse_Normandie_Normandy.html",
]

for url in urls:
    print("Execution du lien " + url + ".")
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
    path_waitingList = "/home/snourry/Documents/drive-download-20200106T103458Z-001/Scrapping_ouest/links_waitinglist.csv"

    # Le chemin des liens des restaurants (Susceptile de changer, à surveiller)
    # Attention il faut récupérer le href, pas le text
    path_link = '_15_ydu6b'

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
            # time.sleep(1)

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
        df.to_csv(path_waitingList, header=False, index=False, mode='a')
        print("Ecriture dans le fichier CSV " + path_waitingList)
        print("Nombre de pages parcourues au total : " + str(nb_page))

print("Fin du traitement. Liens totals récupérés : " + str(len(fullLinks)))
