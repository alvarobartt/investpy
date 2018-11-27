import requests
import datetime
import pandas as pd
from model import Data
from bs4 import BeautifulSoup
from selenium import webdriver


def get_recent_data(ticker):
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
    browser = webdriver.Firefox()
    url = "https://es.investing.com/equities/" + ticker + "-historical-data"
    browser.get(url)

    button = browser.find_element_by_class_name("datePickerWrap")
    button.click()

    start_date = browser.find_element_by_id("startDate")
    start_date.clear()
    start_date.send_keys(start)

    end_date = browser.find_element_by_id("endDate")
    end_date.clear()
    end_date.send_keys(end)

    button = browser.find_element_by_id("applyBtn")
    button.click()

    browser.implicitly_wait(10)
    html = browser.execute_script("return document.body.innerHTML")

    print(html)


get_historical_data('bbva', '10/10/2016', '10/10/2018')