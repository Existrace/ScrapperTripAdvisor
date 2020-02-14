from selenium import webdriver
import pandas as pd

# Chemin
path_driver = '/home/snourry/Documents/chromedriver_linux64/chromedriver'

# Configuration du Chrome headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

driver = webdriver.Chrome(executable_path='/home/snourry/Documents/chromedriver_linux64/chromedriver',
                          options=chrome_options)

pages = 10
nb_pages_passe = 0

for page in range(0, pages):

    nb_pages_passe = nb_pages_passe + 1
    url = "http://quotes.toscrape.com/js/page/" + str(page) + "/"
    print('Parcours de la page numéro ' + str(nb_pages_passe))
    driver.get(url)

    items = len(driver.find_elements_by_class_name("quote"))

    total = []
    for item in range(items):
        quotes = driver.find_elements_by_class_name("quote")
        for quote in quotes:
            quote_text = quote.find_element_by_class_name('text').text
            author = quote.find_element_by_class_name('author').text
            new = (quote_text, author)
            total.append(new)
    df = pd.DataFrame(total, columns=['quote', 'author'])
    if df.to_csv('/home/snourry/Documents/drive-download-20200106T103458Z-001/test.csv'):
        print('Ecriture dans le fichier CSV')
driver.close()
