#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

__author__ = 'Alvaro Bartolome @ alvarob96 in GitHub'
__version__ = '0.9.6'

import datetime
import json
from random import randint
import logging

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent, stocks as eq, funds as fs, etfs as es, indices as ic, currency_crosses as cc
from investpy.Data import Data


"""------------- STOCKS -------------"""


def get_stocks(country=None):
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

                country | name | full name | isin | class | currency | symbol 
                --------|------|-----------|------|-------|----------|--------
                xxxxxxx | xxxx | xxxxxxxxx | xxxx | xxxxx | xxxxxxxx | xxxxxx 

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        IOError: raised when `stocks.csv` file is missing or empty.

    """

    return eq.stocks_as_df(country)


def get_stocks_list(country=None):
    """
    This function retrieves all the stock names stored in `stocks.csv` file, which contains all the 
    data from the stocks as previously retrieved from Investing.com. So on, this function will just return
    the stock names which will be one of the input parameters when it comes to stock data retrieval functions
    from investpy. Additionally, note that the country filtering can be applied, which is really useful since
    this function just returns the names and in stock data retrieval functions both the name and the country
    must be specified and they must match.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`list` - stocks_list:
            The resulting :obj:`list` contains the all the stock names from the introduced country if specified, 
            or from every country if None was specified, as indexed in Investing.com from the information previously 
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of stock names will look like::

                stocks_list = ['ACS', 'Abengoa', 'Atresmedia', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        IOError: raised when `stocks.csv` file is missing or empty.

    """

    return eq.stocks_as_list(country)


def get_stocks_dict(country=None, columns=None, as_json=False):
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
        columns (:obj:`list`, optional):column names of the stock data to retrieve, can be: <country, name, full_name, isin, currency, class, symbol>
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
                    'class': class,
                    'symbol': symbol,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        IOError: raised when `stocks.csv` file is missing or empty.

    """

    return eq.stocks_as_dict(country=country, columns=columns, as_json=as_json)


def get_stock_countries():
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

    return eq.stock_countries_as_list()


def get_stock_recent_data(stock, country, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced stock from Investing.com. So on, the recent data
    of the introduced stock from the specified coutry will be retrieved and returned as a :obj:`pandas.DataFrame` if 
    the parameters are valid and the request to Investing.com succeeds. Note that additionally some optional parameters 
    can be specified: as_json, order and debug, which let the user decide if the data is going to be returned as a 
    :obj:`json` or not, if the historical data is going to be ordered ascending or descending (where the index is the date) 
    and whether debug messages are going to be printed or not, respectively.

    Args:
        stock (:obj:`str`): name of the stock to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the stock is.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, either True or False, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            recent data of the specified stock from the specified country. So on, the resulting dataframe contains the 
            open, high, low, close and volume values for the selected stock on market days and the currency in which those
            values are presented.

            The resulting recent data, in case that the default parameters were applied, will look like::

                date || open | high | low | close | volume | currency
                -----||-----------------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but in case that as_json parameter was defined as True, then the output will be::

                {
                    name: name,
                    recent: [
                        dd/mm/yyyy: {
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        IOError: raised if stocks object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced stock/country was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if stock recent data was unavailable or not found in Investing.com.

    Examples:
        >>> investpy.get_recent_data(stock='bbva', country='spain')
                         Open   High    Low  Close    Volume Currency
            Date
            2019-08-13  4.263  4.395  4.230  4.353  27250000      EUR
            2019-08-14  4.322  4.325  4.215  4.244  36890000      EUR
            2019-08-15  4.281  4.298  4.187  4.234  21340000      EUR
            2019-08-16  4.234  4.375  4.208  4.365  46080000      EUR
            2019-08-19  4.396  4.425  4.269  4.269  18950000      EUR

    """

    if not stock:
        raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock name.")

    if not isinstance(stock, str):
        raise ValueError("ERR#0027: stock argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_stock_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

    stock = stock.strip()
    stock = stock.lower()

    if unidecode.unidecode(stock) not in [unidecode.unidecode(value.lower()) for value in stocks['name'].tolist()]:
        raise RuntimeError("ERR#0018: stock " + stock + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced stock on Investing.com')

    symbol = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'symbol']
    id_ = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'id']
    name = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'name']

    stock_currency = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'currency']

    logger.info(str(stock) + ' found on Investing.com')

    header = "Datos históricos " + symbol

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/instruments/HistoricalDataAjax"

    logger.info('Request sent to Investing.com!')

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        logger.info('Data parsing process starting...')

        for elements_ in path_:
            info = []
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.text_content())

            if info[0] == 'No se encontraron resultados':
                raise IndexError("ERR#0007: stock information unavailable or not found.")

            stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
            stock_close = float(info[1].replace('.', '').replace(',', '.'))
            stock_open = float(info[2].replace('.', '').replace(',', '.'))
            stock_high = float(info[3].replace('.', '').replace(',', '.'))
            stock_low = float(info[4].replace('.', '').replace(',', '.'))

            stock_volume = 0

            if info[5].__contains__('K'):
                stock_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
            elif info[5].__contains__('M'):
                stock_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
            elif info[5].__contains__('B'):
                stock_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)

            result.insert(len(result),
                          Data(stock_date, stock_open, stock_high, stock_low,
                               stock_close, stock_volume, stock_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {'name': name,
                     'recent':
                         [value.stock_as_json() for value in result]
                     }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.stock_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_stock_historical_data(stock, country, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced stock from Investing.com. So on, the historical data
    of the introduced stock from the specified coutry in the specified data range will be retrieved and returned as 
    a :obj:`pandas.DataFrame` if the parameters are valid and the request to Investing.com succeeds. Note that additionally 
    some optional parameters can be specified: as_json, order and debug, which let the user decide if the data is going to 
    be returned as a :obj:`json` or not, if the historical data is going to be ordered ascending or descending (where the 
    index is the date) and whether debug messages are going to be printed or not, respectively.

    Args:
        stock (:obj:`str`): name of the stock to retrieve historical data from.
        country (:obj:`str`): name of the country from where the stock is.
        from_date (:obj:`str`): date formatted as `dd/mm/yyyy`, since when data is going to be retrieved.
        to_date (:obj:`str`): date formatted as `dd/mm/yyyy`, until when data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, either True or False, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified stock via argument. The dataset contains the open, high, low, close and
            volume values for the selected stock on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | volume | currency
                -----||-----------------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    full_name: full_name,
                    historical: [
                        dd/mm/yyyy: {
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        IOError: raised if stocks object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced stock/country was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if stock historical data was unavailable or not found in Investing.com.

    Examples:
        >>> investpy.get_historical_data(stock='bbva', country='spain', from_date='01/01/2010', to_date='01/01/2019')
                         Open   High    Low  Close  Volume Currency
            Date
            2010-01-04  12.73  12.96  12.73  12.96       0      EUR
            2010-01-05  13.00  13.11  12.97  13.09       0      EUR
            2010-01-06  13.03  13.17  13.02  13.12       0      EUR
            2010-01-07  13.02  13.11  12.93  13.05       0      EUR
            2010-01-08  13.12  13.22  13.04  13.18       0      EUR

    """

    if not stock:
        raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock name.")

    if not isinstance(stock, str):
        raise ValueError("ERR#0027: stock argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    try:
        datetime.datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

    date_interval = {
        'intervals': [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 20:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_stock_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

    stock = stock.strip()
    stock = stock.lower()

    if unidecode.unidecode(stock) not in [unidecode.unidecode(value.lower()) for value in stocks['name'].tolist()]:
        raise RuntimeError("ERR#0018: stock " + stock + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced stock on Investing.com')

    symbol = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'symbol']
    id_ = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'id']
    name = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'name']

    stock_currency = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'currency']

    logger.info(str(stock) + ' found on Investing.com')

    final = list()

    logger.info('Data parsing process starting...')

    header = "Datos históricos " + symbol

    for index in range(len(date_interval['intervals'])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://es.investing.com/instruments/HistoricalDataAjax"

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        if not req.text:
            continue

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")

        result = list()

        if path_:
            for elements_ in path_:
                info = []
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.text_content())

                if info[0] == 'No se encontraron resultados':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0007: stock information unavailable or not found.")
                else:
                    data_flag = True

                if data_flag is True:
                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace('.', '').replace(',', '.'))
                    stock_open = float(info[2].replace('.', '').replace(',', '.'))
                    stock_high = float(info[3].replace('.', '').replace(',', '.'))
                    stock_low = float(info[4].replace('.', '').replace(',', '.'))

                    stock_volume = 0

                    if info[5].__contains__('K'):
                        stock_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        stock_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        stock_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)

                    result.insert(len(result),
                                  Data(stock_date, stock_open, stock_high, stock_low,
                                       stock_close, stock_volume, stock_currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.stock_as_json() for value in result]
                             }
                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.stock_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)

        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def get_stock_company_profile(stock, country='spain', language='english'):
    """
    This function retrieves the company profile of a stock company in the specified language. This
    function is really useful if NLP techniques want to be applied to stocks, since the company profile
    is a short description of what the company does and since it is written by the company, it can give
    the user an overview on what does the company do. The company profile can be retrieved either in english
    or in spanish, the only thing that changes is the source from where the data is retrieved, but the 
    resulting object will be the same. Note that this functionalliy as described in the docs is just supported
    for spanish stocks currently, so on, if any other stock from any other country is introduced as parameter, 
    the function will raise an exception.

    Args:
        stock (:obj:`str`): name of the stock to retrieve its company profile from.
        country (:obj:`str`): name of the country from where the stock is.
        language (:obj:`str`, optional): language in which the company profile is going to be retrieved, can either be english or spanish.

    Returns:
        :obj:`dict` - company_profile:
            The resulting :obj:`dict` contains the retrieved company profile from the selected source depending
            on the specified language in the function parameters, which can be either Investing.com (english) 
            or Bolsa de Madrid (spanish); and the URL from where it was retrieved, so to have both the source 
            and the description of the company_profile.

            So the resulting :obj:`dict` should look like::

                company_profile = {
                    url: 'https://www.investing.com/equities/bbva-company-profile',
                    desc: 'Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a ...'
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFound: raised if the `stocks.csv` file was not found or unable to retrieve.
        IOError: raised if stocks object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced stock/country was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.

    Examples:
        >>> investpy.get_equity_company_profile(stock='bbva', country='spain', language='english')
            company_profile = {
                url: 'https://www.investing.com/equities/bbva-company-profile',
                desc: 'Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a ...'
            }

    """

    available_sources = {
        'english': 'Investing',
        'en': 'Investing',
        'spanish': 'Bolsa de Madrid',
        'es': 'Bolsa de Madrid',
    }

    if not stock:
        raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock name.")

    if not isinstance(stock, str):
        raise ValueError("ERR#0027: stock argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if language.lower() not in available_sources.keys():
        raise ValueError("ERR#0014: the specified language is not valid, it can just be either spanish (es) or english (en).")

    if unidecode.unidecode(country.lower()) not in ['spain']:
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    selected_source = available_sources[language.lower()]

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

    stock = stock.strip()

    if unidecode.unidecode(stock.lower()) not in [unidecode.unidecode(value.lower()) for value in stocks['name'].tolist()]:
        raise RuntimeError("ERR#0018: stock " + stock.lower() + " not found, check if it is correct.")

    company_profile = {
        'url': None,
        'desc': None
    }

    if selected_source == 'Bolsa de Madrid':
        isin = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'isin']

        url = "http://www.bolsamadrid.es/esp/aspx/Empresas/FichaValor.aspx?ISIN=" + isin

        company_profile['url'] = url

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)

        path_ = root_.xpath(".//td[contains(@class, 'Perfil')]/p")

        if path_:
            text = list()
            for element_ in path_:
                if not element_.xpath(".//a"):
                    text.append(element_.text_content())

            text = ''.join(text)

            company_profile['desc'] = ' '.join(text.replace('\n', ' ').replace('\xa0', ' ').split())

            return company_profile
        else:
            return company_profile
    elif selected_source == 'Investing':
        tag = stocks.loc[(stocks['name'].str.lower() == stock).idxmax(), 'tag']

        url = "https://www.investing.com/equities/" + tag + "-company-profile"

        company_profile['url'] = url

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)

        path_ = root_.xpath(".//*[@id=\"profile-fullStory-showhide\"]")

        if path_:
            company_profile['desc'] = str(path_[0].text_content())

            return company_profile
        else:
            return company_profile


def get_stock_dividends(stock, country):
    """
    This function ...
    """

    if not stock:
        raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock symbol.")

    if not isinstance(stock, str):
        raise ValueError("ERR#0027: stock argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_stock_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

    stock = stock.strip()
    stock = stock.lower()

    if unidecode.unidecode(stock) not in [unidecode.unidecode(value.lower()) for value in stocks['symbol'].tolist()]:
        raise RuntimeError("ERR#0018: stock " + stock + " not found, check if it is correct.")

    tag_ = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'tag']

    headers = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://es.investing.com/equities/' + str(tag_) + '-dividends'

    req = requests.get(url=url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[contains(@id, 'dividendsHistoryData')]")

    more_results_id = path_[0].get('id').replace('dividendsHistoryData', '')

    path_ = root_.xpath(".//table[@id='dividendsHistoryData" + str(more_results_id) + "']/tbody/tr")

    objs = list()

    if path_:
        last_timestamp = path_[-1].get('event_timestamp')

        for elements_ in path_:
            for element_ in elements_.xpath(".//td"):
                if element_.get('class'):
                    if element_.get('class').__contains__('first'):
                        dividend_date = datetime.datetime.strptime(element_.text_content().strip().replace('.', '-'), '%d-%m-%Y')
                        dividend_value = float(element_.getnext().text_content().replace('.', '').replace(',', '.'))

                        obj = {
                            'Date': dividend_date,
                            'Dividend': dividend_value,
                        }

                        objs.append(obj)
        
        flag = True

        while flag is True:
            headers = {
                "User-Agent": user_agent.get_random(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            params = {
                'pairID': int(more_results_id),
                'last_timestamp': int(last_timestamp)
            }

            url = 'https://es.investing.com/equities/MoreDividendsHistory'

            req = requests.post(url=url, headers=headers, params=params)

            if req.status_code != 200:
                raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

            res = req.json()

            if res['hasMoreHistory'] is False:
                flag = False

            root_ = fromstring(res['historyRows'])
            path_ = root_.xpath(".//tr")

            if path_:
                last_timestamp = path_[-1].get('event_timestamp')

                for elements_ in path_:
                    for element_ in elements_.xpath(".//td"):
                        if element_.get('class'):
                            if element_.get('class').__contains__('first'):
                                dividend_date = datetime.datetime.strptime(element_.text_content().strip().replace('.', '-'), '%d-%m-%Y')
                                dividend_value = float(element_.getnext().text_content().replace('.', '').replace(',', '.'))

                                obj = {
                                    'Date': dividend_date,
                                    'Dividend': dividend_value,
                                }

                                objs.append(obj)

    df = pd.DataFrame(objs)
    return df


def search_stocks(by, value):
    """
    This function searches stocks by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced one for the specified field which is the
    `stocks.csv` column name to search in. Available fields to search stocks are 'name', 'full_name' and 'isin'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name which can be: 'name', 'full_name' or 'isin'.
        value (:obj:`str`): value of the field to search for, which is the value that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting :obj:`pandas.DataFrame` contains the search results from the given query, which is
            any match of the specified value in the specified field. If there are no results for the given query, 
            an error will be raised, but otherwise the resulting :obj:`pandas.DataFrame` will contain all the 
            available stocks that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised if no results were found for the introduced value in the introduced field.

    """

    available_search_fields = ['name', 'full_name', 'isin']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    stocks['matches'] = stocks[by].str.contains(value, case=False)

    search_result = stocks.loc[stocks['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result


"""------------- FUNDS -------------"""


def get_funds(country=None):
    """
    This function retrieves all the available `funds` from Investing.com and returns them as a :obj:`pandas.DataFrame`,
    which contains not just the fund names, but all the fields contained on the funds file.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available funds from.

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

    return fs.funds_as_df(country=country)


def get_funds_list(country=None):
    """
    This function retrieves all the available funds and returns a list of each one of them.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available funds from.

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

    return fs.funds_as_list(country=country)


def get_funds_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available funds on Investing.com and
    returns them as a :obj:`dict` containing the `asset_class`, `id`, `issuer`,
    `name`, `symbol` and `tag`. All the available funds can be found at:
    https://es.investing.com/etfs/spain-etfs

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available funds from.
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

    return fs.funds_as_dict(country=country, columns=columns, as_json=as_json)


def get_fund_countries():
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

    return fs.fund_countries_as_list()


def get_fund_recent_data(fund, country, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `fund` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        fund (:obj:`str`): name of the fund to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the introduced fund is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified fund via argument. The dataset contains the open, high, low and close
            values for the selected fund on market days.

            The return data is case we use default arguments will look like::

                date || open | high | low | close | currency
                -----||--------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        date: dd/mm/yyyy,
                        open: x,
                        high: x,
                        low: x,
                        close: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: funds object/file not found or unable to retrieve.
        RuntimeError: introduced fund does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.

    Examples:
        >>> investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp', country='spain', as_json=False, order='ascending', debug=False)
                         Open   High    Low  Close Currency
            Date
            2019-08-13  1.110  1.110  1.110  1.110      EUR
            2019-08-16  1.109  1.109  1.109  1.109      EUR
            2019-08-19  1.114  1.114  1.114  1.114      EUR
            2019-08-20  1.112  1.112  1.112  1.112      EUR
            2019-08-21  1.115  1.115  1.115  1.115      EUR

    """

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_fund_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    funds = funds[funds['country'] == unidecode.unidecode(country.lower())]

    fund = fund.strip()
    fund = fund.lower()

    if unidecode.unidecode(fund) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced fund on Investing.com')

    symbol = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'symbol']
    id_ = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'id']
    name = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'name']

    fund_currency = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'currency']

    logger.info(str(fund) + ' found on Investing.com')

    header = "Datos históricos " + symbol

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/instruments/HistoricalDataAjax"

    logger.info('Request sent to Investing.com!')

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        logger.info('Data parsing process starting...')

        for elements_ in path_:
            info = []
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.text_content())

            if info[0] == 'No se encontraron resultados':
                raise IndexError("ERR#0008: fund information unavailable or not found.")

            fund_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
            fund_close = float(info[1].replace('.', '').replace(',', '.'))
            fund_open = float(info[2].replace('.', '').replace(',', '.'))
            fund_high = float(info[3].replace('.', '').replace(',', '.'))
            fund_low = float(info[4].replace('.', '').replace(',', '.'))

            result.insert(len(result), Data(fund_date, fund_open, fund_high, fund_low,
                                            fund_close, None, fund_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {'name': name,
                     'recent':
                         [value.fund_as_json() for value in result]
                     }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_fund_historical_data(fund, country, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced `fund` from Investing
    via Web Scraping on the introduced date range. The resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` object with `ascending` or `descending` order.

    Args:
        fund (:obj:`str`): name of the fund to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the introduced fund is.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified fund via argument. The dataset contains the open, high, low and close
            values for the selected fund on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | currency
                -----||--------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: funds object/file not found or unable to retrieve.
        RuntimeError: introduced fund does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.

    Examples:
        >>> investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', country='spain', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)
                         Open   High    Low  Close Currency
            Date
            2018-02-15  1.105  1.105  1.105  1.105      EUR
            2018-02-16  1.113  1.113  1.113  1.113      EUR
            2018-02-17  1.113  1.113  1.113  1.113      EUR
            2018-02-18  1.113  1.113  1.113  1.113      EUR
            2018-02-19  1.111  1.111  1.111  1.111      EUR

    """

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    try:
        datetime.datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect start date format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

    date_interval = {
        'intervals': [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 20:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_fund_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    funds = funds[funds['country'] == unidecode.unidecode(country.lower())]

    fund = fund.strip()
    fund = fund.lower()

    if unidecode.unidecode(fund) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced fund on Investing.com')

    symbol = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'symbol']
    id_ = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'id']
    name = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'name']

    fund_currency = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'currency']

    logger.info(str(fund) + ' found on Investing.com')

    final = list()

    logger.info('Data parsing process starting...')

    header = "Datos históricos " + symbol

    for index in range(len(date_interval['intervals'])):
        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://es.investing.com/instruments/HistoricalDataAjax"

        logger.info('Request sent to Investing.com!')

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

        if not req.text:
            continue

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()

        if path_:
            for elements_ in path_:
                info = []
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.text_content())

                if info[0] == 'No se encontraron resultados':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0008: fund information unavailable or not found.")

                else:
                    data_flag = True

                if data_flag is True:
                    fund_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    fund_close = float(info[1].replace('.', '').replace(',', '.'))
                    fund_open = float(info[2].replace('.', '').replace(',', '.'))
                    fund_high = float(info[3].replace('.', '').replace(',', '.'))
                    fund_low = float(info[4].replace('.', '').replace(',', '.'))

                    result.insert(len(result), Data(fund_date, fund_open, fund_high, fund_low,
                                                    fund_close, None, fund_currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.fund_as_json() for value in result]
                             }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)

        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def get_fund_information(fund, country, as_json=False):
    """
    This function retrieves basic financial information from the specified fund.
    As the information is also provided by Investing.com, the tags and names remain the same so
    a new Web Scraping process is not needed, the headers can be created with the existing information.
    The retrieved information from the fund can be valuable as it is additional information that can
    be used combined with OHLC values, so to determine financial insights from the company which holds
    the specified fund.

    Args:
        fund (:obj:`str`): name of the fund to retrieve the financial information from.
        country (:obj:`str`): name of the country from where the introduced fund is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict`- fund_information:
            The resulting :obj:`dict` contains the information fields retrieved from Investing.com from the
            specified funds; it can also be returned as a :obj:`json`, if argument `as_json=True`.

            If any of the information fields could not be retrieved, that field/s will be filled with
            None values. If the retrieval process succeeded, the resulting :obj:`dict` will look like::

                fund_information = {
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
    """

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_fund_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    funds = funds[funds['country'] == unidecode.unidecode(country.lower())]

    fund = fund.strip()
    fund = fund.lower()

    if unidecode.unidecode(fund) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund + " not found, check if it is correct.")

    tag = funds.loc[(funds['name'].str.lower() == fund).idxmax(), 'tag']

    url = "https://es.investing.com/funds/" + tag

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath("//div[contains(@class, 'overviewDataTable')]/div")

    result = pd.DataFrame(columns=['Fund Name', 'Rating', '1-Year Change', 'Previous Close', 'Risk Rating',
                                   'TTM Yield', 'ROE', 'Issuer', 'Turnover', 'ROA', 'Inception Date',
                                   'Total Assets', 'Expenses', 'Min Investment', 'Market Cap', 'Category'])
    result.at[0, 'Fund Name'] = fund

    if path_:
        for elements_ in path_:
            title_ = elements_.xpath(".//span[@class='float_lang_base_1']")[0].text_content()

            if title_ == 'Rating':
                rating_score = 5 - len(elements_.xpath(".//span[contains(@class, 'morningStarsWrap')]/i[@class='morningStarLight']"))

                result.at[0, 'Rating'] = int(rating_score)
            elif title_ == 'Var. en un año':
                oneyear_variation = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content().replace(" ", "")

                result.at[0, '1-Year Change'] = oneyear_variation
            elif title_ == 'Último cierre':
                previous_close = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'Previous Close'] = previous_close

                if previous_close != 'N/A':
                    result.at[0, 'Previous Close'] = float(previous_close.replace('.', '').replace(',', '.'))
            elif title_ == 'Calificación de riesgo':
                risk_score = 5 - len(elements_.xpath(".//span[contains(@class, 'morningStarsWrap')]/i[@class='morningStarLight']"))

                result.at[0, 'Risk Rating'] = int(risk_score)
            elif title_ == 'Rendimiento año móvil':
                ttm_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'TTM Yield'] = ttm_percentage
            elif title_ == 'ROE':
                roe_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'ROE'] = roe_percentage
            elif title_ == 'Emisor':
                issuer_name = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'Issuer'] = issuer_name.strip()
            elif title_ == 'Volumen de ventas':
                turnover_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'Turnover'] = turnover_percentage
            elif title_ == 'ROA':
                roa_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'ROA'] = roa_percentage
            elif title_ == 'Fecha de inicio':
                value = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                inception_date = datetime.datetime.strptime(value.replace('.', '/'), '%d/%m/%Y')

                result.at[0, 'Inception Date'] = inception_date.strftime('%d/%m/%Y')
            elif title_ == 'Total activos':
                total_assets = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                if total_assets != 'N/A':
                    if total_assets.__contains__('K'):
                        total_assets = int(float(total_assets.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif total_assets.__contains__('M'):
                        total_assets = int(float(total_assets.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    elif total_assets.__contains__('B'):
                        total_assets = int(float(total_assets.replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)
                    else:
                        total_assets = int(float(total_assets.replace('.', '')))

                result.at[0, 'Total Assets'] = total_assets
            elif title_ == 'Gastos':
                expenses_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'Expenses'] = expenses_percentage
            elif title_ == 'Inversión mínima':
                min_investment = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'Min Investment'] = min_investment

                if min_investment != 'N/A':
                    result.at[0, 'Min Investment'] = int(float(min_investment.replace('.', '')))
            elif title_ == 'Cap. mercado':
                market_cap = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                if market_cap != 'N/A':
                    if market_cap.__contains__('K'):
                        market_cap = int(float(market_cap.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif market_cap.__contains__('M'):
                        market_cap = int(float(market_cap.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    elif market_cap.__contains__('B'):
                        market_cap = int(float(market_cap.replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)
                    else:
                        market_cap = int(float(market_cap.replace('.', '')))

                result.at[0, 'Market Cap'] = market_cap
            elif title_ == 'Categoría':
                category_name = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()

                result.at[0, 'Category'] = category_name

        result.replace({'N/A': None}, inplace=True)

        if as_json is True:
            json_ = result.iloc[0].to_json()
            json_ = json.dumps(json_, sort_keys=False)

            return json_
        elif as_json is False:
            return result
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def search_funds(by, value):
    """
    This function searches funds by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced value for the specified field which is the
    `funds.csv` column name to search in. Available fields to search funds are 'name', 'symbol', 'issuer' and 'isin'.

    Args:
        by (:obj:`str`):
            name of the field to search for, which is the column name ('name', 'symbol', 'issuer' or 'isin').
        value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
            in the specified field). If there are no results and error will be raised, but otherwise this
            `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced params is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised if no results were found for the introduced value in the introduced field.
    """

    available_search_fields = ['name', 'symbol', 'issuer', 'isin']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    funds['matches'] = funds[by].str.contains(value, case=False)

    search_result = funds.loc[funds['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result


"""------------- ETFS -------------"""


def get_etfs(country=None):
    """
    This function retrieves all the available countries to retrieve etfs from, as the listed
    countries are the ones indexed on Investing.com. The purpose of this function is to list
    the countries which have available etfs according to Investing.com data, so to ease the
    etf retrieval process of a particular country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`pandas.DataFrame` - etfs:
            The resulting :obj:`pandas.DataFrame` contains all the etfs basic information stored on `etfs.csv`, since it
            was previously retrieved in `investpy.etfs.retrieve_etfs()`. Unless the country is specified, all the
            available etfs indexed on Investing.com is returned, but if it is specified, just the etfs from that country
            are returned.

            In the case that the file reading of `etfs.csv` or the retrieval process from Investing.com was
            successfully completed, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | symbol | tag | id | currency
                --------|------|--------|-----|----|----------
                xxxxxxx | xxxx | xxxxxx | xxx | xx | xxxxxxxx

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing.
    """

    return es.etfs_as_df(country=country)


def get_etfs_list(country=None):
    """
    This function retrieves all the available etfs indexed on Investing.com, already
    stored on `etfs.csv`, which if does not exists, will be created by `investpy.etfs.retrieve_etfs()`.
    This function also allows the users to specify which country do they want to retrieve data from or if they
    want to retrieve it from every listed country; so on, a listing of etfs will be returned. This function
    helps the user to get to know which etfs are available on Investing.com.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`list` - etfs_list:
            The resulting :obj:`list` contains the retrieved data from the `etfs.csv` file, which is
            a listing of the names of the etfs listed on Investing.com, which is the input for data
            retrieval functions as the name of the etf to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                etfs_list = ['Betashares U.S. Equities Strong Bear Currency Hedg',
                            'Betashares Active Australian Hybrids',
                            'Australian High Interest Cash', ...]

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing or empty.
    """

    return es.etfs_as_list(country=country)


def get_etfs_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available etfs indexed on Investing.com, already
    stored on `etfs.csv`, which if does not exists, will be created by `investpy.etfs.retrieve_etfs()`.
    This function also allows the user to specify which country do they want to retrieve data from,
    or from every listed country; the columns which the user wants to be included on the resulting
    :obj:`dict`; and the output of the function (:obj:`dict` or :obj:`json`).

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.
        columns (:obj:`list`, optional):
            names of the columns of the etf data to retrieve <country, country_code, id, name, symbol, tag>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - etfs_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'country': country,
                    'id': id,
                    'tag': tag,
                    'name': name,
                    'symbol': symbol,
                    'currency': currency
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing or empty.
    """

    return es.etfs_as_dict(country=country, columns=columns, as_json=as_json)


def get_etf_countries():
    """
    This function retrieves all the available countries to retrieve etfs from, as the listed
    countries are the ones indexed on Investing.com. The purpose of this function is to list
    the countries which have available etfs according to Investing.com data, so to ease the
    etf retrieval process of a particular country.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the countries listed on Investing.com with
            etfs available to retrieve data from.

            In the case that the file reading of `etf_countries.csv` which contains the names and codes of the countries
            with etfs was successfully completed, the resulting :obj:`list` will look like::

                countries = ['australia', 'austria', 'belgium', 'brazil', ...]

    Raises:
        FileNotFoundError: raised when `etf_countries.csv` file is missing.
    """

    return es.etf_countries_as_list()


def get_etf_recent_data(etf, country, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `etf` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        etf (:obj:`str`): name of the etf to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the etf is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified etf via argument. The dataset contains the open, high, low and close
            values for the selected etf on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | currency
                -----||--------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: etfs object/file not found or unable to retrieve.
        RuntimeError: introduced etf does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if etf information was unavailable or not found.

    Examples:
        >>> investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50', country='spain', as_json=False, order='ascending', debug=False)
                          Open    High     Low   Close Currency
            Date
            2019-08-13  33.115  33.780  32.985  33.585      EUR
            2019-08-14  33.335  33.335  32.880  32.905      EUR
            2019-08-15  32.790  32.925  32.455  32.845      EUR
            2019-08-16  33.115  33.200  33.115  33.305      EUR
            2019-08-19  33.605  33.735  33.490  33.685      EUR

    """

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_etf_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    etfs = etfs[etfs['country'] == unidecode.unidecode(country.lower())]

    etf = etf.strip()
    etf = etf.lower()

    if unidecode.unidecode(etf) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + etf + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced etf on Investing.com')

    symbol = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'symbol']
    id_ = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'id']
    name = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'name']

    etf_currency = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'currency']

    logger.info(str(etf) + ' found on Investing.com')

    header = "Datos históricos " + symbol

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/instruments/HistoricalDataAjax"

    logger.info('Request sent to Investing.com!')

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        logger.info('Data parsing process starting...')

        for elements_ in path_:
            info = []
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.text_content())

            if info[0] == 'No se encontraron resultados':
                raise IndexError("ERR#0010: etf information unavailable or not found.")

            etf_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
            etf_close = float(info[1].replace('.', '').replace(',', '.'))
            etf_open = float(info[2].replace('.', '').replace(',', '.'))
            etf_high = float(info[3].replace('.', '').replace(',', '.'))
            etf_low = float(info[4].replace('.', '').replace(',', '.'))

            result.insert(len(result), Data(etf_date, etf_open, etf_high, etf_low, etf_close, None, etf_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {'name': name,
                     'recent':
                         [value.etf_as_json() for value in result]
                     }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df

    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_etf_historical_data(etf, country, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced `etf` from Investing
    via Web Scraping on the introduced date range. The resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` object with `ascending` or `descending` order.

    Args:
        etf (:obj:`str`): name of the etf to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the etf is.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified etf via argument. The dataset contains the open, high, low and close
            values for the selected etf on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | currency
                -----||--------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: etfs object/file not found or unable to retrieve.
        RuntimeError: introduced etf does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if etf information was unavailable or not found.

    Examples:
        >>> investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50', country='spain', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)
                         Open   High    Low  Close Currency
            Date
            2011-12-07  23.70  23.70  23.70  23.62      EUR
            2011-12-08  23.53  23.60  23.15  23.04      EUR
            2011-12-09  23.36  23.60  23.36  23.62      EUR
            2011-12-12  23.15  23.26  23.00  22.88      EUR
            2011-12-13  22.88  22.88  22.88  22.80      EUR

    """

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    try:
        datetime.datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

    date_interval = {
        'intervals': [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 20:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_etf_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    etfs = etfs[etfs['country'] == unidecode.unidecode(country.lower())]

    etf = etf.strip()
    etf = etf.lower()

    if unidecode.unidecode(etf) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + str(etf) + " not found in " + str(country.lower()) + ", check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced etf on Investing.com')

    symbol = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'symbol']
    id_ = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'id']
    name = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'name']

    etf_currency = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'currency']

    logger.info(str(etf) + ' found on Investing.com')

    final = list()

    header = "Datos históricos " + symbol

    for index in range(len(date_interval['intervals'])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://es.investing.com/instruments/HistoricalDataAjax"

        logger.info('Request sent to Investing.com!')

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

        if not req.text:
            continue

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()

        if path_:
            logger.info('Data parsing process starting...')

            for elements_ in path_:
                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.text_content())

                if info[0] == 'No se encontraron resultados':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0010: etf information unavailable or not found.")
                else:
                    data_flag = True

                if data_flag is True:
                    etf_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    etf_close = float(info[1].replace('.', '').replace(',', '.'))
                    etf_open = float(info[2].replace('.', '').replace(',', '.'))
                    etf_high = float(info[3].replace('.', '').replace(',', '.'))
                    etf_low = float(info[4].replace('.', '').replace(',', '.'))

                    result.insert(len(result),
                                  Data(etf_date, etf_open, etf_high, etf_low, etf_close, None, etf_currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.etf_as_json() for value in result]
                             }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)

        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def get_etfs_overview(country, as_json=False):
    """
    This function retrieves an object containing all the real time data available for all the ETFs from a country,
    such as the ETF names, symbols, current value, etc. as indexed in Investing.com. So on, the main usage of this
    function is to get an overview on all the available ETFs from a country.

    Args:
        country (:obj:`str`): name of the country to retrieve all its available etf data from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).

    Returns:
        :obj:`pandas.DataFrame` - etfs_overview:
            The resulting :obj:`pandas.DataFrame` contains all the data available in Investing.com from all the ETFs
            from a country in order to get an overview of it.

            If the retrieval process succeeded, the resulting :obj:`pandas.DataFrame` should look like::

                name | symbol | last | change | turnover
                ----------------------------------------
                xxxx | xxxxxx | xxxx | xxxxxx | xxxxxxxx
    Raises:
        ValueError: raised if there was any argument error.
        FileNotFoundError:  raised when `etf_countries.csv` file is missing.
        RuntimeError: raised it the introduced country does not match any of the indexed ones.
        ConnectionError: raised if GET requests does not return 200 status code.
    """

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    if unidecode.unidecode(country.lower()) not in get_etf_countries():
        raise RuntimeError('ERR#0025: specified country value not valid.')

    url = "https://es.investing.com/etfs/" + unidecode.unidecode(country.lower()).replace(" ", "-") + "-etfs"

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='etfs']"
                        "/tbody"
                        "/tr")

    results = list()

    if path_:
        for element_ in path_:
            id_ = element_.get('id').replace('pair_', '')
            symbol = element_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

            name = element_.xpath(".//a")[0].text.strip()

            last_path = ".//td[@class='" + 'pid-' + str(id_) + '-last' + "']"
            last = element_.xpath(last_path)[0].text_content()

            change_path = ".//td[contains(@class, '" + 'pid-' + str(id_) + '-pcp' + "')]"
            change = element_.xpath(change_path)[0].text_content()

            turnover_path = ".//td[contains(@class, '" + 'pid-' + str(id_) + '-turnover' + "')]"
            turnover = element_.xpath(turnover_path)[0].text_content()

            if turnover == '':
                continue

            if turnover.__contains__('K'):
                turnover = int(float(turnover.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
            elif turnover.__contains__('M'):
                turnover = int(float(turnover.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
            else:
                turnover = int(float(turnover.replace('.', '').replace(',', '.')))

            data = {
                "name": name,
                "symbol": symbol,
                "last": float(last.replace('.', '').replace(',', '.')),
                "change": change,
                "turnover": turnover,
            }

            results.append(data)

    df = pd.DataFrame(results)

    if as_json:
        return df.to_json(orient='records')
    else:
        return df


def search_etfs(by, value):
    """
    This function searches etfs by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced value for the specified field which is the
    `etfs.csv` column name to search in. Available fields to search etfs are 'name' and 'symbol'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name ('name' or 'symbol').
        value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
            in the specified field). If there are no results and error will be raised, but otherwise this
            `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced params is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised if no results were found for the introduced value in the introduced field.
    """

    available_search_fields = ['name', 'symbol']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    etfs['matches'] = etfs[by].str.contains(value, case=False)

    search_result = etfs.loc[etfs['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result


"""------------- INDICES -------------"""


def get_indices(country=None):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`pandas.DataFrame` with all the information of every available index. If the country
    filtering is applied, just the indices from the introduced country are going to be returned.
    All the available indices can be found at: https://es.investing.com/indices/world-indices and at
    https://es.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`pandas.DataFrame` - indices_df:
            The resulting :obj:`pandas.DataFrame` contains all the indices information retrieved from Investing.com,
            as previously listed by investpy.

            In case the information was successfully retrieved, the :obj:`pandas.DataFrame` will look like::

                country | name | full_name | symbol | currency | class | market
                --------|------|-----------|--------|----------|-------|--------
                xxxxxxx | xxxx | xxxxxxxxx | xxxxxx | xxxxxxxx | xxxxx | xxxxxx

    Raises:
        ValueError: raised if any of the introduced parameters is missing or errored.
        IOError: raised if the indices file from `investpy` is missing or errored.
    """

    return ic.indices_as_df(country=country)


def get_indices_list(country=None):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`list` with the names of every available index. If the country filtering is applied, just
    the indices from the introduced country are going to be returned.
    All the available indices can be found at: https://es.investing.com/indices/world-indices and at
    https://es.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`list` - indices_list:
            The resulting :obj:`list` contains the retrieved data, which corresponds to the index names of
            every index listed in Investing.com.

            In case the information was successfully retrieved, the :obj:`list` will look like::

                indices = ['S&P Merval', 'S&P Merval Argentina', 'S&P/BYMA Argentina General', ...]

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: raised if the indices file from `investpy` is missing or errored.
    """

    return ic.indices_as_list(country=country)


def get_indices_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`dict` with all the information of every available index. If the country
    filtering is applied, just the indices from the introduced country are going to be returned. Additionally, the
    columns to retrieve data from can be specified as a parameter formatted as a :obj:`list`.
    All the available indices can be found at: https://es.investing.com/indices/world-indices and at
    https://es.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.
        columns (:obj:`list` of :obj:`str`, optional): description
            a :obj:`list` containing the column names from which the data is going to be retrieved.
        as_json (:obj:`bool`, optional): description
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - indices_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'symbol': symbol,
                    'tag': tag,
                    'id': id,
                    'currency': currency
                }

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: raised if the indices file from `investpy` is missing or errored.
    """

    return ic.indices_as_dict(country=country, columns=columns, as_json=as_json)


def get_index_countries():
    """
    This function retrieves all the country names indexed in Investing.com with available indices to retrieve data
    from, via reading the `indices.csv` file from the resources directory. So on, this function will display a listing 
    containing a set of countries, in order to let the user know which countries are available for indices data retrieval.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with indices as indexed in Investing.com

    Raises:
        FileNotFoundError: raised if `indices.csv` file was unavailable or not found.
        IOError: raised if indices were not found.
    """

    return ic.index_countries_as_list()


def get_index_recent_data(index, country, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `index` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        index (:obj:`str`): name of the index to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the index is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified index via argument. The dataset contains the open, high, low, close and volume
            values for the selected index on market days, additionally the currency value is returned.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Volume | Currency
                -----||------|------|-----|-------|--------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised if there was an argument error.
        IOError: raised if indices object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced index does not match any of the indexed ones.
        ConnectionError: raised if GET requests does not return 200 status code.
        IndexError: raised if index information was unavailable or not found.

    Examples:
        >>> investpy.get_index_recent_data(index='ibex 35', country='spain')
                           Open     High      Low    Close   Volume Currency
            Date
            2019-08-26  12604.7  12646.3  12510.4  12621.3  4770000      EUR
            2019-08-27  12618.3  12723.3  12593.6  12683.8  8230000      EUR
            2019-08-28  12657.2  12697.2  12585.1  12642.5  7300000      EUR
            2019-08-29  12637.2  12806.6  12633.8  12806.6  5650000      EUR
            2019-08-30  12767.6  12905.9  12756.9  12821.6  6040000      EUR

    """

    if not index:
        raise ValueError("ERR#0047: index param is mandatory and should be a str.")

    if not isinstance(index, str):
        raise ValueError("ERR#0047: index param is mandatory and should be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_index_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    indices = indices[indices['country'] == unidecode.unidecode(country.lower())]

    index = index.strip()
    index = index.lower()

    if unidecode.unidecode(index) not in [unidecode.unidecode(value.lower()) for value in indices['name'].tolist()]:
        raise RuntimeError("ERR#0045: index " + index + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced index on Investing.com')

    full_name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'full_name']
    id_ = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'id']
    name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'name']

    index_currency = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'currency']

    logger.info(str(index) + ' found on Investing.com')

    header = "Datos históricos " + full_name

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/instruments/HistoricalDataAjax"

    logger.info('Request sent to Investing.com!')

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        logger.info('Data parsing process starting...')

        for elements_ in path_:
            info = []
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.text_content())

            if info[0] == 'No se encontraron resultados':
                raise IndexError("ERR#0046: index information unavailable or not found.")

            index_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')

            index_close = float(info[1].replace('.', '').replace(',', '.'))
            index_open = float(info[2].replace('.', '').replace(',', '.'))
            index_high = float(info[3].replace('.', '').replace(',', '.'))
            index_low = float(info[4].replace('.', '').replace(',', '.'))

            index_volume = 0

            if info[5].__contains__('K'):
                index_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
            elif info[5].__contains__('M'):
                index_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
            elif info[5].__contains__('B'):
                index_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)

            result.insert(len(result), Data(index_date, index_open, index_high, index_low,
                                            index_close, index_volume, index_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {'name': name,
                     'recent':
                         [value.index_as_json() for value in result]
                     }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.index_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df

    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_index_historical_data(index, country, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data of the introduced `index` (from the specified country, note that both
    index and country should match since if the introduced index is not listed in the indices of that country, the
    function will raise an error). The retrieved historical data are the OHLC values plus the Volume and the Currency in
    which those values are specified, from the introduced data range if valid. So on, the resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` file.

    Args:
        index (:obj:`str`): name of the index to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the index is.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            historical data from the specified index via argument. The dataset contains the open, high, low, close and
            volume values for the selected index on market days, additionally the currency in which those values are
            specified is returned.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Volume | Currency
                -----||------------------------------------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised if there was an argument error.
        IOError: raised if indices object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced index does not match any of the indexed ones.
        ConnectionError: raised if GET requests does not return 200 status code.
        IndexError: raised if index information was unavailable or not found.

    Examples:
        >>> investpy.get_index_historical_data(index='ibex 35', country='spain', from_date='01/01/2018', to_date='01/01/2019')
                           Open     High      Low    Close    Volume Currency
            Date
            2018-01-02  15128.2  15136.7  14996.6  15096.8  10340000      EUR
            2018-01-03  15145.0  15186.9  15091.9  15106.9  12800000      EUR
            2018-01-04  15105.5  15368.7  15103.7  15368.7  17070000      EUR
            2018-01-05  15353.9  15407.5  15348.6  15398.9  11180000      EUR
            2018-01-08  15437.1  15448.7  15344.0  15373.3  12890000      EUR

    """

    if not index:
        raise ValueError("ERR#0047: index param is mandatory and should be a str.")

    if not isinstance(index, str):
        raise ValueError("ERR#0047: index param is mandatory and should be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    try:
        datetime.datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    date_interval = {
        'intervals': [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 20:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_index_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    indices = indices[indices['country'] == unidecode.unidecode(country.lower())]

    index = index.strip()
    index = index.lower()

    if unidecode.unidecode(index) not in [unidecode.unidecode(value.lower()) for value in indices['name'].tolist()]:
        raise RuntimeError("ERR#0045: index " + index + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced index on Investing.com')

    full_name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'full_name']
    id_ = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'id']
    name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'name']

    index_currency = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'currency']

    logger.info(str(index) + ' found on Investing.com')

    final = list()

    header = "Datos históricos " + full_name

    for index in range(len(date_interval['intervals'])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://es.investing.com/instruments/HistoricalDataAjax"

        logger.info('Request sent to Investing.com!')

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

        if not req.text:
            continue

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()

        if path_:
            logger.info('Data parsing process starting...')

            for elements_ in path_:
                info = []
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.text_content())

                if info[0] == 'No se encontraron resultados':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0046: index information unavailable or not found.")
                else:
                    data_flag = True

                if data_flag is True:
                    index_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')

                    index_close = float(info[1].replace('.', '').replace(',', '.'))
                    index_open = float(info[2].replace('.', '').replace(',', '.'))
                    index_high = float(info[3].replace('.', '').replace(',', '.'))
                    index_low = float(info[4].replace('.', '').replace(',', '.'))

                    index_volume = 0

                    if info[5].__contains__('K'):
                        index_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        index_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        index_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)

                    result.insert(len(result), Data(index_date, index_open, index_high, index_low,
                                                    index_close, index_volume, index_currency))
            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.index_as_json() for value in result]
                             }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.index_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)
        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def search_indices(by, value):
    """
    This function searches indices by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced value for the specified field which is the
    `indices.csv` column name to search in. Available fields to search indices are 'name', 'full_name' and 'symbol'.

    Args:
       by (:obj:`str`): name of the field to search for, which is the column name ('name', 'full_name' or 'symbol').
       value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
       :obj:`pandas.DataFrame` - search_result:
           The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
           in the specified field). If there are no results and error will be raised, but otherwise this
           `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
       ValueError: raised if any of the introduced params is not valid or errored.
       IOError: raised if data could not be retrieved due to file error.
       RuntimeError: raised if no results were found for the introduced value in the introduced field.
    """

    available_search_fields = ['name', 'full_name', 'symbol']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    indices['matches'] = indices[by].str.contains(value, case=False)

    search_result = indices.loc[indices['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result


"""------------- CURRENCY CROSSES -------------"""


def get_currency_crosses(base=None, second=None):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`pandas.DataFrame`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file. Note that the filtering params are both base and second, which mean the base and the
    second currency of the currency cross, for example, in the currency cross `EUR/USD` the base currency is EUR and
    the second currency is USD. These are optional parameters, so specifying one of them means that all the currency
    crosses where the introduced currency is either base or second will be returned; if both are specified,
    just the introduced currency cross will be returned if it exists. All the available currency crosses can be found
    at: https://es.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.

    Returns:
        :obj:`pandas.DataFrame` - currency_crosses_df:
            The resulting :obj:`pandas.DataFrame` contains all the currency crosses basic information retrieved from
            Investing.com, some of which is not useful for the user, but for the inner package functions, such as the
            `tag` or `id` fields.

            In case the information was successfully retrieved, the resulting :obj:`pandas.DataFrame` will look like::

                name | full_name | tag | id | base | second | base_name | second_name
                -----|-----------|-----|----|------|--------|-----------|-------------
                xxxx | xxxxxxxxx | xxx | xx | xxxx | xxxxxx | xxxxxxxxx | xxxxxxxxxxx

            Just like `investpy.currency_crosses.retrieve_currencies()`, the output of this function is a
            :obj:`pandas.DataFrame` containing all the currency crosses as indexed in Investing.com, but instead of
            scraping the web in order to retrieve them and then generating the CSV file, this function just reads it
            and loads it into a :obj:`pandas.DataFrame`.

    Raises:
        IOError: raised if currency_crosses retrieval failed, both for missing file or empty file.
    """

    return cc.currency_crosses_as_df(base=base, second=second)


def get_currency_crosses_list(base=None, second=None):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`dict`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file is columns is None, otherwise, just the specified column values will be returned. Note
    that the filtering params are both base and second, which mean the base and the second currency of the currency
    cross, for example, in the currency cross `EUR/USD` the base currency is EUR and the second currency is USD. These
    are optional parameters, so specifying one of them means that all the currency crosses where the introduced
    currency is either base or second will be returned; if both are specified, just the introduced currency cross will
    be returned if it exists. All the available currency crosses can be found at: https://es.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.

    Returns:
        :obj:`list` - currency_crosses_list:
            The resulting :obj:`list` contains the retrieved data from the `currency_crosses.csv` file, which is
            a listing of the names of the currency crosses listed in Investing.com, which is the input for data
            retrieval functions as the name of the currency cross to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                currency_crosses_list = [
                    'USD/BRLT', 'CAD/CHF', 'CHF/CAD', 'CAD/PLN', 'PLN/CAD', ...
                ]

    Raises:
        IOError: raised if currency_crosses retrieval failed, both for missing file or empty file.
    """

    return cc.currency_crosses_as_list(base=base, second=second)


def get_currency_crosses_dict(base=None, second=None, columns=None, as_json=False):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`dict`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file is columns is None, otherwise, just the specified column values will be returned. Note
    that the filtering params are both base and second, which mean the base and the second currency of the currency
    cross, for example, in the currency cross `EUR/USD` the base currency is EUR and the second currency is USD. These
    are optional parameters, so specifying one of them means that all the currency crosses where the introduced
    currency is either base or second will be returned; if both are specified, just the introduced currency cross will
    be returned if it exists. All the available currency crosses can be found at: https://es.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.
        columns (:obj:`list`, optional):
            names of the columns of the stock data to retrieve <name, full_name, tag, id, base, base_name,
            second, second_name>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

    Returns:
        :obj:`dict` or :obj:`json` - currency_crosses_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'name': name,
                    'full_name': full_name,
                    'tag': tag,
                    'id': id,
                    'base': base,
                    'base_name': base_name,
                    'second': second,
                    'second_name': second_name
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
       IOError: raised if currency_crosses retrieval failed, both for missing file or empty file.
    """

    return cc.currency_crosses_as_dict(base=base, second=second, columns=columns, as_json=as_json)


def get_available_currencies():
    """
    This function retrieves a listing with all the available currencies with indexed currency crosses in order to
    get to know which are the available currencies. The currencies listed in this function, so on, can be used to
    search currency crosses and used the retrieved data to get historical data of those currency crosses, so to
    determine which is the value of one base currency in the second currency.

    Returns:
        :obj:`list` - available_currencies:
            The resulting :obj:`list` contains all the available currencies with currency crosses being either the base
            or the second value of the cross, as listed in Investing.com.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                available_currencies = [
                    'AED', 'AFN', 'ALL', 'AMD', 'ANG', ...
                ]

    Raises:
        IndexError: raised if `currency_crosses.csv` file was unavailable or not found.
    """

    return cc.available_currencies_as_list()


def get_currency_cross_recent_data(currency_cross, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `currency_cross` as indexed in Investing.com
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        currency_cross (:obj:`str`): name of the currency_cross to retrieve recent historical data from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified currency_cross via argument. The dataset contains the open, high, low, close,
            volume and currency values for the selected currency_cross on market days.

            The return data is in case we use default arguments will look like::

                date || open | high | low | close | volume | currency
                -----||------------------------------------|---------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        dd/mm/yyyy: {
                            'open': x,
                            'high': x,
                            'low': x,
                            'close': x,
                            'volume': x,
                            'currency' : x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised if any of the introduced arguments was not valid or errored.
        IOError: raised if currency_crosses object/file not found or unable to retrieve.
        RuntimeError: raised introduced currency_cross does not match any of the indexed ones.
        ConnectionError: raised if GET request did not return 200 status code.
        IndexError: raised if currency_cross information was unavailable or not found.

    Examples:
        >>> investpy.get_currency_cross_recent_data(currency_cross='EUR/USD')
                          Open    High     Low   Close  Volume Currency
            Date
            2019-08-27  1.1101  1.1116  1.1084  1.1091       0      USD
            2019-08-28  1.1090  1.1099  1.1072  1.1078       0      USD
            2019-08-29  1.1078  1.1093  1.1042  1.1057       0      USD
            2019-08-30  1.1058  1.1062  1.0963  1.0991       0      USD
            2019-09-02  1.0990  1.1000  1.0958  1.0968       0      USD

    """

    if not currency_cross:
        raise ValueError("ERR#0052: currency_cross param is mandatory and should be a str.")

    if not isinstance(currency_cross, str):
        raise ValueError("ERR#0052: currency_cross param is mandatory and should be a str.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0060: currency_crosses file not found or errored.")

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    currency_cross = currency_cross.strip()
    currency_cross = currency_cross.lower()

    if unidecode.unidecode(currency_cross) not in [unidecode.unidecode(value.lower()) for value in currency_crosses['name'].tolist()]:
        raise RuntimeError("ERR#0054: the introduced currency_cross " + str(currency_cross) + " does not exists.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced currency_cross on Investing.com')

    id_ = currency_crosses.loc[(currency_crosses['name'].str.lower() == currency_cross).idxmax(), 'id']
    name = currency_crosses.loc[(currency_crosses['name'].str.lower() == currency_cross).idxmax(), 'name']
    currency = currency_crosses.loc[(currency_crosses['name'].str.lower() == currency_cross).idxmax(), 'second']

    logger.info(str(currency_cross) + ' found on Investing.com')

    header = "Datos históricos " + name

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/instruments/HistoricalDataAjax"

    logger.info('Request sent to Investing.com!')

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        logger.info('Data parsing process starting...')

        for elements_ in path_:
            info = []
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.text_content())

            if info[0] == 'No se encontraron resultados':
                raise IndexError("ERR#0055: currency_cross information unavailable or not found.")

            currency_cross_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
            currency_cross_close = float(info[1].replace('.', '').replace(',', '.'))
            currency_cross_open = float(info[2].replace('.', '').replace(',', '.'))
            currency_cross_high = float(info[3].replace('.', '').replace(',', '.'))
            currency_cross_low = float(info[4].replace('.', '').replace(',', '.'))

            currency_cross_volume = 0

            if info[5].__contains__('K'):
                currency_cross_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
            elif info[5].__contains__('M'):
                currency_cross_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
            elif info[5].__contains__('B'):
                currency_cross_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)

            result.insert(len(result),
                          Data(currency_cross_date, currency_cross_open, currency_cross_high, currency_cross_low,
                               currency_cross_close, currency_cross_volume, currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {
                'name': name,
                'recent': [value.currency_cross_as_json() for value in result]
            }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.currency_cross_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_currency_cross_historical_data(currency_cross, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `currency_cross` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        currency_cross (:obj:`str`): name of the currency cross to retrieve recent historical data from.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified currency_cross via argument. The dataset contains the open, high, low, close and
            volume values for the selected currency_cross on market days.

            The return data is case we use default arguments will look like::

                date || open | high | low | close | volume | currency
                -----||------------------------------------|---------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        dd/mm/yyyy: {
                            'open': x,
                            'high': x,
                            'low': x,
                            'close': x,
                            'volume': x,
                            'currency' : x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: stocks object/file not found or unable to retrieve.
        RuntimeError: introduced currency_cross does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if currency_cross information was unavailable or not found.

    Examples:
        >>> investpy.get_currency_cross_historical_data(currency_cross='EUR/USD', from_date='01/01/2018', to_date='01/01/2019')
                          Open    High     Low   Close  Volume Currency
            Date
            2018-01-01  1.2003  1.2014  1.1995  1.2010       0      USD
            2018-01-02  1.2013  1.2084  1.2003  1.2059       0      USD
            2018-01-03  1.2058  1.2070  1.2001  1.2014       0      USD
            2018-01-04  1.2015  1.2090  1.2004  1.2068       0      USD
            2018-01-05  1.2068  1.2085  1.2021  1.2030       0      USD

    """

    if not currency_cross:
        raise ValueError("ERR#0052: currency_cross param is mandatory and should be a str.")

    if not isinstance(currency_cross, str):
        raise ValueError("ERR#0052: currency_cross param is mandatory and should be a str.")

    try:
        datetime.datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    date_interval = {
        'intervals': [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 20:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0060: currency_crosses file not found or errored.")

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    currency_cross = currency_cross.strip()
    currency_cross = currency_cross.lower()

    if unidecode.unidecode(currency_cross) not in [unidecode.unidecode(value.lower()) for value in currency_crosses['name'].tolist()]:
        raise RuntimeError("ERR#0054: the introduced currency_cross " + str(currency_cross) + " does not exists.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced currency_cross on Investing.com')

    id_ = currency_crosses.loc[(currency_crosses['name'].str.lower() == currency_cross).idxmax(), 'id']
    name = currency_crosses.loc[(currency_crosses['name'].str.lower() == currency_cross).idxmax(), 'name']
    currency = currency_crosses.loc[(currency_crosses['name'].str.lower() == currency_cross).idxmax(), 'second']

    logger.info(str(currency_cross) + ' found on Investing.com')

    final = list()

    header = "Datos históricos " + name

    for index in range(len(date_interval['intervals'])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://es.investing.com/instruments/HistoricalDataAjax"

        logger.info('Request sent to Investing.com!')

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()

        if path_:
            logger.info('Data parsing process starting...')

            for elements_ in path_:
                info = []
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.text_content())

                if info[0] == 'No se encontraron resultados':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0055: currency_cross information unavailable or not found.")
                else:
                    data_flag = True

                if data_flag is True:
                    currency_cross_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')

                    currency_cross_close = float(info[1].replace('.', '').replace(',', '.'))
                    currency_cross_open = float(info[2].replace('.', '').replace(',', '.'))
                    currency_cross_high = float(info[3].replace('.', '').replace(',', '.'))
                    currency_cross_low = float(info[4].replace('.', '').replace(',', '.'))

                    currency_cross_volume = 0

                    if info[5].__contains__('K'):
                        currency_cross_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        currency_cross_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        currency_cross_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)

                    result.insert(len(result),
                                  Data(currency_cross_date, currency_cross_open, currency_cross_high, currency_cross_low,
                                       currency_cross_close, currency_cross_volume, currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.currency_cross_as_json() for value in result]
                             }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.currency_cross_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)
        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def search_currency_crosses(by, value):
    """
    This function searches currency crosses by the introduced value for the specified field. This means that this
    function is going to search if there is a value that matches the introduced value for the specified field which is
    the `currency_crosses.csv` column name to search in. Available fields to search indices are 'name', 'full_name',
    'base', 'second', 'base_name' and 'second_name'.

    Args:
        by (:obj:`str`):
            name of the field to search for, which is the column name ('name', 'full_name', 'base', 'second',
            'base_name' or 'second_name').
        value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
       :obj:`pandas.DataFrame` - search_result:
           The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
           in the specified field). If there are no results and error will be raised, but otherwise this
           `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
       ValueError: raised if any of the introduced params is not valid or errored.
       IOError: raised if data could not be retrieved due to file error.
       RuntimeError: raised if no results were found for the introduced value in the introduced field.
    """

    available_search_fields = ['name', 'full_name', 'base', 'second', 'base_name', 'second_name']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0060: currency_crosses file not found or errored.")

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    currency_crosses['matches'] = currency_crosses[by].str.contains(value, case=False)

    search_result = currency_crosses.loc[currency_crosses['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + ' value.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
