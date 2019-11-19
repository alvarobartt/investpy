#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy.utils.user_agent import get_random
from investpy.utils.data import Data

from investpy.data.stocks_data import stocks_as_df, stocks_as_list, stocks_as_dict
from investpy.data.stocks_data import stock_countries_as_list


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

                country | name | full name | isin | currency | symbol
                --------|------|-----------|------|----------|--------
                xxxxxxx | xxxx | xxxxxxxxx | xxxx | xxxxxxxx | xxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if stocks file was not found.
        IOError: raised when stocks file is missing or empty.

    """

    return stocks_as_df(country)


def get_stocks_list(country=None):
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
        FileNotFoundError: raised if stocks file was not found.
        IOError: raised when stocks file is missing or empty.
    
    """

    return stocks_as_list(country)


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
        columns (:obj:`list`, optional):column names of the stock data to retrieve, can be: <country, name, full_name, isin, currency, symbol>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - stocks_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every stock as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                stocks_dict = {
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
        FileNotFoundError: raised if stocks file was not found.
        IOError: raised when stocks file is missing or empty.

    """

    return stocks_as_dict(country=country, columns=columns, as_json=as_json)


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
        FileNotFoundError: raised if stock countries file was not found.
        IOError: raised when stock countries file is missing or empty.

    """

    return stock_countries_as_list()


def get_stock_recent_data(stock, country, as_json=False, order='ascending', interval='Daily'):
    """
    This function retrieves recent historical data from the introduced stock from Investing.com. So on, the recent data
    of the introduced stock from the specified country will be retrieved and returned as a :obj:`pandas.DataFrame` if
    the parameters are valid and the request to Investing.com succeeds. Note that additionally some optional parameters
    can be specified: as_json and order, which let the user decide if the data is going to be returned as a
    :obj:`json` or not, and if the historical data is going to be ordered ascending or descending (where the index is the 
    date), respectively.

    Args:
        stock (:obj:`str`): symbol of the stock to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the stock is.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            recent data of the specified stock from the specified country. So on, the resulting dataframe contains the
            open, high, low, close and volume values for the selected stock on market days and the currency in which those
            values are presented.

            The resulting recent data, in case that the default parameters were applied, will look like::

                Date || Open | High | Low | Close | Volume | Currency 
                -----||------|------|-----|-------|--------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx 

            but in case that as_json parameter was defined as True, then the output will be::

                {
                    name: name,
                    recent: [
                        {
                            date: 'dd/mm/yyyy',
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
        >>> investpy.get_stock_recent_data(stock='bbva', country='spain')
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

    if not interval:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if interval not in ['Daily', 'Weekly', 'Monthly']:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    resource_package = 'investpy'
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

    symbol = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'symbol']
    id_ = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'id']
    name = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'name']

    stock_currency = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'currency']

    header = symbol + ' Historical Data'

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": interval,
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/HistoricalDataAjax"

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        for elements_ in path_:
            if elements_.xpath(".//td")[0].text_content() == 'No results found':
                raise IndexError("ERR#0007: stock information unavailable or not found.")

            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get('data-real-value'))

            stock_date = datetime.fromtimestamp(int(info[0]))
            stock_date = date(stock_date.year, stock_date.month, stock_date.day)
            
            stock_close = float(info[1].replace(',', ''))
            stock_open = float(info[2].replace(',', ''))
            stock_high = float(info[3].replace(',', ''))
            stock_low = float(info[4].replace(',', ''))

            stock_volume = 0

            if info[5].__contains__('K'):
                stock_volume = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
            elif info[5].__contains__('M'):
                stock_volume = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
            elif info[5].__contains__('B'):
                stock_volume = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

            result.insert(len(result),
                          Data(stock_date, stock_open, stock_high, stock_low,
                               stock_close, stock_volume, stock_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        if as_json is True:
            json_ = {
                'name': name,
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


def get_stock_historical_data(stock, country, from_date, to_date, as_json=False, order='ascending', interval='Daily'):
    """
    This function retrieves historical data from the introduced stock from Investing.com. So on, the historical data
    of the introduced stock from the specified country in the specified data range will be retrieved and returned as
    a :obj:`pandas.DataFrame` if the parameters are valid and the request to Investing.com succeeds. Note that additionally
    some optional parameters can be specified: as_json and order, which let the user decide if the data is going to
    be returned as a :obj:`json` or not, and if the historical data is going to be ordered ascending or descending (where the
    index is the date), respectively.

    Args:
        stock (:obj:`str`): symbol of the stock to retrieve historical data from.
        country (:obj:`str`): name of the country from where the stock is.
        from_date (:obj:`str`): date formatted as `dd/mm/yyyy`, since when data is going to be retrieved.
        to_date (:obj:`str`): date formatted as `dd/mm/yyyy`, until when data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            historical data of the specified stock from the specified country. So on, the resulting dataframe contains the
            open, high, low, close and volume values for the selected stock on market days and the currency in which those
            values are presented.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Volume | Currency 
                -----||------|------|-----|-------|--------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx 

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: 'dd/mm/yyyy',
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
        >>> investpy.get_stock_historical_data(stock='bbva', country='spain', from_date='01/01/2010', to_date='01/01/2019')
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

    if not interval:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if interval not in ['Daily', 'Weekly', 'Monthly']:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    try:
        datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.strptime(to_date, '%d/%m/%Y')

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
                'start': start_date.strftime('%m/%d/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%m/%d/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%m/%d/%Y'),
                'end': end_date.strftime('%m/%d/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = 'investpy'
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

    symbol = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'symbol']
    id_ = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'id']
    name = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'name']

    stock_currency = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'currency']

    final = list()

    header = symbol + ' Historical Data'

    for index in range(len(date_interval['intervals'])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": interval,
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/instruments/HistoricalDataAjax"

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
                if elements_.xpath(".//td")[0].text_content() == 'No results found':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0007: stock information unavailable or not found.")
                else:
                    data_flag = True
                
                info = []
            
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get('data-real-value'))

                if data_flag is True:
                    stock_date = datetime.fromtimestamp(int(info[0]))
                    stock_date = date(stock_date.year, stock_date.month, stock_date.day)
                    
                    stock_close = float(info[1].replace(',', ''))
                    stock_open = float(info[2].replace(',', ''))
                    stock_high = float(info[3].replace(',', ''))
                    stock_low = float(info[4].replace(',', ''))

                    stock_volume = 0

                    if info[5].__contains__('K'):
                        stock_volume = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
                    elif info[5].__contains__('M'):
                        stock_volume = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
                    elif info[5].__contains__('B'):
                        stock_volume = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

                    result.insert(len(result),
                                  Data(stock_date, stock_open, stock_high, stock_low,
                                       stock_close, stock_volume, stock_currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {
                        'name': name,
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
        stock (:obj:`str`): symbol of the stock to retrieve its company profile from.
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
        >>> investpy.get_stock_company_profile(stock='bbva', country='spain', language='english')
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
        raise ValueError(
            "ERR#0014: the specified language is not valid, it can just be either spanish (es) or english (en).")

    if unidecode.unidecode(country.lower()) not in ['spain']:
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    selected_source = available_sources[language.lower()]

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]

    stock = stock.strip()

    if unidecode.unidecode(stock.lower()) not in [unidecode.unidecode(value.lower()) for value in
                                                  stocks['symbol'].tolist()]:
        raise RuntimeError("ERR#0018: stock " + stock.lower() + " not found, check if it is correct.")

    company_profile = {
        'url': None,
        'desc': None
    }

    if selected_source == 'Bolsa de Madrid':
        isin = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'isin']

        url = "http://www.bolsamadrid.es/esp/aspx/Empresas/FichaValor.aspx?ISIN=" + isin

        company_profile['url'] = url

        head = {
            "User-Agent": get_random(),
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
        tag = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'tag']

        url = "https://www.investing.com/equities/" + tag + "-company-profile"

        company_profile['url'] = url

        head = {
            "User-Agent": get_random(),
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
    This function retrieves the stock dividends from the introduced stocks, which are token rewards paid to
    the shareholders for their investment in a company's stock/equity. Dividends data include date of the
    dividend, dividend value, type, payment date and yield. This information is really useful when it comes
    to creating portfolios.

    Args:
        stock (:obj:`str`): symbol of the stock to retrieve its dividends from.
        country (:obj:`country`): name of the country from where the stock is from.

    Returns:
        :obj:`pandas.DataFrame` - stock_dividends:
            Returns a :obj:`pandas.DataFrame` containing the retrieved information of stock dividends for every stock
            symbol introduced as parameter.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                         Date  Dividend                    Type Payment Date  Yield
                0  2019-10-11    0.2600  trailing_twelve_months   2019-10-15  5,67%
                1  2019-04-08    0.2600  trailing_twelve_months   2019-04-10  5,53%
                2  2018-06-11    0.3839  trailing_twelve_months   2018-06-13  3,96%
                3  2018-04-06    0.2400  trailing_twelve_months   2018-04-10  4,41%
                4  2017-10-06    0.3786  trailing_twelve_months   2017-10-10  4,45%

    """

    if not stock:
        raise ValueError("ERR#0013: stock parameter is mandatory and must be a valid stock symbol.")

    if not isinstance(stock, str):
        raise ValueError("ERR#0027: stock argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_stock_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    stocks = stocks[stocks['country'].str.lower() == unidecode.unidecode(country.lower())]

    stock = stock.strip()
    stock = stock.lower()

    if unidecode.unidecode(stock) not in [unidecode.unidecode(value.lower()) for value in stocks['symbol'].tolist()]:
        raise RuntimeError("ERR#0018: stock " + stock + " not found, check if it is correct.")

    tag_ = stocks.loc[(stocks['symbol'].str.lower() == stock).idxmax(), 'tag']

    headers = {
        "User-Agent": get_random(),
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

    if path_:
        more_results_id = path_[0].get('id').replace('dividendsHistoryData', '')

        path_ = root_.xpath(".//table[@id='dividendsHistoryData" + str(more_results_id) + "']/tbody/tr")

        objs = list()

        type_values = {
            '1': 'monthly',
            '2': 'quarterly',
            '3': 'semi_annual',
            '4': 'annual',
            '5': 'trailing_twelve_months',
        }

        if path_:
            last_timestamp = path_[-1].get('event_timestamp')

            for elements_ in path_:
                dividend_date = dividend_value = dividend_type = dividend_payment_date = dividend_yield = None
                for element_ in elements_.xpath(".//td"):
                    if element_.get('class'):
                        if element_.get('class').__contains__('first'):
                            dividend_date = datetime.strptime(element_.text_content().strip().replace('.', '-'), '%d-%m-%Y')
                            dividend_value = float(element_.getnext().text_content().replace('.', '').replace(',', '.'))
                        if element_.get('data-value') in type_values.keys():
                            dividend_type = type_values[element_.get('data-value')]
                            dividend_payment_date = datetime.strptime(element_.getnext().text_content().strip().replace('.', '-'), '%d-%m-%Y')
                            next_element_ = element_.getnext()
                            dividend_yield = next_element_.getnext().text_content()

                obj = {
                    'Date': dividend_date,
                    'Dividend': dividend_value,
                    'Type': dividend_type,
                    'Payment Date': dividend_payment_date,
                    'Yield': dividend_yield,
                }

                objs.append(obj)

            flag = True

            while flag is True:
                headers = {
                    "User-Agent": get_random(),
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
                        dividend_date = dividend_value = dividend_type = dividend_payment_date = dividend_yield = None
                        for element_ in elements_.xpath(".//td"):
                            if element_.get('class'):
                                if element_.get('class').__contains__('first'):
                                    dividend_date = datetime.strptime(element_.text_content().strip().replace('.', '-'), '%d-%m-%Y')
                                    dividend_value = float(
                                        element_.getnext().text_content().replace('.', '').replace(',', '.'))
                                if element_.get('data-value') in type_values.keys():
                                    dividend_type = type_values[element_.get('data-value')]
                                    dividend_payment_date = datetime.strptime(element_.getnext().text_content().strip().replace('.', '-'), '%d-%m-%Y')
                                    next_element_ = element_.getnext()
                                    dividend_yield = next_element_.getnext().text_content()
                        obj = {
                            'Date': dividend_date,
                            'Dividend': dividend_value,
                            'Type': dividend_type,
                            'Payment Date': dividend_payment_date,
                            'Yield': dividend_yield,
                        }

                        objs.append(obj)

        df = pd.DataFrame(objs)
        return df
    else:
        raise RuntimeError("ERR#0061: introduced stock has no dividend's data to display.")


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

    resource_package = 'investpy'
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
