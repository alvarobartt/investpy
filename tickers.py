from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

import unidecode
import json


def get_ticker_names():
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)

    url = "https://es.investing.com/equities/spain"
    browser.get(url)

    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'popupCloseIcon')))

    close = browser.find_element_by_class_name("popupCloseIcon")
    browser.execute_script("arguments[0].click();", close)

    select = Select(browser.find_element_by_class_name("selectBox"))
    select.select_by_visible_text("España - Acciones")

    WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.ID, 'pair_101934')))

    html = BeautifulSoup(browser.page_source, 'html.parser')

    selection = html.select("table.crossRatesTbl > tbody > tr")

    results = list()

    for element in selection:
        for nested in element.select("a"):
            info = unidecode.unidecode(nested.text).lower()
            info = info.replace(" ", "-")

            data = {
                "name": nested.text,
                "tag": info
            }

            results.append(data)

    json.dumps(results)
    return results
