import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


def get_ticker_names():
    """
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    """

    browser = webdriver.Chrome()
    url = "https://es.investing.com/equities/spain"
    browser.get(url)

    close = browser.find_element_by_class_name("popupCloseIcon")
    browser.execute_script("arguments[0].click();", close)

    select = Select(browser.find_element_by_class_name("selectBox"))
    select.select_by_visible_text("España - Acciones")

    html = BeautifulSoup(browser.page_source, 'html.parser')

    selection = html.select('div#marketInnerContent > table > tbody > tr')

    result = list()

    for element in selection:
        info = element.select('td > a')
        print(info)


get_ticker_names()