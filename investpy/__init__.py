#!/usr/bin/env python

import datetime
from random import randint

import pandas as pd
import pkg_resources
import requests
import json
from lxml.html import fromstring

from investpy import user_agent as ua, equities as ts, funds as fs, etfs as es
from investpy.Data import Data  # TypeError: 'module' object is not callable


def get_equities_list():
    return ts.list_equities()


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
                    json_ = {'Name': row.name,
                             'Recent Data':
                                 [value.equity_as_json() for value in result]
                             }
                    return json.dumps(json_)
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

    try:
        datetime.datetime.strptime(start, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#011: incorrect data format, it should be 'dd/mm/yyyy'."
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    try:
        datetime.datetime.strptime(end, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#011: incorrect data format, it should be 'dd/mm/yyyy'."
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
                    return json.dumps(json_)
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


def get_equity_company_profile(equity, source='Investing'):

    available_sources = ['Investing', 'Bolsa de Madrid']

    if not equity:
        raise ValueError("ERR#012: equity parameter is mandatory and must be a valid equity name."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    if source not in available_sources:
        raise ValueError("ERR#013: the specified source is not valid, it can just be either" + ' or '.join(available_sources) +
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
            if source == 'Bolsa de Madrid':
                url = "http://www.bolsamadrid.es/esp/aspx/Empresas/FichaValor.aspx?ISIN=" + row.isin

                headers = {
                    "User-Agent": ua.get_random(),
                    "X-Requested-With": "XMLHttpRequest"
                }

                req = requests.get(url, headers=headers, timeout=5)

                root_ = fromstring(req.text)

                path_ = root_.xpath(".//td[contains(@class, 'Perfil')]")

                if path_:
                    return path_[0].text_content()
                else:
                    return None
            elif source == 'Investing':
                url = "https://www.investing.com/equities/" + row.tag + "-company-profile"

                headers = {
                    "User-Agent": ua.get_random(),
                    "X-Requested-With": "XMLHttpRequest"
                }

                req = requests.get(url, headers=headers, timeout=5)

                root_ = fromstring(req.text)

                path_ = root_.xpath(".//*[@id=\"profile-fullStory-showhide\"]")

                if path_:
                    return path_[0].text_content()
                else:
                    return None


def get_funds_list():
    return fs.list_funds()


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
                    return json.dumps(json_)
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

    try:
        datetime.datetime.strptime(start, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#011: incorrect data format, it should be 'dd/mm/yyyy'."
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    try:
        datetime.datetime.strptime(end, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#011: incorrect data format, it should be 'dd/mm/yyyy'."
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
                    return json.dumps(json_)
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


def get_fund_information(fund, as_json=False):
    """
        This function retrieves historical data from the specified fund in the specified date range.

        Parameters
        ----------
        :param fund: str
            name of the fund to retrieve information from
        :param as_json: bool
            optional parameter to specify the output, default is pandas.DataFrame
            if true, return value is a JSON object containing the information of the specified fund

        Returns
        -------
        :returns pandas.DataFrame (or JSON object if specified)
            returns a pandas DataFrame (or JSON object if specified) containing the information of the fund
        """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type."
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
            url = "https://es.investing.com/funds/" + row.tag
            headers = {
                'User-Agent': ua.get_random(),
                "X-Requested-With": "XMLHttpRequest"
            }

            req = requests.get(url, headers=headers, timeout=5)

            if req.status_code != 200:
                return None

            root_ = fromstring(req.text)
            path_ = root_.xpath("//div[contains(@class, 'overviewDataTable')]/div")
            result = pd.DataFrame(columns=['Fund Name', 'Rating', '1-Year Change', 'Previous Close', 'Risk Rating',
                                           'TTM Yield', 'ROE', 'Issuer', 'Turnover', 'ROA', 'Inception Date',
                                           'Total Assets', 'Expenses', 'Min Investment', 'Market Cap', 'Category'])
            result.at[0, 'Fund Name'] = row.name  # set_value deprecation warning

            if path_:
                for elements_ in path_:
                    title_ = elements_.xpath(".//span[@class='float_lang_base_1']")[0].text_content()
                    if title_ == 'Rating':
                        rating_score = 5 - len(elements_.xpath(".//span[contains(@class, 'morningStarsWrap')]/i[@class='morningStarLight']"))
                        result.at[0, 'Rating'] = rating_score
                    elif title_ == 'Var. en un año':
                        oneyear_variation = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content().replace(" ", "")
                        result.at[0, '1-Year Change'] = oneyear_variation
                    elif title_ == 'Último cierre':
                        previous_close = float(elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content().replace(',', '.'))
                        result.at[0, 'Previous Close'] = previous_close
                    elif title_ == 'Calificación de riesgo':
                        risk_score = 5 - len(elements_.xpath(".//span[contains(@class, 'morningStarsWrap')]/i[@class='morningStarLight']"))
                        result.at[0, 'Risk Rating'] = risk_score
                    elif title_ == 'Rendimiento año móvil':
                        ttm_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'TTM Yield'] = ttm_percentage
                    elif title_ == 'ROE':
                        roe_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'ROE'] = roe_percentage
                    elif title_ == 'Emisor':
                        issuer_name = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'Issuer'] = issuer_name
                    elif title_ == 'Volumen de ventas':
                        turnover_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'Turnover'] = turnover_percentage
                    elif title_ == 'ROA':
                        roa_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'ROA'] = roa_percentage
                    elif title_ == 'Fecha de inicio':
                        value = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        inception_date = datetime.datetime.strptime(value.replace('.', '-'), '%d/%m/%Y')
                        result.at[0, 'Inception Date'] = inception_date
                    elif title_ == 'Total activos':
                        value = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        total_assets = None
                        if value.__contains__('K'):
                            total_assets = int(float(value.replace('K', '').replace(',', '.')) * 1000)
                        elif value.__contains__('M'):
                            total_assets = int(float(value.replace('M', '').replace(',', '.')) * 1000000)
                        elif value.__contains__('B'):
                            total_assets = int(float(value.replace('B', '').replace(',', '.')) * 1000000000)
                        result.at[0, 'Total Assets'] = total_assets
                    elif title_ == 'Gastos':
                        expenses_percentage = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'Expenses'] = expenses_percentage
                    elif title_ == 'Inversión mínima':
                        min_investment = int(elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content())
                        result.at[0, 'Min Investment'] = min_investment
                    elif title_ == 'Cap. mercado':
                        value = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        market_cap = None
                        if value.__contains__('K'):
                            market_cap = int(float(value.replace('K', '').replace(',', '.')) * 1000)
                        elif value.__contains__('M'):
                            market_cap = int(float(value.replace('M', '').replace(',', '.')) * 1000000)
                        elif value.__contains__('B'):
                            market_cap = int(float(value.replace('B', '').replace(',', '.')) * 1000000000)
                        result.at[0, 'Market Cap'] = market_cap
                    elif title_ == 'Categoría':
                        category_name = elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content()
                        result.at[0, 'Category'] = category_name

                if as_json is True:
                    json_ = fs.fund_information_to_json(result)
                    return json_
                elif as_json is False:
                    return result
            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping."
                                   "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                   "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue


def get_etfs_list():
    return es.list_etfs()


def get_etf_recent_data(etf, as_json=False, order='ascending'):
    """
        This function retrieves recent historical data from the specified etf.
        The retrieved data corresponds to the last month and a half more or less.

        Parameters
        ----------
        :param etf: str
            name of the etf to retrieve recent historical data from
        :param order: str
            optional parameter to indicate the order of the recent data to retrieve
            default value is ascending
        :param as_json: bool
            optional parameter to specify the output, default is pandas.DataFrame
            if true, return value is a JSON object containing the recent data from the specified etf

        Returns
        -------
        :returns pandas.DataFrame (or JSON object if specified)
            returns a pandas DataFrame (or JSON object if specified) containing the recent data of the etf
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
    resource_path = '/'.join(('resources', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = es.get_etf_names()
        etfs = pd.DataFrame(names)

    if etfs is None:
        raise IOError("ERR#009: etf list not found or unable to retrieve."
                      "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    for row in etfs.itertuples():
        if row.name.lower() == etf.lower():
            url = "https://es.investing.com/etfs/" + row.tag + "-historical-data"
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
                        raise IndexError("ERR#010: etf information unavailable or not found."
                                         "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_max = float(info[3].replace(',', '.'))
                    stock_min = float(info[4].replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_close, stock_open, stock_max, stock_min, None, ))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
                             'recent data':
                                 [value.etf_as_json() for value in result]
                             }
                    return json.dumps(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    return df

            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping."
                                   "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                   "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue


def get_etf_historical_data(etf, start, end, as_json=False, order='ascending'):
    """
    This function retrieves historical data from the specified etf in the specified date range.

    Parameters
    ----------
    :param etf: str
        name of the etf to retrieve historical data from
    :param start: str
        start date since the data is going to be retrieved
    :param end: str
        end date until the data is going to be retrieved
    :param order: str
        optional parameter to indicate the order of the historical data to retrieve
        default value is ascending
    :param as_json: bool
        optional parameter to specify the output, default is pandas.DataFrame
        if true, return value is a JSON object containing the historical data from the specified etf

    Returns
    -------
    :returns pandas.DataFrame (or JSON object if specified)
        returns a pandas DataFrame (or JSON object if specified) containing the historical data of the etf
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#003: order argument can just be ascending or descending, str type."
                         "\n\t\t\tPlease check you are passing the parameters correctly or contact package admin: alvarob96@usal.es"
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    try:
        datetime.datetime.strptime(start, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#011: incorrect data format, it should be 'dd/mm/yyyy'."
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    try:
        datetime.datetime.strptime(end, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#011: incorrect data format, it should be 'dd/mm/yyyy'."
                         "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = es.get_etf_names()
        etfs = pd.DataFrame(names)

    if etfs is None:
        raise IOError("ERR#009: etf list not found or unable to retrieve."
                      "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                      "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")

    for row in etfs.itertuples():
        if row.name.lower() == etf.lower():
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
                        raise IndexError("ERR#010: etf information unavailable or not found."
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
                                 [value.etf_as_json() for value in result]
                             }
                    return json.dumps(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
                    df.set_index('Date', inplace=True)
                    return df
            else:
                raise RuntimeError("ERR#004: data retrieval error while scraping."
                                   "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
                                   "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
        else:
            continue


# def get_available_sectors():
#     sectors = []
#
#     resource_package = __name__
#     resource_path = '/'.join(('resources', 'equities.csv'))
#     if pkg_resources.resource_exists(resource_package, resource_path):
#         equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
#     else:
#         names = ts.get_equity_names()
#         equities = pd.DataFrame(names)
#
#     if equities is None:
#         raise IOError("ERR#001: equities list not found or unable to retrieve."
#                       "\n\t\t\tPlease check your Internet connection or contact package admin: alvarob96@usal.es"
#                       "\n\t\t\tIf needed, open an issue on: https://github.com/alvarob96/investpy/issues")
#
#     for row in equities.itertuples():
#         url = "https://www.investing.com/equities/" + row.tag + "-company-profile"
#
#         headers = {
#             "User-Agent": ua.get_random(),
#             "X-Requested-With": "XMLHttpRequest"
#         }
#
#         req = requests.get(url, headers=headers, timeout=5)
#
#         root_ = fromstring(req.text)
#
#         path_ = root_.xpath("/html/body/div[5]/section/div[8]/div[2]/a")
#
#         if path_:
#             sector = path_[0].text_content()
#             if sector not in sectors:
#                 sectors.append(path_[0].text_content())
#
#     return sectors