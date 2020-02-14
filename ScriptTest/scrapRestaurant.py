import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# Chemin du driver chrome
path_driver = '/home/snourry/Documents/chromedriver_linux64/chromedriver'

# Configuration du Chrome headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

browser = webdriver.Chrome(executable_path=path_driver,
                           options=chrome_options)

url = "https://www.tripadvisor.fr/Restaurant_Review-g187147-d9783452-Reviews-Boutary-Paris_Ile_de_France.html"

browser.get(url)
time.sleep(2)


def scrap_data(browser):
    timeout = 10
    """ Fonction permettant de récupérer les informations nécessaire dans un lien """
    WebDriverWait(browser, timeout)
    # Récupération du nom
    nom = browser.find_element_by_css_selector('.ui_header.h1').text
    WebDriverWait(browser, timeout)
    # Récupération de l'adresse postale
    adresse = browser.find_element_by_class_name(
        'restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei').text
    WebDriverWait(browser, timeout)
    """
    # E-mail
    mail = browser.find_element_by_link_text('E-mail').get_attribute("href")
    # Enlève les parties inutiles de l'e-mail extraite
    mail = mail.replace('mailto:', '')
    mail = mail.replace('?subject=?', '')
    """
    WebDriverWait(browser, timeout)
    # Récupération du numéro de téléphone
    # L'adresse postale et le numéro partage les mêmes class CSS
    # alors j'ai été contraint de prendre le deuxième élement (à surveiller)
    result_num = browser.find_elements_by_class_name('ui_link')
    numero_tel = result_num[1].text

    # Insertion de toutes les données dans une liste
    data_all_array = [
        nom,
        adresse,
        # mail,
        numero_tel
    ]

    return data_all_array


recupData = scrap_data(browser)

for data in recupData:
    print(data)
