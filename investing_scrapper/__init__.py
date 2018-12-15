#!/usr/bin/env python

import datetime

import pandas as pd
import pkg_resources
import requests
from bs4 import BeautifulSoup

from investing_scrapper.Data import Data # TypeError: 'module' object is not callable
from investing_scrapper import user_agent as ua, tickers as ts


def get_recent_data(ticker):
    resource_package = __name__
    resource_path = '/'.join(('resources', 'tickers.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        tickers = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = ts.get_ticker_names()
        tickers = pd.DataFrame(names)

    for row in tickers.itertuples():
        if row.name.lower() == ticker.lower():
            url = "https://es.investing.com/equities/" + ticker + "-historical-data"
            headers = {
                'User-Agent': ua.get_random()
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

            df = pd.DataFrame.from_records([value.to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df


def get_historical_data(ticker, start, end):
    for item in ts.get_ticker_names():
        if item['name'].lower() == ticker.lower():
            params = {
                "curr_id": "558",
                "smlID": "1159685",
                "header": "Datos históricos SAN",
                "st_date": start,
                "end_date": end,
                "interval_sec": "Daily",
                "sort_col": "date",
                "sort_ord": "DESC",
                "action": "historical_data"
            }

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            url = "https://es.investing.com/instruments/HistoricalDataAjax"

            req = requests.post(url, data=params, headers=head)

            html = BeautifulSoup(req.content, 'html.parser')

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