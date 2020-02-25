import logging
import time
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

"""
Fonctions servant pour les deux scripts :
Crawler_page_TripAdvisor
Spiderlink_TripAdvisor

"""


def setUp():
    # Chemin du driver chrome
    path_driver = '/home/snourry/Documents/chromedriver_linux64/chromedriver'

    # Configuration du Chrome headless
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=path_driver,
                              options=chrome_options)

    return driver


def scrap_data(browser):
    timeout = 10
    """ Fonction permettant de récupérer les informations nécessaire dans un lien """
    WebDriverWait(browser, timeout)
    # Récupération du nom
    nom = browser.find_element_by_css_selector('.ui_header.h1').text
    WebDriverWait(browser, timeout)

    try:
        adresse = browser.find_element_by_class_name(
            'restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei').text
        WebDriverWait(browser, timeout)
    except NoSuchElementException:
        adresse = browser.find_element_by_class_name(
            'detail  ui_link level_4').text

    if adresse:
        # Il faut que j'ajoute une dernière colonne du code postal
        # En faisant une regex dans adresse
        pattern = "[0-9]{5}"
        code_postal = re.search(pattern, adresse)
        code_postal.group()

    try:
        # E-mail
        mail = browser.find_element_by_link_text('E-mail').get_attribute("href")
        # Enlève les parties inutiles de l'e-mail extraite
        mail = mail.replace('mailto:', '')
        mail = mail.replace('?subject=?', '')
        print("Mail trouvé : " + mail)
    except NoSuchElementException:
        print("Mail non trouvé")
        mail = ''

    WebDriverWait(browser, timeout)

    # Récupération du numéro de téléphone
    # L'adresse postale et le numéro partage les mêmes class CSS
    # alors j'ai été contraint de prendre le deuxième élement (à surveiller)
    result_num = browser.find_elements_by_class_name('ui_link')
    numero_tel = result_num[1].text

    try:
        type_cuisine = browser.find_elements_by_class_name(
            "restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h")
        type_cuisine = type_cuisine[1].text
    except IndexError:
        try:
            type_cuisine = browser.find_element_by_class_name(
                "restaurants-detail-overview-cards-SnippetsOverviewCard__heading--2jhMN").text
        except:
            type_cuisine = ""

    except Exception as e:
        logging.exception(e)
        type_cuisine = ""

    # Insertion de toutes les données dans une liste
    data_all_array = [
        nom,
        adresse,
        mail,
        numero_tel,
        type_cuisine,
        code_postal
    ]

    return data_all_array
