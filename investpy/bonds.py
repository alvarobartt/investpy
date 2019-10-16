#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
from random import randint
import logging

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy.utils import user_agent
from investpy.utils.Data import Data

from investpy.data.bonds_data import bonds_as_df, bonds_as_list, bonds_as_dict
from investpy.data.bonds_data import bond_countries_as_list


def get_bonds(country=None):
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

    return bonds_as_df(country)


def get_bonds_list(country=None):
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

    return bonds_as_list(country)


def get_bonds_dict(country=None, columns=None, as_json=False):
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
                    'id': id,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        IOError: raised when `bonds.csv` file is missing or empty.

    """

    return bonds_as_dict(country=country, columns=columns, as_json=as_json)


def get_bond_countries():
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

    return bond_countries_as_list()


def get_bond_recent_data(bond, country, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced stock from Investing.com. So on, the recent data
    of the introduced stock from the specified country will be retrieved and returned as a :obj:`pandas.DataFrame` if
    the parameters are valid and the request to Investing.com succeeds. Note that additionally some optional parameters
    can be specified: as_json, order and debug, which let the user decide if the data is going to be returned as a
    :obj:`json` or not, if the historical data is going to be ordered ascending or descending (where the index is the date)
    and whether debug messages are going to be printed or not, respectively.

    Args:
        stock (:obj:`str`): symbol of the stock to retrieve recent historical data from.
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
        >>> investpy.get_bond_recent_data(bond='bbva', country='spain')
                         Open   High    Low  Close
            Date
            2019-08-13  4.263  4.395  4.230  4.353
            2019-08-14  4.322  4.325  4.215  4.244
            2019-08-15  4.281  4.298  4.187  4.234
            2019-08-16  4.234  4.375  4.208  4.365
            2019-08-19  4.396  4.425  4.269  4.269

    """

    if not bond:
        raise ValueError("ERR#0066: bond parameter is mandatory and must be a valid bond name.")

    if not isinstance(bond, str):
        raise ValueError("ERR#0067: bond argument needs to be a str.")

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

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'bonds', 'bonds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0065: bonds object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_bond_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    bonds = bonds[bonds['country'] == unidecode.unidecode(country.lower())]

    bond = bond.strip()
    bond = bond.lower()

    if unidecode.unidecode(bond) not in [unidecode.unidecode(value.lower()) for value in bonds['name'].tolist()]:
        raise RuntimeError("ERR#0068: bond " + bond + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('investpy')

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced bond on Investing.com')

    id_ = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'id']
    name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'name']
    full_name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'full_name']

    logger.info(str(bond) + ' found on Investing.com')

    header = full_name + " Bond Yield Historical Data"

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

    url = "https://www.investing.com/instruments/HistoricalDataAjax"

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
                info.append(nested_.get('data-real-value'))

            bond_date = datetime.fromtimestamp(int(info[0]))
            bond_date = date(bond_date.year, bond_date.month, bond_date.day)
            bond_close = float(info[1])
            bond_open = float(info[2])
            bond_high = float(info[3])
            bond_low = float(info[4])

            result.insert(len(result),
                          Data(bond_date, bond_open, bond_high, bond_low,
                               bond_close, None, None))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {'name': name,
                     'recent':
                         [value.bond_as_json() for value in result]
                     }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.bond_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_bond_historical_data(bond, country, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced stock from Investing.com. So on, the historical data
    of the introduced stock from the specified country in the specified data range will be retrieved and returned as
    a :obj:`pandas.DataFrame` if the parameters are valid and the request to Investing.com succeeds. Note that additionally
    some optional parameters can be specified: as_json, order and debug, which let the user decide if the data is going to
    be returned as a :obj:`json` or not, if the historical data is going to be ordered ascending or descending (where the
    index is the date) and whether debug messages are going to be printed or not, respectively.

    Args:
        bond (:obj:`str`): symbol of the stock to retrieve historical data from.
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
        >>> investpy.get_bond_historical_data(bond='bbva', country='spain', from_date='01/01/2010', to_date='01/01/2019')
                         Open   High    Low  Close  Volume Currency
            Date
            2010-01-04  12.73  12.96  12.73  12.96       0      EUR
            2010-01-05  13.00  13.11  12.97  13.09       0      EUR
            2010-01-06  13.03  13.17  13.02  13.12       0      EUR
            2010-01-07  13.02  13.11  12.93  13.05       0      EUR
            2010-01-08  13.12  13.22  13.04  13.18       0      EUR

    """

    if not bond:
        raise ValueError("ERR#0066: bond parameter is mandatory and must be a valid bond name.")

    if not isinstance(bond, str):
        raise ValueError("ERR#0067: bond argument needs to be a str.")

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

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'bonds', 'bonds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0065: bonds object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_bond_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    bonds = bonds[bonds['country'] == unidecode.unidecode(country.lower())]

    bond = bond.strip()
    bond = bond.lower()

    if unidecode.unidecode(bond) not in [unidecode.unidecode(value.lower()) for value in bonds['name'].tolist()]:
        raise RuntimeError("ERR#0068: bond " + bond + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('investpy')

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced bond on Investing.com')

    id_ = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'id']
    name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'name']
    full_name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'full_name']

    logger.info(str(bond) + ' found on Investing.com')

    final = list()

    logger.info('Data parsing process starting...')

    header = full_name + " Bond Yield Historical Data"

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
                        raise IndexError("ERR#0069: bond information unavailable or not found.")
                else:
                    data_flag = True
                
                if data_flag is True:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.get('data-real-value'))

                    bond_date = datetime.fromtimestamp(int(info[0]))
                    bond_date = date(bond_date.year, bond_date.month, bond_date.day)
                    bond_close = float(info[1])
                    bond_open = float(info[2])
                    bond_high = float(info[3])
                    bond_low = float(info[4])

                    result.insert(len(result),
                                Data(bond_date, bond_open, bond_high, bond_low,
                                    bond_close, None, None))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.bond_as_json() for value in result]
                             }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.bond_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)
        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def search_bonds(by, value):
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

    available_search_fields = ['name', 'full_name']

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
    resource_path = '/'.join(('resources', 'bonds', 'bonds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0065: bonds object not found or unable to retrieve.")

    bonds['matches'] = bonds[by].str.contains(value, case=False)

    search_result = bonds.loc[bonds['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
