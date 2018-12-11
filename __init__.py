import datetime
import os.path

import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from data import Data
import tickers as ts


def get_recent_data(ticker):
    if os.path.exists('tickers.csv') is False:
        tickers = ts.get_ticker_names()
        ts.convert_tickers_into_csv(tickers)

    tickers = pd.read_csv('tickers.csv')

    for item in tickers:
        if item['name'] == ticker:
            url = "https://es.investing.com/equities/" + ticker + "-historical-data"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
            }

            req = requests.get(url, headers=headers)

            status = req.status_code
            html = BeautifulSoup(req.text, 'html.parser')

            selection = html.select('div#results_box > table#curr_table > tbody > tr')

            result = list()

            for element in selection:
                info = element.getText().strip().split('\n')
                stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                stock_close = int(info[1].replace(',', ''))
                stock_open = int(info[2].replace(',', ''))
                result.insert(len(result), Data(stock_date, stock_close, stock_open))

            result = result[::-1]

            df = pd.DataFrame.from_records([data.to_dict() for data in result])
            df.set_index('Date', inplace=True)

            return df


def get_historical_data(ticker, start, end):
    for item in ts.get_ticker_names():
        if item['name'].lower() == ticker.lower():
            options = Options()
            options.add_argument("--headless")
            browser = webdriver.Chrome(options=options)

            url = "https://es.investing.com/equities/" + item['info'] + "-historical-data"
            browser.get(url)

            close = browser.find_element_by_class_name("popupCloseIcon")
            browser.execute_script("arguments[0].click();", close)

            button = browser.find_element_by_id("flatDatePickerCanvasHol")
            browser.execute_script("arguments[0].click();", button)

            start_date = browser.find_element_by_id("startDate")
            start_date.clear()
            start_date.send_keys(start)

            end_date = browser.find_element_by_id("endDate")
            end_date.clear()
            end_date.send_keys(end)

            apply = browser.find_element_by_id("applyBtn")
            browser.execute_script("arguments[0].click();", apply)

            WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.ID, 'curr_table')))

            html = BeautifulSoup(browser.page_source, 'html.parser')
            browser.close()

            selection = html.select('div#results_box > table#curr_table > tbody > tr')

            result = list()

            for element in selection:
                info = element.getText().strip().split('\n')
                stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                stock_close = int(info[1].replace(',', ''))
                stock_open = int(info[2].replace(',', ''))
                result.insert(len(result), Data(stock_date, stock_close, stock_open))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
