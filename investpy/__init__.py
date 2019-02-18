#!/usr/bin/env python

import datetime

import pandas as pd
import pkg_resources
import requests
from bs4 import BeautifulSoup

from investpy.Data import Data # TypeError: 'module' object is not callable
from investpy import user_agent as ua, equities as ts, funds as fs


def get_recent_data(equity):
    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = ts.get_equity_names()
        equities = pd.DataFrame(names)

    for row in equities.itertuples():
        if row.name.lower() == equity.lower():
            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"
            headers = {
                'User-Agent': ua.get_random()
            }

            req = requests.get(url, headers=headers)

            status = req.status_code
            html = BeautifulSoup(req.text, 'html.parser')

            selection = html.select('div#results_box > table#curr_table > tbody > tr')

            result = list()

            for element in selection:
                info = element.getText().strip().split()

                stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                stock_close = float(info[1].replace(',', '.'))
                stock_open = float(info[2].replace(',', '.'))
                stock_max = float(info[3].replace(',', '.'))
                stock_min = float(info[4].replace(',', '.'))
                stock_volume = 0

                if info[5].__contains__('K'):
                    stock_volume = int(float(info[5].replace('K', '').replace(',', '.')) * 1000)
                elif info[5].__contains__('M'):
                    stock_volume = int(float(info[5].replace('M', '').replace(',', '.')) * 1000000)
                elif info[5].__contains__('B'):
                    stock_volume = int(float(info[5].replace('B', '').replace(',', '.')) * 1000000000)

                result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, stock_volume,))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.equity_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df


def get_historical_data(equity, start, end):
    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = ts.get_equity_names()
        equities = pd.DataFrame(names)

    for row in equities.itertuples():
        if row.name.lower() == equity.lower():
            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"
            headers = {
                'User-Agent': ua.get_random()
            }

            req = requests.get(url, headers=headers)

            status = req.status_code
            html = BeautifulSoup(req.text, 'html.parser')

            selection = html.select('div.instrumentHeader > h2')
            for element in selection:
                header = element.text

            params = {
                "curr_id": row.id,
                "smlID": "1159685",
                "header": header,
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
                info = element.getText().strip().split()

                stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                stock_close = float(info[1].replace(',', '.'))
                stock_open = float(info[2].replace(',', '.'))
                stock_max = float(info[3].replace(',', '.'))
                stock_min = float(info[4].replace(',', '.'))
                stock_volume = 0

                if info[5].__contains__('K'):
                    stock_volume = int(float(info[5].replace('K', '').replace(',', '.')) * 1000)
                elif info[5].__contains__('M'):
                    stock_volume = int(float(info[5].replace('M', '').replace(',', '.')) * 1000000)
                elif info[5].__contains__('B'):
                    stock_volume = int(float(info[5].replace('B', '').replace(',', '.')) * 1000000000)

                result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, stock_volume,))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.equity_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df


def get_fund_recent_data(fund):
    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = fs.get_fund_names()
        funds = pd.DataFrame(names)

    for row in funds.itertuples():
        if row.name.lower() == fund.lower():
            url = "https://es.investing.com/funds/" + row.tag + "-historical-data"
            headers = {
                'User-Agent': ua.get_random()
            }

            req = requests.get(url, headers=headers)

            status = req.status_code
            html = BeautifulSoup(req.text, 'html.parser')

            selection = html.select('div#results_box > table#curr_table > tbody > tr')

            result = list()

            for element in selection:
                info = element.getText().strip().split()

                stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                stock_close = float(info[1].replace(',', '.'))
                stock_open = float(info[2].replace(',', '.'))
                stock_max = float(info[3].replace(',', '.'))
                stock_min = float(info[4].replace(',', '.'))

                result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, None,))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df


def get_fund_historical_data(fund, start, end):
    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = fs.get_fund_names()
        funds = pd.DataFrame(names)

    for row in funds.itertuples():
        if row.name.lower() == fund.lower():
            header = "Datos históricos " + row.symbol

            params = {
                "curr_id": row.id,
                "smlID": "15361696",
                "header": header,
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
                info = element.getText().strip().split()

                stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                stock_close = float(info[1].replace(',', '.'))
                stock_open = float(info[2].replace(',', '.'))
                stock_max = float(info[3].replace(',', '.'))
                stock_min = float(info[4].replace(',', '.'))

                result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, None,))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df