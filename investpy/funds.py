#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import json

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_funds():
    """
    This function retrieves all the available spanish funds listed on Investing
    (https://es.investing.com/funds/spain-funds?&issuer_filter=0). Retrieving all the meta-information attached to
    them. Additionally when funds are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources. Note that maybe some of the
    information contained in the resulting :obj:`pandas.DataFrame` is useless.

    Returns:
        :obj:`pandas.DataFrame`: contains all the spanish fund meta-information if found, if not, an empty
        :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

        In the case that the retrieval process of spanish funds was successfully completed, the resulting
        :obj:`pandas.DataFrame` will look like::

            asset class | id | isin | issuer | name | symbol | tag
            ------------|----|------|--------|------|--------|-----
            xxxxxxxxxxx | xx | xxxx | xxxxxx | xxxx | xxxxxx | xxx

    Raises:
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.
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
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='etfs']"
                        "/tbody"
                        "/tr")

    results = list()

    if path_:
        for elements_ in path_:
            id_ = elements_.get('id').replace('pair_', '')
            symbol = elements_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

            nested = elements_.xpath(".//a")[0].get('title').rstrip()
            info = elements_.xpath(".//a")[0].get('href').replace('/funds/', '')

            data = retrieve_fund_data(info)

            obj = {
                "name": nested,
                "symbol": symbol,
                "tag": info,
                "id": id_,
                "issuer": data['issuer'],
                "isin": data['isin'],
                "asset class": data['asset class'],
            }

            results.append(obj)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return df


def retrieve_fund_data(fund):
    """
    This function retrieves additional information from a fund as listed on
    es.Investing.com. Every fund data is retrieved and stored in a CSV in order
    to get all the possible information from a fund.

    Args:
        fund (:obj:`str`): is the identifying tag of the specified fund.

    Returns:
        :obj:`dict`: The resulting dictionary contains the retrieved data if found, if not, the corresponding
        fields are filled with None values.

        In case the information was successfully retrieved, the :obj:`dict` will look like::

            {
                'issuer': issuer_value,
                'isin': isin_value,
                'asset class': asset_value
            }

    Raises:
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.
    """

    url = "https://www.investing.com/funds/" + fund

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head, timeout=5)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

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
                result['issuer'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
                continue
            elif p.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
                result['isin'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
                continue
            elif p.xpath("span[not(@class)]")[0].text_content().__contains__('Asset Class'):
                result['asset class'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
                continue
            else:
                continue
        except IndexError:
            raise IndexError("ERR#0017: isin code unavailable or not found.")

    return result


def fund_information_as_json(df):
    """
    This function converts a :obj:`pandas.DataFrame` into a :obj:`JSON` object, where the introduced
    :obj:`pandas.DataFrame`, is the one created by the `investpy.get_fund_information(fund, as_json)` function,
    when as_json is `True`, which retrieves all the information listed on Investing.com from a fund.

    Args:
        df (:obj:`pandas.DataFrame`): description
            generated by `investpy.get_fund_information(fund, as_json)` which contains all the available fund
            information listed on Investing.com

    Returns:
        :obj:`dict`: the resulting dictionary as :obj:`JSON` contains all the features from the :obj:`pandas.DataFrame`

        In case the information was successfully retrieved, the :obj:`dict` will look like::

            {
                'Fund Name': fund_name,
                'Rating': rating,
                '1-Year Change': year_change,
                'Previous Close': prev_close,
                'Risk Rating': risk_rating,
                'TTM Yield': ttm_yield,
                'ROE': roe,
                'Issuer': issuer,
                'Turnover': turnover,
                'ROA': row,
                'Inception Date': inception_date,
                'Total Assets': total_assets,
                'Expenses': expenses,
                'Min Investment': min_investment,
                'Market Cap': market_cap,
                'Category': category
            }

    Raises:
        IndexError: if fund information was unavailable or not found.
    """

    try:
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
    except IndexError:
        return {}


def funds_as_df():
    """
    This function retrieves all the available funds and returns a pandas.DataFrame of them all.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        :returns a pandas.DataFrame with all the available funds to retrieve data from
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = retrieve_funds()

    if funds is None:
        raise IOError("ERR#0005: fund list not found or unable to retrieve.")
    else:
        return funds


def funds_as_list():
    """
    This function retrieves all the available funds and returns a list of each one of them.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        :returns a list with all the available funds to retrieve data from
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = retrieve_funds()

    if funds is None:
        raise IOError("ERR#0005: fund list not found or unable to retrieve.")
    else:
        return funds['name'].tolist()


def funds_as_dict(columns=None, as_json=False):
    """
    This function retrieves all the available funds and returns a dictionary with the specified columns.
    Available columns are: 'asset class', 'id', 'isin', 'issuer', 'name', 'symbol' and 'tag'
    All the available funds can be found at: https://es.investing.com/etfs/spain-etfs

    Returns
    -------
        :returns a dictionary that contains all the available fund values specified in the columns
    """

    if columns is None:
        columns = ['asset class', 'id', 'isin', 'issuer', 'name', 'symbol', 'tag']
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = retrieve_funds()

    if funds is None:
        raise IOError("ERR#0005: fund list not found or unable to retrieve.")

    if not all(column in funds.columns.tolist() for column in columns):
        raise ValueError("ERR#0023: specified columns does not exist, available columns are "
                         "<asset class, id, isin, issuer, name, symbol, tag>")

    if as_json:
        return json.dumps(funds[columns].to_dict(orient='records'))
    else:
        return funds[columns].to_dict(orient='records')
