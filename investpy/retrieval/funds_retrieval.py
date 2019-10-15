#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd
import pkg_resources

import requests
from lxml.html import fromstring

from investpy.utils import user_agent as ua


def retrieve_funds(test_mode=False):
    """
    This function retrieves all the available `funds` listed in Investing.com https://es.investing.com/funds. Retrieving
    all the meta-information attached to them. Additionally when funds are retrieved all the meta-information
    is both returned as a :obj:`pandas.DataFrame` and stored on a CSV file on a package folder containing all the
    available resources. Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame`
    is useless.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - funds:
            The resulting :obj:`pandas.DataFrame` contains all the fund meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of funds was successfully completed, the resulting
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

    resource_package = 'investpy'
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

        url = 'https://www.investing.com/funds/' + country.replace(' ', '-') + '-funds?issuer_filter=0'

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//select[@name='asset_filter']/option")

        assets = list()

        if path_:
            for elements_ in path_:
                assets.append(elements_.get("value"))

        for asset in assets:
            url = "https://www.investing.com/funds/" + country.replace(' ', '-') + "-funds?asset=" \
                  + str(asset) + "&issuer_filter=0"

            req = requests.get(url, headers=head)

            if req.status_code != 200:
                raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//select[@name='category_filter']/option")

            categories = list()

            if path_:
                for elements_ in path_:
                    if elements_.get("value") != '0' and not any(category['id'] == elements_.get("value") for category in categories):
                        data = {
                            'name': elements_.text_content().lower(),
                            'id': elements_.get("value"),
                        }

                        categories.append(data)

            for category in categories:
                url = "https://es.investing.com/funds/" + country.replace(' ', '-') + "-funds?asset=" \
                      + str(asset) + "&issuer_filter=0&fundCategory=" + str(category['id'])

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
                        tag = elements_.xpath(".//a")[0].get('href').replace('/funds/', '')

                        if not any(result['tag'] == tag for result in results):
                            info = None

                            while info is None:
                                try:
                                    info = retrieve_fund_info(tag)
                                except:
                                    pass

                            obj = {
                                "country": 'united kingdom' if country == 'uk' else 'united states' if country == 'usa' else country,
                                "name": nested.strip().replace(u"\N{REGISTERED SIGN}", ''),
                                "symbol": symbol,
                                "tag": tag,
                                "id": id_,
                                "issuer": info['issuer'].strip() if info['issuer'] is not None else info['issuer'],
                                "isin": info['isin'],
                                "asset_class": info['asset_class'].lower() if info['asset_class'] is not None else info['asset_class'],
                                "currency": info['currency']
                            }

                            results.append(obj)

        if test_mode is True:
            break

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    df = df.where((pd.notnull(df)), None)
    df.drop_duplicates(subset="tag", keep='first', inplace=True)
    df.sort_values('country', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df


def retrieve_fund_info(tag):
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
        ConnectionError: raised if GET requests does not return 200 status code.
        IndexError: raised if fund information was unavailable or not found.
    """

    url = "https://www.investing.com/funds/" + tag

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    result = {
        'issuer': None,
        'isin': None,
        'asset_class': None,
        'currency': None
    }

    root_ = fromstring(req.text)

    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for p in path_:
        if p.xpath("span[not(@class)]")[0].text_content().__contains__('Issuer'):
            result['issuer'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
            continue
        elif p.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
            result['isin'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
            continue
        elif p.xpath("span[not(@class)]")[0].text_content().__contains__('Asset Class'):
            result['asset_class'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
            continue

    path_ = root_.xpath(".//div[contains(@class, 'bottom')]"
                        "/span[@class='bold']")

    for element_ in path_:
        if element_.text_content():
            result['currency'] = element_.text_content()

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
                'country': element.get('value').replace('/funds/', '').replace('-funds', '').replace('-', ' ').strip(),
                'id': int(element.get('country_id')),
            }

            countries.append(obj)

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'funds', 'fund_countries.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df