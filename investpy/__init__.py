#!/usr/bin/env python

import datetime
from random import randint

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy_test import user_agent as ua, equities as ts, funds as fs
from investpy_test.Data import Data  # TypeError: 'module' object is not callable


def get_recent_data(equity, as_json=False, order='ascending'):
    """
    This function retrieves recent historical data from the specified equity.
    The retrieved data corresponds to the last month and a half more or less.

    Parameters
    ----------
    :param equity: str
        name of the equity to retrieve recent historical data from
    :param order: str
        optional parameter to indicate the order of the recent data to retrieve
        default value is ascending
    :param as_json: bool
        optional parameter to specify the output, default is pandas.DataFrame
        if true, return value is a JSON object containing the recent data from the specified equity

    Returns
    -------
    :returns pandas.DataFrame (or JSON object if specified)
        returns a pandas DataFrame (or JSON object if specified) containing the recent data of the equity
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#003: order argument can just be ascending or descending, str type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = ts.get_equity_names()
        equities = pd.DataFrame(names)

    if equities is None:
        raise IOError("ERR#001: equities list not found or unable to retrieve."
                      "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    for row in equities.itertuples():
        if row.name.lower() == equity.lower():
            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"
            headers = {
                'User-Agent': ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            req = requests.get(url, headers=headers, timeout=5)

            if req.status_code != 200:
                return None

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#007: equity information unavailable or not found." 
                                         "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es" 
                                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_max = float(info[3].replace(',', '.'))
                    stock_min = float(info[4].replace(',', '.'))
                    stock_volume = 0

                    if info[5].__contains__('K'):
                        stock_volume = int(float(info[5].replace('K', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        stock_volume = int(float(info[5].replace('M', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        stock_volume = int(float(info[5].replace('B', '').replace(',', '.')) * 1000000000)

                    result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, stock_volume,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
                             'recent data':
                                 [value.equity_as_json() for value in result]
                             }
                    return json_
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.equity_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    return df
            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping." 
                                    "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es" 
                                    "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue


def get_historical_data(equity, start, end, as_json=False, order='ascending'):
    """
    This function retrieves historical data from the specified equity in the specified date range.

    Parameters
    ----------
    :param equity: str
        name of the equity to retrieve historical data from
    :param start: str
        start date since the data is going to be retrieved
    :param end: str
        end date until the data is going to be retrieved
    :param order: str
        optional parameter to indicate the order of the historical data to retrieve
        default value is ascending
    :param as_json: bool
        optional parameter to specify the output, default is pandas.DataFrame
        if true, return value is a JSON object containing the historical data from the specified equity

    Returns
    -------
    :returns pandas.DataFrame (or JSON object if specified)
        returns a pandas DataFrame (or JSON object if specified) containing the historical data of the equity
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#003: order argument can just be ascending or descending, str type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = ts.get_equity_names()
        equities = pd.DataFrame(names)

    if equities is None:
        raise IOError("ERR#001: equities list not found or unable to retrieve."
                      "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    for row in equities.itertuples():
        if row.name.lower() == equity.lower():
            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"
            headers = {
                'User-Agent': ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            req = requests.get(url, headers=headers, timeout=5)

            if req.status_code != 200:
                return None

            root_ = fromstring(req.text)
            header = root_.xpath('//h2//text()')[0]

            params = {
                "curr_id": row.id,
                "smlID": str(randint(1000000, 99999999)),
                "header": header,
                "st_date": start,
                "end_date": end,
                "interval_sec": "Daily",
                "sort_col": "date",
                "sort_ord": "DESC",
                "action": "historical_data"
            }

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            url = "https://es.investing.com/instruments/HistoricalDataAjax"

            req = requests.post(url, data=params, headers=head)

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#007: equity information unavailable or not found." 
                                         "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es" 
                                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_max = float(info[3].replace(',', '.'))
                    stock_min = float(info[4].replace(',', '.'))
                    stock_volume = 0

                    if info[5].__contains__('K'):
                        stock_volume = int(float(info[5].replace('K', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        stock_volume = int(float(info[5].replace('M', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        stock_volume = int(float(info[5].replace('B', '').replace(',', '.')) * 1000000000)

                    result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, stock_volume,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
                             'recent data':
                                 [value.equity_as_json() for value in result]
                             }
                    return json_
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.equity_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    return df
            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping."
                                   "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                   "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue


def get_fund_recent_data(fund, as_json=False, order='ascending'):
    """
    This function retrieves recent historical data from the specified fund.
    The retrieved data corresponds to the last month and a half more or less.

    Parameters
    ----------
    :param fund: str
        name of the fund to retrieve recent historical data from
    :param order: str
        optional parameter to indicate the order of the recent data to retrieve
        default value is ascending
    :param as_json: bool
        optional parameter to specify the output, default is pandas.DataFrame
        if true, return value is a JSON object containing the recent data from the specified fund

    Returns
    -------
    :returns pandas.DataFrame (or JSON object if specified)
        returns a pandas DataFrame (or JSON object if specified) containing the recent data of the fund
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#003: order argument can just be ascending or descending, str type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = fs.get_fund_names()
        funds = pd.DataFrame(names)

    if funds is None:
        raise IOError("ERR#005: fund list not found or unable to retrieve."
                      "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    for row in funds.itertuples():
        if row.name.lower() == fund.lower():
            url = "https://es.investing.com/funds/" + row.tag + "-historical-data"
            headers = {
                'User-Agent': ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            req = requests.get(url, headers=headers)

            if req.status_code != 200:
                return None

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#008: fund information unavailable or not found." 
                                         "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es" 
                                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_max = float(info[3].replace(',', '.'))
                    stock_min = float(info[4].replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, None,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
                             'recent data':
                                 [value.fund_as_json() for value in result]
                             }
                    return json_
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    return df

            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping."
                                   "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                   "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue


def get_fund_historical_data(fund, start, end, as_json=False, order='ascending'):
    """
    This function retrieves historical data from the specified fund in the specified date range.

    Parameters
    ----------
    :param fund: str
        name of the fund to retrieve historical data from
    :param start: str
        start date since the data is going to be retrieved
    :param end: str
        end date until the data is going to be retrieved
    :param order: str
        optional parameter to indicate the order of the historical data to retrieve
        default value is ascending
    :param as_json: bool
        optional parameter to specify the output, default is pandas.DataFrame
        if true, return value is a JSON object containing the historical data from the specified fund

    Returns
    -------
    :returns pandas.DataFrame (or JSON object if specified)
        returns a pandas DataFrame (or JSON object if specified) containing the historical data of the fund
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#003: order argument can just be ascending or descending, str type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = fs.get_fund_names()
        funds = pd.DataFrame(names)

    if funds is None:
        raise IOError("ERR#005: fund list not found or unable to retrieve."
                      "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    for row in funds.itertuples():
        if row.name.lower() == fund.lower():
            header = "Datos históricos " + row.symbol

            params = {
                "curr_id": row.id,
                "smlID": str(randint(1000000, 99999999)),
                "header": header,
                "st_date": start,
                "end_date": end,
                "interval_sec": "Daily",
                "sort_col": "date",
                "sort_ord": "DESC",
                "action": "historical_data"
            }

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            url = "https://es.investing.com/instruments/HistoricalDataAjax"

            req = requests.post(url, data=params, headers=head)

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#008: fund information unavailable or not found." 
                                         "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es" 
                                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_max = float(info[3].replace(',', '.'))
                    stock_min = float(info[4].replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, None,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
                             'recent data':
                                 [value.fund_as_json() for value in result]
                             }
                    return json_
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    return df
            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping."
                                   "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                   "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue
