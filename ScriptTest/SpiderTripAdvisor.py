import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class SpiderTripAdvisor:

    def __init__(self):
        self.path_driver = '/home/snourry/Documents/chromedriver_linux64/chromedriver'
        self.url = "https://www.tripadvisor.fr/Restaurants-g187147-Paris_Ile_de_France.html"

    def setUp(self):
        # Configuration du Chrome headless
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        browser = webdriver.Chrome(executable_path=self.path_driver,
                                   options=chrome_options)
        browser.get(self.url)
        time.sleep(2)

