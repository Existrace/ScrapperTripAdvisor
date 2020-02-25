import csv
import logging
import time
import utils
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd

# Il faut que je fasse un script qui a comme point de départ cette adresse :
# https://www.tripadvisor.fr/Restaurants-g187144-Ile_de_France.html#LOCATION_LIST

path_url = "geo_name"
list_url = []
is_enable = True
nb_page = 0
timeout = 10
path_firstPages = "/home/snourry/Documents/drive-download-20200106T103458Z-001/CsvParis/links_waitingUrl.csv"

browser = utils.setUp()

url = "https://www.tripadvisor.fr/Restaurants-g187144-Ile_de_France.html#LOCATION_LIST"
browser.get(url)

try:
    # Il faut récupérer les liens de la page courante avant de cliquer sur suivant
    print("Parcours des pages des régions de Paris pour récupérer tous les premier liens. Démarrage. \n")
    print("Execution de la page N° 1 " + url + "\n")
    list_links = browser.find_elements_by_class_name(path_url)
    print("Nombre de liens récupérés sur la page " + str(nb_page) + " : " + str(len(list_links)) + " liens. \n")
    browser.implicitly_wait(10)

    for link in list_links:
        list_url.append(link.get_attribute("href"))

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
        print("Récupération de l'url " + str(next_page.get_attribute("href")) + "\n")

        # Récupération des liens des autres pages
        list_links = browser.find_elements_by_class_name(path_url)

        print("Nombre de urls récupérées sur la page " + str(nb_page) + " : " + str(len(list_links)) + " liens.")

        for link in list_links:
            list_url.append(link.get_attribute("href"))

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
    print(list_url)
    is_enable = False
    df = pd.DataFrame(list_url)
    df.to_csv(path_firstPages, header=False, index=False, mode='a')
    print("Ecriture dans le fichier CSV " + path_firstPages)
    print("Nombre de pages parcourues au total : " + str(nb_page))
