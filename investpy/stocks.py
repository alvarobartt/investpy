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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks2.csv'))
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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stock_countries.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df


def stock_countries_as_list():
    """
    This function returns a listing with all the available countries from where stocks can be retrieved, so to
    let the user know which of them are available, since the parameter country is mandatory in every stock retrieval
    function. Also, not just the available countries, but the required name is provided since Investing.com has a
    certain country name standard and countries should be specified the same way they are in Investing.com.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with stocks as indexed in Investing.com

    Raises:
        IOError: raised when `stock_countries.csv` file is missing or empty.

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
    This function retrieves all the stock data stored in `stocks.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the stock data is properly
    structured in rows and columns, where columns are the stock data attribute names. Additionally, country 
    filtering can be specified, which will make this function return not all the stored stock data, but just 
    the stock data of the stocks from the introduced country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`pandas.DataFrame` - stocks_df:
            The resulting :obj:`pandas.DataFrame` contains all the stock data from the introduced country if specified, 
            or from every country if None was specified, as indexed in Investing.com from the information previously 
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | full name | isin | currency | symbol 
                --------|------|-----------|------|----------|--------
                xxxxxxx | xxxx | xxxxxxxxx | xxxx | xxxxxxxx | xxxxxx 

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        IOError: raised when `stocks.csv` file is missing or empty.

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

    stocks.drop(columns=['tag', 'id'], inplace=True)

    if country is None:
        stocks.reset_index(drop=True, inplace=True)
        return stocks
    elif unidecode.unidecode(country.lower()) in stock_countries_as_list():
        stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]
        stocks.reset_index(drop=True, inplace=True)
        return stocks


def stocks_as_list(country=None):
    """
    This function retrieves all the stock symbols stored in `stocks.csv` file, which contains all the 
    data from the stocks as previously retrieved from Investing.com. So on, this function will just return
    the stock symbols which will be one of the input parameters when it comes to stock data retrieval functions
    from investpy. Additionally, note that the country filtering can be applied, which is really useful since
    this function just returns the symbols and in stock data retrieval functions both the symbol and the country
    must be specified and they must match.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`list` - stocks_list:
            The resulting :obj:`list` contains the all the stock symbols from the introduced country if specified, 
            or from every country if None was specified, as indexed in Investing.com from the information previously 
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of stock symbols will look like::

                stocks_list = ['TS', 'APBR', 'GGAL', 'TXAR', 'PAMP', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        IOError: raised when `stocks.csv` file is missing or empty.
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

    stocks.drop(columns=['tag', 'id'], inplace=True)

    if country is None:
        return stocks['symbol'].tolist()
    elif unidecode.unidecode(country.lower()) in stock_countries_as_list():
        return stocks[stocks['country'] == unidecode.unidecode(country.lower())]['symbol'].tolist()


def stocks_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the stock information stored in the `stocks.csv` file and formats it as a 
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and 
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the 
    JSON structure. Some optional paramaters can be specified such as the country, columns or as_json, which 
    are a filtering by country so not to return all the stocks but just the ones from the introduced country, 
    the column names that want to be retrieved in case of needing just some columns to avoid unnecessary information
    load, and whether the information wants to be returned as a JSON object or as a dictionary; respectively.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.
        columns (:obj:`list`, optional):column names of the stock data to retrieve, can be: <country, name, full_name, isin, currency, symbol>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - equities_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every stock as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'tag': tag,
                    'isin': isin,
                    'id': id,
                    'currency': currency,
                    'symbol': symbol,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
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

    stocks.drop(columns=['tag', 'id'], inplace=True)

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
