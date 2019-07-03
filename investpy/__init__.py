#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import datetime
import json
from random import randint

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent as ua, equities as ts, funds as fs, etfs as es
from investpy.Data import Data


"""------------- EQUITIES -------------"""


def get_equities():
    """
    This function retrieves all the available equities indexed on a CSV file,
    previously filled via Web Scraping of Investing, as a pandas.DataFrame.

    Returns:
        equities (:obj:`pandas.DataFrame`): description
            it contains the retrieved data from equities.csv file with its respective column values
            <full_name, id, isin, name, tag>

            So the resulting `pandas.DataFrame` should look like:

                full_name | id | isin | name | tag
                ----------------------------------
                xxxxxxxxx | xx | xxxx | xxxx | xxx

    Raises:
        IOError: if data could not be retrieved due to file error.

    """

    return ts.equities_as_df()


def get_equities_list():
    """
    This function retrieves all the available equities indexed on a CSV file,
    previously filled via Web Scraping of Investing, as a list. The resulting list
    contains all the names of all the available equities, which can be further used
    for recent or historical data retrieval.

    Returns:
        equities (:obj:`list` of :obj:`str`): description
            it contains the retrieved data from equities.csv as a list with all the equity names available.

            So the resulting `list` should look like:

                equities = ['acs', 'abengoa', ...]

    Raises:
        IOError: if data could not be retrieved due to file error.

    """

    return ts.equities_as_list()


def get_recent_data(equity, as_json=False, order='ascending'):
    """

    This function retrieves recent historical data from the introduced equity from Investing
    via Web Scraping. The resulting data can it either be stored in a pandas.DataFrame or in a
    json file with ascending or descending order.

    Args:
        equity (str): name of the equity to retrieve recent historical data from.

        as_json (:obj:`boolean`, optional): optional argument to determine the format of the output data (pandas.DataFrame or JSON).

        order (:obj:`str`, optional): optional argument to define the order of the retrieved data (ascending or descending).

    Returns:
        data (pandas.DataFrame or JSON): description
            The function returns a either a pandas.DataFrame or a JSON file containing the retrieved recent data
            from the specified equity via argument. The dataset contains the open, high, low, close and volume values
            for the selected equity on market days.

            The Return data is case we use default arguments will look like::

            date || open | high | low | close | volume
            -----||-----------------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

            , but if we define as_json=True, then the output will be::

                {
                    name: name,
                    full_name: full_name,
                    recent: [
                        dd/mm/yyyy: {
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: equities object/file not found or unable to retrieve.
        RuntimeError: introduced equity does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if equity information was unavailable or not found.

    Examples:
        >>> investpy.get_recent_data(equity='bbva', as_json=False, order='ascending')
        date || open | high | low | close | volume
        -----||-----------------------------------
        xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

    """

    if not isinstance(equity, str):
        raise ValueError("ERR#0027: equity argument needs to be a str.")

    if not equity:
        raise ValueError("ERR#0013: equity parameter is mandatory and must be a valid equity name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#0003: order argument can just be ascending or descending, str type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = get_equities()

    if equities is None:
        raise IOError("ERR#0001: equities object not found or unable to retrieve.")

    if unidecode.unidecode(equity.lower()) not in [unidecode.unidecode(value.lower()) for value in equities['name'].tolist()]:
        raise RuntimeError("ERR#0018: equity " + equity.lower() + " not found, check if it is correct.")

    for row in equities.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(equity.lower()):
            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"

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
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#0007: equity information unavailable or not found.")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_high = float(info[3].replace(',', '.'))
                    stock_low = float(info[4].replace(',', '.'))
                    stock_volume = 0

                    if info[5].__contains__('K'):
                        stock_volume = int(float(info[5].replace('K', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        stock_volume = int(float(info[5].replace('M', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        stock_volume = int(float(info[5].replace('B', '').replace(',', '.')) * 1000000000)

                    result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, stock_volume,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
                             'full_name': row.full_name,
                             'recent':
                                 [value.equity_as_json() for value in result]
                             }

                    return json.dumps(json_, sort_keys=False)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.equity_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    return df
            else:
                raise RuntimeError("ERR#0004: data retrieval error while scraping.")
        else:
            continue


def get_historical_data(equity, start, end, as_json=False, order='ascending'):
    """

        This function retrieves historical data from the introduced equity from Investing
        via Web Scraping on the introduced date range. The resulting data can it either be `
        stored in a `pandas.DataFrame` or in a `json` object with ascending or descending order.

        Args:
            equity (str): name of the equity to retrieve recent historical data from.

            start (str): start date as `str` formatted as dd/mm/yyyy

            end (str): end date as `str` formatted as dd/mm/yyyy

            as_json (:obj:`boolean`, optional): to determine the format of the output data (pandas.DataFrame or JSON).

            order (:obj:`str`, optional): to define the order of the retrieved data (ascending or descending).

        Returns:
            data (:obj:`pandas.DataFrame` or :obj:`json`): description
                The function returns a either a pandas.DataFrame or a JSON file containing the retrieved recent data
                from the specified equity via argument. The dataset contains the open, high, low, close and volume values
                for the selected equity on market days.

                The Return data is case we use default arguments will look like::

                date || open | high | low | close | volume
                -----||-----------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

                , but if we define as_json=True, then the output will be::

                    {
                        name: name,
                        full_name: full_name,
                        historical: [
                            dd/mm/yyyy: {
                                open: x,
                                high: x,
                                low: x,
                                close: x,
                                volume: x
                            },
                            ...
                        ]
                    }

        Raises:
            ValueError: argument error.
            IOError: equities object/file not found or unable to retrieve.
            RuntimeError: introduced equity does not match any of the indexed ones.
            ConnectionError: if GET requests does not return 200 status code.
            IndexError: if equity information was unavailable or not found.

        Examples:
            >>> investpy.get_historical_data(equity='bbva', start='01/01/2010', end='01/01/2019', as_json=False, order='ascending')
            date || open | high | low | close | volume
            -----||-----------------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

    """

    if not isinstance(equity, str):
        raise ValueError("ERR#0027: equity argument needs to be a str.")

    if not equity:
        raise ValueError("ERR#0013: equity parameter is mandatory and must be a valid equity name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#0003: order argument can just be ascending or descending, str type.")

    try:
        datetime.datetime.strptime(start, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect start date format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(end, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0012: incorrect end date format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: end_date should be greater than start_date, both formatted as 'dd/mm/yyyy'.")

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
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = ts.retrieve_equities()

    if equities is None:
        raise IOError("ERR#0001: equities object not found or unable to retrieve.")

    if unidecode.unidecode(equity.lower()) not in [unidecode.unidecode(value.lower()) for value in equities['name'].tolist()]:
        raise RuntimeError("ERR#0018: equity " + equity.lower() + " not found, check if it is correct.")

    for row in equities.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(equity.lower()):
            final = list()

            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"

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
            header = root_.xpath('//h2//text()')[0]

            for index in range(len(date_interval['intervals'])):

                interval_counter += 1

                params = {
                    "curr_id": row.id,
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
                    "User-Agent": ua.get_random(),
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
                                raise IndexError("ERR#0007: equity information unavailable or not found.")
                        else:
                            data_flag = True

                        if data_flag is True:
                            stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                            stock_close = float(info[1].replace(',', '.'))
                            stock_open = float(info[2].replace(',', '.'))
                            stock_high = float(info[3].replace(',', '.'))
                            stock_low = float(info[4].replace(',', '.'))
                            stock_volume = 0

                            if info[5].__contains__('K'):
                                stock_volume = int(float(info[5].replace('K', '').replace(',', '.')) * 1000)
                            elif info[5].__contains__('M'):
                                stock_volume = int(float(info[5].replace('M', '').replace(',', '.')) * 1000000)
                            elif info[5].__contains__('B'):
                                stock_volume = int(float(info[5].replace('B', '').replace(',', '.')) * 1000000000)

                            result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, stock_volume,))

                    if data_flag is True:
                        if order == 'ascending':
                            result = result[::-1]
                        elif order == 'descending':
                            result = result

                        if as_json is True:
                            json_ = {'name': row.name,
                                     'full_name': row.full_name,
                                     'historical':
                                         [value.equity_as_json() for value in result]
                                     }
                            final.append(json_)
                        elif as_json is False:
                            df = pd.DataFrame.from_records([value.equity_to_dict() for value in result])
                            df.set_index('Date', inplace=True)

                            final.append(df)
                    else:
                        continue
                else:
                    raise RuntimeError("ERR#0004: data retrieval error while scraping.")

            if as_json is True:
                return json.dumps(final, sort_keys=False)
            elif as_json is False:
                return pd.concat(final)
        else:
            continue


def get_equity_company_profile(equity, language='english'):
    """
    This function retrieves the company profile from an equity in the specified language
    from different sources. Currently just the company profile of spanish equities in english
    and spanish is available for retrieval.

    Args:
        equity (str): name of the equity to retrieve ther company profile from.

        language (:obj:`str`, optional): language of the company profile to be retrieved (english or spanish).

    Returns:
        company_profile (:obj:`dict`): description
            it contains the retrieved company profile from either Investing.com (english) or Bolsa de Madrid (spanish)
            and its respective url link from where it was retrieved.

            So the resulting `dict` should look like::

                company_profile = {
                    url: 'https://www.investing.com/equities/bbva-company-profile',
                    desc: 'Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a diversified financial company [...]'
                }

    Raises:
        IOError: if data could not be retrieved due to file error.

    Examples:
        >>> investpy.get_equity_company_profile(equity='bbva', language='english')
        company_profile = {
            url: 'https://www.investing.com/equities/bbva-company-profile',
            desc: 'Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a diversified financial company [...]'
        }

    """

    available_sources = {
        'english': 'Investing',
        'en': 'Investing',
        'spanish': 'Bolsa de Madrid',
        'es': 'Bolsa de Madrid',
    }

    if not isinstance(equity, str):
        raise ValueError("ERR#0027: equity argument needs to be a str.")

    if not equity:
        raise ValueError("ERR#0013: equity parameter is mandatory and must be a valid equity name.")

    if language.lower() not in available_sources.keys():
        raise ValueError("ERR#0014: the specified language is not valid, it can just be either spanish (es) or english (en).")

    selected_source = available_sources[language.lower()]

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = ts.retrieve_equities()

    if equities is None:
        raise IOError("ERR#0001: equities object not found or unable to retrieve.")

    if unidecode.unidecode(equity.lower()) not in [unidecode.unidecode(value.lower()) for value in equities['name'].tolist()]:
        raise RuntimeError("ERR#0018: equity " + equity.lower() + " not found, check if it is correct.")

    company_profile = {
        'url': None,
        'desc': None
    }

    for row in equities.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(equity.lower()):
            if selected_source == 'Bolsa de Madrid':
                url = "http://www.bolsamadrid.es/esp/aspx/Empresas/FichaValor.aspx?ISIN=" + row.isin

                company_profile['url'] = url

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

                path_ = root_.xpath(".//td[contains(@class, 'Perfil')]")

                if path_:
                    company_profile['desc'] = str(path_[0].text_content())

                    return company_profile
                else:
                    return company_profile
            elif selected_source == 'Investing':
                url = "https://www.investing.com/equities/" + row.tag + "-company-profile"

                company_profile['url'] = url

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

                path_ = root_.xpath(".//*[@id=\"profile-fullStory-showhide\"]")

                if path_:
                    company_profile['desc'] = str(path_[0].text_content())

                    return company_profile
                else:
                    return company_profile


"""------------- FUNDS -------------"""


def get_funds():
    """
    This function retrieves all the available funds and returns a pandas.DataFrame of them all.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        :returns a pandas.DataFrame with all the available funds to retrieve data from
    """

    return fs.funds_as_df()


def get_funds_list():
    """
    This function retrieves the list of all the available funds

    Returns
    -------
    :returns list that contains all the available fund names
    """

    return fs.funds_as_list()


def get_funds_dict(columns, as_json):
    """
    This function retrieves a dictionary with the specified columns of all the available funds

    Returns
    -------
    :returns a dictionary that contains all the available fund values specified in the columns
    """

    return fs.funds_as_dict(columns=columns, as_json=as_json)


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
    :returns pandas DataFrame (or JSON object if specified) containing the recent data of the fund
    """

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#0003: order argument can just be ascending or descending, str type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = get_funds()

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    if unidecode.unidecode(fund.lower()) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund.lower() + " not found, check if it is correct.")

    for row in funds.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(fund.lower()):
            url = "https://es.investing.com/funds/" + row.tag + "-historical-data"

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
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#0008: fund information unavailable or not found.")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_high = float(info[3].replace(',', '.'))
                    stock_low = float(info[4].replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
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
    :returns pandas DataFrame (or JSON object if specified) containing the historical data of the fund
    """

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#0003: order argument can just be ascending or descending, str type.")

    try:
        datetime.datetime.strptime(start, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect start date format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(end, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0012: incorrect end date format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: end_date should be greater than start_date, both formatted as 'dd/mm/yyyy'.")

    if start_date.year < 2010:
        start_date = start_date.replace(year=2010)

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
        funds = get_funds()

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    if unidecode.unidecode(fund.lower()) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund.lower() + " not found, check if it is correct.")

    for row in funds.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(fund.lower()):
            final = list()

            for index in range(len(date_interval['intervals'])):
                header = "Datos históricos " + row.symbol

                params = {
                    "curr_id": row.id,
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
                    "User-Agent": ua.get_random(),
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
                                raise IndexError("ERR#0008: fund information unavailable or not found.")

                        else:
                            data_flag = True

                        if data_flag is True:
                            stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                            stock_close = float(info[1].replace(',', '.'))
                            stock_open = float(info[2].replace(',', '.'))
                            stock_high = float(info[3].replace(',', '.'))
                            stock_low = float(info[4].replace(',', '.'))

                            result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                    if data_flag is True:
                        if order == 'ascending':
                            result = result[::-1]
                        elif order == 'descending':
                            result = result

                        if as_json is True:
                            json_ = {'name': row.name,
                                     'historical':
                                         [value.fund_as_json() for value in result]
                                     }

                            final.append(json_)
                        elif as_json is False:
                            df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
                            df.set_index('Date', inplace=True)

                            final.append(df)
                    else:
                        continue
                else:
                    raise RuntimeError("ERR#0004: data retrieval error while scraping.")

            if as_json is True:
                return json.dumps(final, sort_keys=False)
            elif as_json is False:
                return pd.concat(final)
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
    :returns pandas DataFrame (or JSON object if specified) containing the information of the fund
    """

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'funds', 'funds.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        funds = get_funds()

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    if unidecode.unidecode(fund.lower()) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund.lower() + " not found, check if it is correct.")

    for row in funds.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(fund.lower()):
            url = "https://es.investing.com/funds/" + row.tag

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
            path_ = root_.xpath("//div[contains(@class, 'overviewDataTable')]/div")
            result = pd.DataFrame(columns=['Fund Name', 'Rating', '1-Year Change', 'Previous Close', 'Risk Rating',
                                           'TTM Yield', 'ROE', 'Issuer', 'Turnover', 'ROA', 'Inception Date',
                                           'Total Assets', 'Expenses', 'Min Investment', 'Market Cap', 'Category'])
            result.at[0, 'Fund Name'] = row.name

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
                        inception_date = datetime.datetime.strptime(value.replace('.', '/'), '%d/%m/%Y')
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
                    json_ = fs.fund_information_as_json(result)
                    return json_
                elif as_json is False:
                    return result
            else:
                raise RuntimeError("ERR#0004: data retrieval error while scraping.")
        else:
            continue


"""------------- ETFS -------------"""


def get_etfs():

    return es.retrieve_etfs()


def get_etf_countries():

    return es.retrieve_etf_countries()


def get_etf_df(country=None):
    """
    This function retrieves all the available etfs and returns a pandas.DataFrame of them all.
    All the available etfs can be found at: https://es.investing.com/etfs/spain-etfs

    Returns
    -------
        :returns a pandas.DataFrame with all the available etfs to retrieve data from
    """

    return es.etfs_as_df(country)


def get_etf_list(country=None):
    """
    This function retrieves the list of all the available etfs

    Returns
    -------
    :returns list
        returns a list that contains all the available etf names
    """

    return es.etfs_as_list(country)


def get_etf_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves a dictionary with the specified columns of all the available etfs

    Returns
    -------
    :returns a dictionary that contains all the available etf values specified in the columns
    """

    return es.etfs_as_dict(country, columns=columns, as_json=as_json)


def get_etf_recent_data(etf, as_json=False, order='ascending'):
    """
    This function retrieves recent historical data from the specified etf.
    The retrieved data corresponds to the last month and a half more or less.

    Parameters
    ----------
    :param country:
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
    :returns pandas DataFrame (or JSON object if specified) containing the recent data of the etf
    """

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#0003: order argument can just be ascending or descending, str type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        etfs = es.retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(etf.lower()) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + etf.lower() + " not found, check if it is correct.")

    for row in etfs.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(etf.lower()):
            url = "https://es.investing.com/etfs/" + row.tag + "-historical-data"

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

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
            result = list()

            if path_:
                for elements_ in path_:
                    info = []
                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.text_content())

                    if info[0] == 'No se encontraron resultados':
                        raise IndexError("ERR#0010: etf information unavailable or not found.")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace(',', '.'))
                    stock_open = float(info[2].replace(',', '.'))
                    stock_high = float(info[3].replace(',', '.'))
                    stock_low = float(info[4].replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                if order == 'ascending':
                    result = result[::-1]
                elif order == 'descending':
                    result = result

                if as_json is True:
                    json_ = {'name': row.name,
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
    :returns pandas DataFrame (or JSON object if specified) containing the historical data of the etf
    """

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'descending']:
        raise ValueError("ERR#0003: order argument can just be ascending or descending, str type.")

    try:
        datetime.datetime.strptime(start, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(end, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(start, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: end_date should be greater than start_date, both formatted as 'dd/mm/yyyy'.")

    if start_date.year < 2010:
        start_date = start_date.replace(year=2010)

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
        etfs = es.retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(etf.lower()) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + etf.lower() + " not found, check if it is correct.")

    for row in etfs.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(etf.lower()):
            final = list()

            for index in range(len(date_interval['intervals'])):
                header = "Datos históricos " + row.symbol

                params = {
                    "curr_id": row.id,
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
                    "User-Agent": ua.get_random(),
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
                                raise IndexError("ERR#0010: etf information unavailable or not found.")
                        else:
                            data_flag = True

                        if data_flag is True:
                            stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                            stock_close = float(info[1].replace(',', '.'))
                            stock_open = float(info[2].replace(',', '.'))
                            stock_high = float(info[3].replace(',', '.'))
                            stock_low = float(info[4].replace(',', '.'))

                            result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                    if data_flag is True:
                        if order == 'ascending':
                            result = result[::-1]
                        elif order == 'descending':
                            result = result

                        if as_json is True:
                            json_ = {'name': row.name,
                                     'historical':
                                         [value.etf_as_json() for value in result]
                                     }

                            final.append(json_)
                        elif as_json is False:
                            df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
                            df.set_index('Date', inplace=True)

                            final.append(df)
                    else:
                        continue
                else:
                    raise RuntimeError("ERR#0004: data retrieval error while scraping.")

            if as_json is True:
                return json.dumps(final, sort_keys=False)
            elif as_json is False:
                return pd.concat(final)
        else:
            continue
