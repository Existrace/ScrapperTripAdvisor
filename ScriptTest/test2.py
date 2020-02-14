import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# Chemin du driver chrome
path_driver = '/home/snourry/Documents/chromedriver_linux64/chromedriver'

# Configuration du Chrome headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path='/home/snourry/Documents/chromedriver_linux64/chromedriver',
                          options=chrome_options)

url = "https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html"

driver.get(url)
time.sleep(2)

# La première page à laquelle on est. Il faudra qu'elle change selon la page
window_before = driver.window_handles[0]

print("Page actuelle : " + driver.title)

links = driver.find_elements_by_class_name(
    "restaurants-list-ListCell__titleRow--3rRCX .restaurants-list-ListCell__restaurantName--2aSdo")

"""
Ce bloc est la deuxième étape, quand on a récupéré les liens qui sont dans un fichier CSV
Juste avant cette boucle il faudrait convertir les données du CSV en liste 
"""
# elements = elements[0:2]
timeout = 10
compteur = 0
WebDriverWait(driver, timeout)
for i in range(len(links)):
    driver.switch_to.window(window_before)

    compteur = compteur + 1
    print("Execution du lien N° " + str(compteur))
    WebDriverWait(driver, timeout)
    links[i].click()
    driver.implicitly_wait(10)  # seconds
    time.sleep(2)
    # Changement de page, passage au lien trouvé
    # Plus tard il faudra vérifier si on est à la dernière page (bouton disabled ou pas)
    driver.switch_to.window(driver.window_handles[1])
    print("Arrivée sur le lien : " + driver.title)

    """
    Appel de la fonction ScrapData ici
    """
driver.quit()
