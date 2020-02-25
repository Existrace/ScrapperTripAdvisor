from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re

adresse = "Avenue Théodore Monod, 95150 Taverny France"
pattern = "[0-9]{5}"
# search = re.compile(pattern)
# code_postal = search.match("Avenue Théodore Monod, 95150 Taverny France")

code_postal = re.search(pattern, "Avenue Théodore Monod, 95150 Taverny France").group()

print(code_postal)
