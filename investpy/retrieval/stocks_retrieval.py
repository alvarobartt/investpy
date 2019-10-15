#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy.utils import user_agent as ua


def retrieve_stocks(test_mode=False):
    """
    This function retrieves all the available `stocks` indexed in Investing.com, which includes the retrieval
    of every stock information such as the full name or the symbol. Additionally, when stocks are retrieved
    alongside all the meta-information is both returned as a :obj:`pandas.DataFrame` and stored on a CSV file as
    an investpy resource. All the available stocks can be found at: https://es.investing.com/equities/

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - stocks:
            The resulting :obj:`pandas.DataFrame` contains all the stocks and their meta-information if found, if not,
            an empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored. Which will lead to an error
            whenever the stocks.csv file is found empty, raising an IOError exception.

            In the case that the stock retrieval process was successfully completed, the resulting :obj:`pandas.DataFrame`
            will look like the one presented below::

                name | full name | tag | isin | id | currency | symbol
                -----|-----------|-----|------|----|----------|--------
                xxxx | xxxxxxxxx | xxx | xxxx | xx | xxxxxxxx | xxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        FileNotFoundError: raised if `stock_countries.csv` file does not exists or is empty.

    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stock_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0038: stock_countries.csv file not found")

    results = list()

    for _, row in countries.iterrows():
        head = {
            "User-Agent": ua.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/equities/" + row['country'].replace(' ', '-')

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//select[@id='stocksFilter']/option")

        filters = list()

        if path_:
            for elements_ in path_:
                if elements_.get('id') != 'all':
                    filter_ = {
                        'id': elements_.get('id'),
                        'class': elements_.text_content(),
                    }

                    filters.append(filter_)
        else:
            obj = {
                'id': 'all',
                'class': 'all'
            }

            filters = [obj]

        for filter_ in filters:
            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            params = {
                "noconstruct": "1",
                "smlID": str(row['id']),
                "sid": "",
                "tabletype": "price",
                "index_id": str(filter_['id'])
            }

            url = "https://www.investing.com/equities/StocksFilter"

            req = requests.get(url, params=params, headers=head)

            if req.status_code != 200:
                raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='cross_rate_markets_stocks_1']"
                                "/tbody"
                                "/tr")

            if path_:
                for elements_ in path_:
                    id_ = elements_.get('id').replace('pair_', '')

                    country_check = elements_.xpath(".//td[@class='flag']/span")[0].get('title').lower()

                    if country_check == 'bosnia-herzegovina':
                        country_check = 'bosnia'
                    elif country_check == 'palestinian territory':
                        country_check = 'palestine'
                    elif country_check == 'united arab emirates':
                        country_check = 'dubai'
                    elif country_check == "cote d'ivoire":
                        country_check = 'ivory coast'

                    if row['country'] == country_check:
                        for element_ in elements_.xpath('.//a'):
                            tag_ = element_.get('href')

                            if str(tag_).__contains__('/equities/'):
                                tag_ = tag_.replace('/equities/', '')

                                if not any(result['tag'] == tag_ for result in results):
                                    full_name_ = element_.get('title').replace(' (CFD)', '')

                                    info = None

                                    while info is None:
                                        try:
                                            info = retrieve_stock_info(tag_)
                                        except:
                                            pass

                                    data = {
                                        'country': str(row['country']),
                                        'name': element_.text.strip(),
                                        'full_name': full_name_.rstrip(),
                                        'tag': tag_,
                                        'isin': info['isin'],
                                        'id': str(id_),
                                        'currency': info['currency'],
                                        'symbol': str(info['symbol']),
                                    }

                                    results.append(data)

                    if test_mode is True:
                        break

            if test_mode is True:
                break

        if test_mode is True:
            break

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df


def retrieve_stock_info(tag):
    """
    This function retrieves additional information from every stock as listed in Investing.com. This information will
    be added to the stocks file, which is `stocks.csv` file. So on, that file will contain not only the basic information
    from every stock, but additional information in order to add details to the stocks information. Note that by adding
    more parameters to every stock, it will help whenever a user wants to retrieve a stock or a group of stocks or search
    them when they do not have all the information. The more information, the more valuable the data is.

    Args:
        tag (:obj:`str`): is the tag of the stock to retrieve the information from as indexed by Investing.com.

    Returns:
        :obj:`dict` - info:
            The resulting :obj:`dict` contains the retrieved stock information, such as the ISIN code, the symbol of the
            stock or the currency in which its values are presented.

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if stock information was not found or unable to retrieve.

    """

    url = "https://es.investing.com/equities/" + tag

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
        'isin': None,
        'currency': None,
        'symbol': None
    }

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for element_ in path_:
        if element_.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
            result['isin'] = element_.xpath("span[@class='elp']")[0].text_content().rstrip()

    path_ = root_.xpath(".//div[contains(@class, 'bottom')]"
                        "/span[@class='bold']")

    for element_ in path_:
        if element_.text_content():
            result['currency'] = element_.text_content()

    path_ = root_.xpath(".//div[@class='instrumentHeader']"
                        "/h2")

    for element_ in path_:
        if element_.text_content():
            result['symbol'] = element_.text_content().replace('Resumen ', '').strip()

    return result


def retrieve_stock_countries(test_mode=False):
    """
    This function retrieves all the country names indexed in Investing.com with available stocks to retrieve data
    from. This process is made in order to dispose of a listing with all the countries from where stock information
    can be retrieved from Investing.com. So on, the retrieved country listing will be used whenever the stocks are
    retrieved, while looping over it.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - equity_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries which have available stocks as
            indexed in Investing.com, from which stock data is going to be retrieved.

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were found in the Investing.com stock listing.

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

    url = 'https://www.investing.com/equities/'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath("//*[@id='countryDropdownContainer']/div")

    countries = list()

    for element in path:
        if element.get('id') != 'regionsSelectorContainer' and element.get('id') != 'cdregion0':
            for value in element.xpath(".//ul/li/a"):
                countries.append(value.get('href').replace('/equities/', '').replace('-', ' ').strip())

    results = list()

    if len(countries) > 0:
        for country in countries:
            if country not in ['estonia', 'latvia', 'lithuania']:
                country_url = url + country

                req = requests.get(country_url, headers=headers)

                root = fromstring(req.text)
                path = root.xpath(".//*[@id='leftColumn']/input[@id='smlID']")

                country_id = path[0].get('value')

                obj = {
                    'country': country,
                    'id': country_id
                }

                results.append(obj)

            if test_mode:
                break
    else:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stock_countries.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df
