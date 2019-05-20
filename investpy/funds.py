#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import pandas as pd
import requests
from tqdm import tqdm
import json
from lxml.html import fromstring
import pkg_resources

from investpy import user_agent as ua


def get_fund_names():
    """
    This function retrieves all the available funds to retrieve data from.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        :returns a dictionary containing all the funds information
    """

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/funds/spain-funds?&issuer_filter=0"

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#015: error " + req.status_code + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='etfs']"
                        "/tbody"
                        "/tr")

    results = list()

    if path_:
        for elements_ in tqdm(path_, ascii=True, ncols=80):
            id_ = elements_.get('id').replace('pair_', '')
            symbol = elements_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

            nested = elements_.xpath(".//a")[0].get('title').rstrip()
            info = elements_.xpath(".//a")[0].get('href').replace('/funds/', '')

            data = get_fund_data(info)

            if symbol:
                obj = {
                    "name": nested,
                    "symbol": symbol,
                    "tag": info,
                    "id": id_,
                    "issuer": data['issuer'],
                    "isin": data['isin'],
                    "asset class": data['asset class'],
                }
            else:
                obj = {
                    "name": nested,
                    "symbol": "undefined",
                    "tag": info,
                    "id": id_,
                    "issuer": data['issuer'],
                    "isin": data['isin'],
                    "asset class": data['asset class'],
                }

            results.append(obj)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'funds.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results


def get_fund_data(fund_tag):
    url = "https://www.investing.com/funds/" + fund_tag

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head, timeout=5)

    if req.status_code != 200:
        raise ConnectionError("ERR#015: error " + req.status_code + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    result = {
        'issuer': None,
        'isin': None,
        'asset class': None,
    }

    for p in path_:
        try:
            if p.xpath("span[not(@class)]")[0].text_content().__contains__('Issuer'):
                try:
                    result['issuer'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
                    continue
                except IndexError:
                    raise IndexError("ERR#023: fund issuer unavailable or not found.")
            elif p.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
                try:
                    result['isin'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
                    continue
                except IndexError:
                    raise IndexError("ERR#024: fund isin code unavailable or not found.")
            elif p.xpath("span[not(@class)]")[0].text_content().__contains__('Asset Class'):
                try:
                    result['asset class'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
                    continue
                except IndexError:
                    raise IndexError("ERR#025: fund asset class unavailable or not found.")
            else:
                continue
        except IndexError:
            raise IndexError("ERR#017: isin code unavailable or not found.")

    if None not in result.values():
        return result
    else:
        return result


def fund_information_to_json(df):
    """
    This function converts a pandas.DataFrame, containing all the information from a fund, into a JSON

    Returns
    -------
        :returns a JSON object containing fund information
    """

    json_ = {
        'Fund Name': str(df['Fund Name'][0]),
        'Rating': str(df['Rating'][0]),
        '1-Year Change': str(df['1-Year Change'][0]),
        'Previous Close': str(df['Previous Close'][0]),
        'Risk Rating': str(df['Risk Rating'][0]),
        'TTM Yield': str(df['TTM Yield'][0]),
        'ROE': str(df['ROE'][0]),
        'Issuer': str(df['Issuer'][0]),
        'Turnover': str(df['Turnover'][0]),
        'ROA': str(df['ROA'][0]),
        'Inception Date': str(df['Inception Date'][0]),
        'Total Assets': str(df['Total Assets'][0]),
        'Expenses': str(df['Expenses'][0]),
        'Min Investment': str(df['Min Investment'][0]),
        'Market Cap': str(df['Market Cap'][0]),
        'Category': str(df['Category'][0])
    }

    result = json.dumps(json_, sort_keys=False)

    return result


def list_funds():
    """
    This function retrieves all the available funds and returns a list of each one of them.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        :returns a list with all the available funds to retrieve data from
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_fund_names()
        funds = pd.DataFrame(names)

    if funds is None:
        raise IOError("ERR#005: fund list not found or unable to retrieve.")
    else:
        return funds['name'].tolist()
