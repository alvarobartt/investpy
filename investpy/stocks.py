#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import unidecode
import json

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_stocks(test_mode=False):
    """
    This function retrieves all the available `stocks` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the stocks available can be found at: https://es.investing.com/equities/. Additionally,
    when stocks are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - stocks:
            The resulting :obj:`pandas.DataFrame` contains all the stocks meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of stocks was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                name | full name | tag | isin | id
                -----|-----------|-----|------|----
                xxxx | xxxxxxxxx | xxx | xxxx | xx

    Raises:
        ValueError: if any of the introduced arguments is not valid.
        FileNotFoundError: raised if `stock_countries.csv` file does not exists or is empty.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if stocks information was unavailable or not found.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    resource_package = __name__
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

        params = {
            "noconstruct": "1",
            "smlID": str(row['id']),
            "sid": "",
            "tabletype": "price",
            "index_id": "all"
        }

        url = "https://es.investing.com/equities/StocksFilter"

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

                for element_ in elements_.xpath('.//a'):
                    tag_ = element_.get('href')

                    if str(tag_).__contains__('/stocks/'):
                        tag_ = tag_.replace('/stocks/', '')

                        full_name_ = element_.get('title').replace(' (CFD)', '')

                        info = retrieve_stock_info(tag_)

                        data = {
                            'country': str(row['country']),
                            'name': element_.text.strip(),
                            'full_name': full_name_.rstrip(),
                            'tag': tag_,
                            'isin': info['isin'],
                            'id': id_,
                            'currency': info['currency'],
                            'symbol': info['symbol']
                        }

                        results.append(data)

                if test_mode is True:
                    break
        if test_mode is True:
            break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_stock_info(tag):
    """
    This function retrieves both the ISIN code, the currency and the symbol of an stock indexed in Investing.com, so
    to include additional information in `stocks.csv` file. The ISIN code will later be used in order to retrieve more
    information from the specified stock, as the ISIN code is an unique identifier of each stock; the currency
    will be required in order to know which currency is the value in, and the symbol will be used for processing the
    request to HistoricalDataAjax to retrieve historical data from Investing.com.

    Args:
        tag (:obj:`str`): is the tag of the stock to retrieve the information from as indexed by Investing.com.

    Returns:
        :obj:`dict` - info:
            The resulting :obj:`dict` contains the needed information for the stocks listing, so on, the ISIN
             code of the introduced stock, the currency of its values and the symbol of the stock.

    Raises:
        ConnectionError: raised if GET requests does not return 200 status code.
        IndexError: raised if either the isin code or the currency were unable to retrieve.
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
    from, via Web Scraping https://www.investing.com/equities/ where the available countries are listed, and from their
    names the specific stock website of every country is retrieved in order to get the ID which will later be used
    when retrieving all the information from the available stocks in every country.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - equity_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries with their corresponding ID,
            which will be used later by investpy.

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com stock listing.
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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stock_countries.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def stock_countries_as_list():
    """
    This function retrieves all the country names indexed in Investing.com with available stocks to retrieve data
    from, via reading the `stock_countries.csv` file from the resources directory. So on, this function will display a
    listing containing a set of countries, in order to let the user know which countries are taken into account and also
    the return listing from this function can be used for country param check if needed.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with stocks as indexed in Investing.com

    Raises:
        IndexError: if `stock_countries.csv` was unavailable or not found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stock_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_stock_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0036: stock countries list not found or unable to retrieve.")
    else:
        return countries['country'].tolist()


def stocks_as_df(country=None):
    """
    This function retrieves all the stocks previously stored on `stocks.csv` file, via
    `investpy.stocks.retrieve_equities()`. The CSV file is read and if it does not exists,
    it is created again; but if it does exists, it is loaded into a :obj:`pandas.DataFrame`.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`pandas.DataFrame` - equities_df:
            The resulting :obj:`pandas.DataFrame` contains the `stocks.csv` file content if
            it was properly read or retrieved in case it did not exist in the moment when the
            function was first called.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                name | full name | tag | isin | id
                -----|-----------|-----|------|----
                xxxx | xxxxxxxxx | xxx | xxxx | xx

    Raises:
        IOError: raised if stocks retrieval failed, both for missing file or empty file, after and before retrieval.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        stocks = retrieve_stocks()

    if stocks is None:
        raise IOError("ERR#0001: stocks list not found or unable to retrieve.")

    if country is None:
        stocks.reset_index(drop=True, inplace=True)
        return stocks
    elif unidecode.unidecode(country.lower()) in stock_countries_as_list():
        stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]
        stocks.reset_index(drop=True, inplace=True)
        return stocks


def stocks_as_list(country=None):
    """
    This function retrieves all the stocks previously stored on `stocks.csv` file, via
    `investpy.stocks.retrieve_equities()`. The CSV file is read and if it does not exists,
    it is created again; but if it does exists, stock names are loaded into a :obj:`list`.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`list` - equities_list:
            The resulting :obj:`list` contains the `stocks.csv` file content if
            it was properly read or retrieved in case it did not exist in the moment when the
            function was first called, as a :obj:`list` containing all the stock names.

            So on the listing will contain the stock names listed on Investing.com and will
            look like the following::

                equities_list = ['ACS', 'Abengoa', 'Atresmedia', ...]

    Raises:
        IOError: raised if stocks retrieval failed, both for missing file or empty file, after and before retrieval.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        stocks = retrieve_stocks()

    if stocks is None:
        raise IOError("ERR#0001: stocks list not found or unable to retrieve.")

    if country is None:
        return stocks['name'].tolist()
    elif unidecode.unidecode(country.lower()) in stock_countries_as_list():
        return stocks[stocks['country'] == unidecode.unidecode(country.lower())]['name'].tolist()


def stocks_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available stocks indexed in Investing.com, already
    stored on `stocks.csv`, which if does not exists, will be created by `investpy.stocks.retrieve_equities()`.
    This function also allows the user to specify which country do they want to retrieve data from,
    or from every listed country; the columns which the user wants to be included on the resulting
    :obj:`dict`; and the output of the function will either be a :obj:`dict` or a :obj:`json`.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.
        columns (:obj:`list`, optional):
            names of the columns of the stock data to retrieve <country, name, full_name, tag, isin, id, currency>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

    Returns:
        :obj:`dict` or :obj:`json` - equities_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'tag': tag,
                    'isin': isin,
                    'id': id,
                    'currency': currency,
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `stocks.csv` file is missing or empty.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        stocks = retrieve_stocks()

    if stocks is None:
        raise IOError("ERR#0001: stocks list not found or unable to retrieve.")

    if columns is None:
        columns = stocks.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in stocks.columns.tolist() for column in columns):
        raise ValueError("ERR#0021: specified columns does not exist, available columns are "
                         "<country, name, full_name, tag, isin, id, symbol, currency>")

    if country is None:
        if as_json:
            return json.dumps(stocks[columns].to_dict(orient='records'))
        else:
            return stocks[columns].to_dict(orient='records')
    elif country in stock_countries_as_list():
        if as_json:
            return json.dumps(stocks[stocks['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records'))
        else:
            return stocks[stocks['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records')
