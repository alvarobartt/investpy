#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json
import time

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_funds(test_mode=False):
    """
    This function retrieves all the available `spanish funds` listed on Investing.com
    (https://es.investing.com/funds/spain-funds?&issuer_filter=0). Retrieving all the meta-information attached to
    them. Additionally when funds are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources. Note that maybe some of the
    information contained in the resulting :obj:`pandas.DataFrame` is useless.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - funds:
            The resulting :obj:`pandas.DataFrame` contains all the spanish fund meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of spanish funds was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                asset class | id | isin | issuer | name | symbol | tag
                ------------|----|------|--------|------|--------|-----
                xxxxxxxxxxx | xx | xxxx | xxxxxx | xxxx | xxxxxx | xxx

    Raises:
        ValueError: if any of the introduced arguments is not valid.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'fund_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0042: fund_countries.csv file not found")

    results = list()

    for country in countries['country'].tolist():
        head = {
            "User-Agent": ua.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = 'https://es.investing.com/funds/' + country + '-funds?&issuer_filter=0'

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='etfs']"
                            "/tbody"
                            "/tr")

        if path_:
            for elements_ in path_:
                id_ = elements_.get('id').replace('pair_', '')
                symbol = elements_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

                nested = elements_.xpath(".//a")[0].get('title').rstrip()
                info = elements_.xpath(".//a")[0].get('href').replace('/funds/', '')

                data = retrieve_fund_data(info)

                obj = {
                    "country": country,
                    "name": nested.strip(),
                    "symbol": symbol,
                    "tag": info,
                    "id": id_,
                    "issuer": data['issuer'].strip() if data['issuer'] is not None else data['issuer'],
                    "isin": data['isin'],
                    "asset class": data['asset class'].lower() if data['asset class'] is not None else data['asset class'],
                }

                results.append(obj)

                if test_mode is True:
                    break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_fund_data(tag):
    """
    This function retrieves additional information from a fund as listed in Investing.com. Every fund data is retrieved
    and stored in a CSV in order to get all the possible information from a fund.

    Args:
        tag (:obj:`str`): is the identifying tag of the specified fund.

    Returns:
        :obj:`dict` - fund_data:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

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

    url = "https://www.investing.com/funds/" + tag

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

    return result


def retrieve_fund_countries(test_mode=False):
    """
    This function retrieves all the country names indexed in Investing.com with available funds to retrieve data
    from, via Web Scraping https://www.investing.com/funds/ where the available countries are listed and retrieved.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - fund_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries with their corresponding ID,
            which will be used later by investpy.

    Raises:
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com fund listing.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    headers = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/funds/'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath("//div[@id='country_select']/select/option")

    countries = list()

    for element in path:
        if element.get('value') != '/funds/world-funds':
            obj = {
                'country': element.get('value').replace('/funds/', '').replace('-funds', '').strip(),
                'id': int(element.get('country_id')),
            }

            countries.append(obj)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'fund_countries.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def fund_countries_as_list():
    """
    This function retrieves all the country names indexed in Investing.com with available funds to retrieve data
    from, via reading the `fund_countries.csv` file from the resources directory. So on, this function will display a
    listing containing a set of countries, in order to let the user know which countries are taken into account and also
    the return listing from this function can be used for country param check if needed.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with funds as indexed in Investing.com

    Raises:
        IndexError: if `fund_countries.csv` was unavailable or not found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'fund_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_fund_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0040: fund countries list not found or unable to retrieve.")
    else:
        return countries['country'].tolist()


def fund_information_as_json(df):
    """
    This function converts a :obj:`pandas.DataFrame` into a :obj:`json` object, where the introduced
    :obj:`pandas.DataFrame`, is the one created by the `investpy.get_fund_information(fund, as_json)` function,
    when as_json is `True`, which retrieves all the information listed on Investing.com from a fund.

    Args:
        df (:obj:`pandas.DataFrame`):
            generated by `investpy.get_fund_information(fund, as_json)` which contains all the available fund
            information listed on Investing.com

    Returns:
        :obj:`json` - funds_information:
            The resulting :obj:`json` as :obj:`json` contains all the features from the :obj:`pandas.DataFrame`

            In case the information was successfully retrieved, the :obj:`json` will look like::

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

    json_ = {
        'Fund Name': str(df['Fund Name'][0]),
        'Rating': int(float(df['Rating'][0])),
        '1-Year Change': str(df['1-Year Change'][0]),
        'Previous Close': str(df['Previous Close'][0]),
        'Risk Rating': int(float(df['Risk Rating'][0])),
        'TTM Yield': str(df['TTM Yield'][0]),
        'ROE': str(df['ROE'][0]),
        'Issuer': str(df['Issuer'][0]),
        'Turnover': str(df['Turnover'][0]),
        'ROA': str(df['ROA'][0]),
        'Inception Date': df['Inception Date'][0].strftime('%d/%m/%Y'),
        'Total Assets': int(float(df['Total Assets'][0])),
        'Expenses': str(df['Expenses'][0]),
        'Min Investment': int(float(df['Min Investment'][0])),
        'Market Cap': int(float(df['Market Cap'][0])),
        'Category': str(df['Category'][0])
    }

    result = json.dumps(json_, sort_keys=False)

    return result


def funds_as_df():
    """
    This function retrieves all the available `funds` from Investing.com and returns them as a :obj:`pandas.DataFrame`,
    which contains not just the fund names, but all the fields contained on the funds file.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns:
        :obj:`pandas.DataFrame` - funds_df:
            The resulting :obj:`pandas.DataFrame` contains all the funds basic information retrieved from Investing.com,
            some of which is not useful for the user, but for the inner package functions, such as the `id` field,
            for example.

            In case the information was successfully retrieved, the :obj:`pandas.DataFrame` will look like::

                asset class | id | isin | issuer | name | symbol | tag
                ------------|----|------|--------|------|--------|-----
                xxxxxxxxxxx | xx | xxxx | xxxxxx | xxxx | xxxxxx | xxx

            Just like `investpy.funds.retrieve_funds()` :obj:`pandas.DataFrame` output, but instead of generating the
            CSV file, this function just reads it and loads it into a :obj:`pandas.DataFrame` object.

    Raises:
        IOError: if the funds file from `investpy` is missing or errored.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = retrieve_funds()

    if funds is None:
        raise IOError("ERR#0005: funds not found or unable to retrieve.")
    else:
        return funds


def funds_as_list():
    """
    This function retrieves all the available funds and returns a list of each one of them.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns:
        :obj:`list` - funds_list:
            The resulting list contains the retrieved data, which corresponds to the fund names of
            every fund listed on Investing.com.

            In case the information was successfully retrieved from the CSV file, the :obj:`list` will look like::

                funds = ['Blackrock Global Funds - Global Allocation Fund E2',
                        'Quality Inversión Conservadora Fi',
                        'Nordea 1 - Stable Return Fund E Eur',
                        ...]

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: if the funds file from `investpy` is missing or errored.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = retrieve_funds()

    if funds is None:
        raise IOError("ERR#0005: funds not found or unable to retrieve.")
    else:
        return funds['name'].tolist()


def funds_as_dict(columns=None, as_json=False):
    """
    This function retrieves all the available funds on Investing.com and returns them as a :obj:`dict` containing the
    `asset_class`, `id`, `issuer`, `name`, `symbol` and `tag`. All the available funds can be found at:
    https://es.investing.com/etfs/spain-etfs

    Args:
        columns (:obj:`list` of :obj:`str`, optional): description
            a `list` containing the column names from which the data is going to be retrieved.
        as_json (:obj:`bool`, optional): description
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - funds_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'asset class': asset_class,
                    'id': id,
                    'isin': isin,
                    'issuer': issuer,
                    'name': name,
                    'symbol': symbol,
                    'tag': tag
                }

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: if the funds file from `investpy` is missing or errored.
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
        raise IOError("ERR#0005: funds not found or unable to retrieve.")

    if not all(column in funds.columns.tolist() for column in columns):
        raise ValueError("ERR#0023: specified columns does not exist, available columns are "
                         "<asset class, id, isin, issuer, name, symbol, tag>")

    if as_json:
        return json.dumps(funds[columns].to_dict(orient='records'))
    else:
        return funds[columns].to_dict(orient='records')
