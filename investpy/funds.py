#!/usr/bin/env python

import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import pkg_resources

from investpy import user_agent as ua


def get_fund_names():
    """
    This function retrieves all the available funds to retrieve data from.
    All the funds available can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        returns a dictionary containing all the funds information
    """

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://es.investing.com/funds/spain-funds?&issuer_filter=0"

    req = requests.get(url, headers=head)

    html = BeautifulSoup(req.content, 'html.parser')

    selection = html.select("table#etfs > tbody > tr")

    results = list()

    for element in selection:
        id_ = element.get('id')
        id_ = id_.replace('pair_', '')

        symbol = None
        for symbol in element.select("td.symbol"):
            symbol = symbol.get("title")

        for nested in element.select("a"):
            info = nested.get("href")
            info = info.replace("/funds/", "")

            if symbol:
                data = {
                    "name": nested.text,
                    "symbol": symbol,
                    "tag": info,
                    "id": id_
                }
            else:
                data = {
                    "name": nested.text,
                    "symbol": "undefined",
                    "tag": info,
                    "id": id_
                }

            results.append(data)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results


def fund_information_to_json(df):
    """
    This function converts a pandas.DataFrame, containing all the information from a fund, into a JSON

    Returns
    -------
        returns a JSON object containing fund information
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
    result = json.dumps(json_)
    return result


def list_funds():
    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_fund_names()
        funds = pd.DataFrame(names)

    return funds['name'].tolist()
