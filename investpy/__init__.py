#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = 'Alvaro Bartolome <alvarob96@usal.es>'
__version__ = '0.8.9'

import datetime
import json
from random import randint
import logging

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
    This function retrieves all the equities previously stored on `equities.csv` file, via
    `investpy.equities.retrieve_equities()`. The CSV file is read and if it does not exists,
    it is created again; but if it does exists, it is loaded into a :obj:`pandas.DataFrame`.

    Returns:
        :obj:`pandas.DataFrame` - equities:
            The resulting :obj:`pandas.DataFrame` contains the `equities.csv` file content if
            it was properly read or retrieved in case it did not exist in the moment when the
            function was first called.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                name | full name | tag | isin | id
                -----|-----------|-----|------|----
                xxxx | xxxxxxxxx | xxx | xxxx | xx

    Raises:
        IOError: raised if equities retrieval failed, both for missing file or empty file, after and before retrieval.
    """

    return ts.equities_as_df()


def get_equities_list():
    """
    This function retrieves all the equities previously stored on `equities.csv` file, via
    `investpy.equities.retrieve_equities()`. The CSV file is read and if it does not exists,
    it is created again; but if it does exists, equity names are loaded into a :obj:`list`.

    Returns:
        :obj:`list` - equities_list:
            The resulting :obj:`list` contains the `equities.csv` file content if
            it was properly read or retrieved in case it did not exist in the moment when the
            function was first called, as a :obj:`list` containing all the equity names.

            So on the listing will contain the equity names listed on Investing.com and will
            look like the following::

                equities_list = ['ACS', 'Abengoa', 'Atresmedia', ...]

    Raises:
        IOError: raised if equities retrieval failed, both for missing file or empty file, after and before retrieval.
    """

    return ts.equities_as_list()


def get_recent_data(equity, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `equity` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        equity (:obj:`str`): name of the equity to retrieve recent historical data from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified equity via argument. The dataset contains the open, high, low, close and
            volume values for the selected equity on market days.

            The return data is case we use default arguments will look like::

                date || open | high | low | close | volume
                -----||-----------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

            but if we define `as_json=True`, then the output will be::

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
        >>> investpy.get_recent_data(equity='bbva', as_json=False, order='ascending', debug=False)
            date || open | high | low | close | volume
            -----||-----------------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx
    """

    if not equity:
        raise ValueError("ERR#0013: equity parameter is mandatory and must be a valid equity name.")

    if not isinstance(equity, str):
        raise ValueError("ERR#0027: equity argument needs to be a str.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = get_equities()

    if equities is None:
        raise IOError("ERR#0001: equities object not found or unable to retrieve.")

    equity = equity.strip()

    if unidecode.unidecode(equity.lower()) not in [unidecode.unidecode(value.lower()) for value in equities['name'].tolist()]:
        raise RuntimeError("ERR#0018: equity " + equity.lower() + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced equity on Investing.com')

    for row in equities.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(equity.lower()):
            logger.info(str(equity) + ' found on Investing.com')

            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            logger.info('Request sent to Investing.com!')

            req = requests.get(url, headers=head, timeout=5)

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
                        raise IndexError("ERR#0007: equity information unavailable or not found.")

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace('.', '').replace(',', '.'))
                    stock_open = float(info[2].replace('.', '').replace(',', '.'))
                    stock_high = float(info[3].replace('.', '').replace(',', '.'))
                    stock_low = float(info[4].replace('.', '').replace(',', '.'))

                    if info[5].__contains__('K'):
                        stock_volume = int(float(info[5].replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif info[5].__contains__('M'):
                        stock_volume = int(float(info[5].replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    elif info[5].__contains__('B'):
                        stock_volume = int(float(info[5].replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)
                    else:
                        stock_volume = int(float(info[5].replace('.', '').replace(',', '.')))

                    result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, stock_volume,))

                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                logger.info('Data parsing process finished...')

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


def get_historical_data(equity, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced `equity` from Investing
    via Web Scraping on the introduced date range. The resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` object with `ascending` or `descending` order.

    Args:
        equity (:obj:`str`): name of the equity to retrieve historical data from.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional): to define the order of the retrieved data (`ascending` or `descending`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified equity via argument. The dataset contains the open, high, low, close and
            volume values for the selected equity on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | volume
                -----||-----------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

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
        >>> investpy.get_historical_data(equity='bbva', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)
            date || open | high | low | close | volume
            -----||-----------------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx

    """

    if not equity:
        raise ValueError("ERR#0013: equity parameter is mandatory and must be a valid equity name.")

    if not isinstance(equity, str):
        raise ValueError("ERR#0027: equity argument needs to be a str.")

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
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = ts.retrieve_equities()

    if equities is None:
        raise IOError("ERR#0001: equities object not found or unable to retrieve.")

    equity = equity.strip()

    if unidecode.unidecode(equity.lower()) not in [unidecode.unidecode(value.lower()) for value in equities['name'].tolist()]:
        raise RuntimeError("ERR#0018: equity " + equity.lower() + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced equity on Investing.com')

    for row in equities.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(equity.lower()):
            logger.info(str(equity) + ' found on Investing.com')

            url = "https://es.investing.com/equities/" + row.tag + "-historical-data"

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            logger.info('Request sent to Investing.com!')

            req = requests.get(url, headers=head, timeout=5)

            if req.status_code != 200:
                raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

            logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

            root_ = fromstring(req.text)
            header = root_.xpath('//h2//text()')[0]

            final = list()

            logger.info('Data parsing process starting...')

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
                            else:
                                stock_volume = int(float(info[5].replace('.', '').replace(',', '.')))

                            result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, stock_volume,))

                    if data_flag is True:
                        if order in ['ascending', 'asc']:
                            result = result[::-1]
                        elif order in ['descending', 'desc']:
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
                    raise RuntimeError("ERR#0004: data retrieval error while scraping.")

            logger.info('Data parsing process finished...')

            if as_json is True:
                return json.dumps(final[0], sort_keys=False)
            elif as_json is False:
                return pd.concat(final)


def get_equity_company_profile(equity, language='english'):
    """
    This function retrieves the company profile from an `equity` in the specified language
    from different sources. Currently just the company profile of spanish equities in english
    and spanish is available for retrieval.

    Args:
        equity (:obj:`str`): name of the equity to retrieve its company profile from.
        language (:obj:`str`, optional): language of the company profile to be retrieved (english or spanish).

    Returns:
        :obj:`dict` - company_profile:
            The resulting :obj:`dict` contains the retrieved company profile from the selected source by language,
            which can be either Investing.com (english) or Bolsa de Madrid (spanish); and its respective url
            from where it was retrieved, so to have both the source and the description fo the company_profile.

            So the resulting :obj:`dict` should look like::

                company_profile = {
                    url: 'https://www.investing.com/equities/bbva-company-profile',
                    desc: 'Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a ...'
                }

    Raises:
        IOError: if data could not be retrieved due to file error.

    Examples:
        >>> investpy.get_equity_company_profile(equity='bbva', language='english')
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

    if not equity:
        raise ValueError("ERR#0013: equity parameter is mandatory and must be a valid equity name.")

    if not isinstance(equity, str):
        raise ValueError("ERR#0027: equity argument needs to be a str.")

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

    equity = equity.strip()

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
    This function retrieves all the available `funds` from Investing.com and returns them as a :obj:`pandas.DataFrame`,
    which contains not just the fund names, but all the fields contained on the funds file.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

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

    return fs.funds_as_df()


def get_funds_list():
    """
    This function retrieves all the available funds and returns a list of each one of them.
    All the available funds can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

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

    return fs.funds_as_list()


def get_funds_dict(columns, as_json):
    """
    This function retrieves all the available funds on Investing.com and
    returns them as a :obj:`dict` containing the `asset_class`, `id`, `issuer`,
    `name`, `symbol` and `tag`. All the available funds can be found at:
    https://es.investing.com/etfs/spain-etfs

    Args:
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

    return fs.funds_as_dict(columns=columns, as_json=as_json)


def get_fund_recent_data(fund, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `fund` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        fund (:obj:`str`): name of the fund to retrieve recent historical data from.
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

                date || open | high | low | close
                -----||---------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx

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
        >>> investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp', as_json=False, order='ascending', debug=False)
            date || open | high | low | close
            -----||---------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx
    """

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

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
        funds = get_funds()

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    fund = fund.strip()

    if unidecode.unidecode(fund.lower()) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund.lower() + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced fund on Investing.com')

    for row in funds.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(fund.lower()):
            logger.info(str(fund) + ' found on Investing.com')

            url = "https://es.investing.com/funds/" + row.tag + "-historical-data"

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            logger.info('Request sent to Investing.com!')

            req = requests.get(url, headers=head, timeout=5)

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

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace('.', '').replace(',', '.'))
                    stock_open = float(info[2].replace('.', '').replace(',', '.'))
                    stock_high = float(info[3].replace('.', '').replace(',', '.'))
                    stock_low = float(info[4].replace('.', '').replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                logger.info('Data parsing process finished...')

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


def get_fund_historical_data(fund, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced `fund` from Investing
    via Web Scraping on the introduced date range. The resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` object with `ascending` or `descending` order.

    Args:
        fund (:obj:`str`): name of the fund to retrieve recent historical data from.
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

                date || open | high | low | close
                -----||---------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx

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
        >>> investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)
            date || open | high | low | close
            -----||---------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx

    """

    if not fund:
        raise ValueError("ERR#0029: fund parameter is mandatory and must be a valid fund name.")

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

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
        funds = get_funds()

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    fund = fund.strip()

    if unidecode.unidecode(fund.lower()) not in [unidecode.unidecode(value.lower()) for value in funds['name'].tolist()]:
        raise RuntimeError("ERR#0019: fund " + fund.lower() + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced fund on Investing.com')

    for row in funds.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(fund.lower()):
            logger.info(str(fund) + ' found on Investing.com')

            final = list()

            logger.info('Data parsing process starting...')

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
                            stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                            stock_close = float(info[1].replace('.', '').replace(',', '.'))
                            stock_open = float(info[2].replace('.', '').replace(',', '.'))
                            stock_high = float(info[3].replace('.', '').replace(',', '.'))
                            stock_low = float(info[4].replace('.', '').replace(',', '.'))

                            result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                    if data_flag is True:
                        if order in ['ascending', 'asc']:
                            result = result[::-1]
                        elif order in ['descending', 'desc']:
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
                    raise RuntimeError("ERR#0004: data retrieval error while scraping.")

            logger.info('Data parsing process finished...')

            if as_json is True:
                return json.dumps(final[0], sort_keys=False)
            elif as_json is False:
                return pd.concat(final)


def get_fund_information(fund, as_json=False):
    """
    This function retrieves basic financial information from the specified fund.
    As the information is also provided by Investing.com, the tags and names remain the same so
    a new Web Scraping process is not needed, the headers can be created with the existing information.
    The retrieved information from the fund can be valuable as it is additional information that can
    be used combined with OHLC values, so to determine financial insights from the company which holds
    the specified fund.

    Args:
        fund (:obj:`str`): name of the fund to retrieve the financial information from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` - fund_information:
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

    fund = fund.strip()

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
                        previous_close = float(elements_.xpath(".//span[contains(@class, 'float_lang_base_2')]")[0].text_content().replace('.', '').replace(',', '.'))
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
                            total_assets = int(float(value.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                        elif value.__contains__('M'):
                            total_assets = int(float(value.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                        elif value.__contains__('B'):
                            total_assets = int(float(value.replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)
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
                            market_cap = int(float(value.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                        elif value.__contains__('M'):
                            market_cap = int(float(value.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                        elif value.__contains__('B'):
                            market_cap = int(float(value.replace('B', '').replace('.', '').replace(',', '.')) * 1000000000)
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

                country | country_code | name | symbol | tag | id
                --------|--------------|------|--------|-----|----
                xxxxxxx | xxxxxxxxxxxx | xxxx | xxxxxx | xxx | xx

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing.
    """

    return es.etfs_as_df(country=country)


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

            In the case that the file reading of `etf_markets.csv` which contains the names and codes of the countries
            with etfs was successfully completed, the resulting :obj:`list` will look like::

                countries = ['australia', 'austria', 'belgium', 'brazil', ...]

    Raises:
        FileNotFoundError: raised when `etf_markets.csv` file is missing.
    """

    return es.retrieve_etf_countries()


def get_etf_list(country=None):
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


def get_etf_dict(country=None, columns=None, as_json=False):
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
                    'country_code': country_code,
                    'id': id,
                    'tag': tag,
                    'name': name,
                    'symbol': symbol
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing or empty.
    """

    return es.etfs_as_dict(country=country, columns=columns, as_json=as_json)


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

                date || open | high | low | close
                -----||---------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
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
        IOError: etfs object/file not found or unable to retrieve.
        RuntimeError: introduced etf does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if etf information was unavailable or not found.

    Examples:
        >>> investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50', country='spain', as_json=False, order='ascending', debug=False)
            date || open | high | low | close
            -----||---------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx
    """

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

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
        etfs = es.retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in [unidecode.unidecode(value.lower()) for value in etfs['country'].unique().tolist()]:
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    etfs = etfs[etfs['country'] == country]

    etf = etf.strip()

    if unidecode.unidecode(etf.lower()) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + etf.lower() + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced etf on Investing.com')

    for row in etfs.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(etf.lower()):
            logger.info(str(etf) + 'found on Investing.com')

            url = "https://es.investing.com/etfs/" + row.tag + "-historical-data"

            head = {
                "User-Agent": ua.get_random(),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "text/html",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }

            logger.info('Request sent to Investing.com!')

            req = requests.get(url, headers=head)

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

                    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    stock_close = float(info[1].replace('.', '').replace(',', '.'))
                    stock_open = float(info[2].replace('.', '').replace(',', '.'))
                    stock_high = float(info[3].replace('.', '').replace(',', '.'))
                    stock_low = float(info[4].replace('.', '').replace(',', '.'))

                    result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                logger.info('Data parsing process finished...')

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

                date || open | high | low | close
                -----||---------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx

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
        IOError: etfs object/file not found or unable to retrieve.
        RuntimeError: introduced etf does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if etf information was unavailable or not found.

    Examples:
        >>> investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50', country='spain', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)
            date || open | high | low | close
            -----||---------------------------
            xxxx || xxxx | xxxx | xxx | xxxxx

    """

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

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
        etfs = es.retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in [unidecode.unidecode(value.lower()) for value in etfs['country'].unique().tolist()]:
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    etfs = etfs[etfs['country'] == country]

    etf = etf.strip()

    if unidecode.unidecode(etf.lower()) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + str(etf.lower()) + " not found in " + str(country.lower()) + ", check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced etf on Investing.com')

    for row in etfs.itertuples():
        if unidecode.unidecode(row.name.lower()) == unidecode.unidecode(etf.lower()):
            logger.info(str(etf) + 'found on Investing.com')

            final = list()

            logger.info('Data parsing process starting...')

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
                                raise IndexError("ERR#0010: etf information unavailable or not found.")
                        else:
                            data_flag = True

                        if data_flag is True:
                            stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                            stock_close = float(info[1].replace('.', '').replace(',', '.'))
                            stock_open = float(info[2].replace('.', '').replace(',', '.'))
                            stock_high = float(info[3].replace('.', '').replace(',', '.'))
                            stock_low = float(info[4].replace('.', '').replace(',', '.'))

                            result.insert(len(result), Data(stock_date, stock_open, stock_high, stock_low, stock_close, None,))

                    if data_flag is True:
                        if order in ['ascending', 'asc']:
                            result = result[::-1]
                        elif order in ['descending', 'desc']:
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
        FileNotFoundError:  raised when `etf_markets.csv` file is missing.
        RuntimeError: raised it the introduced country does not match any of the indexed ones.
        ConnectionError: raised if GET requests does not return 200 status code.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etf_markets.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        markets = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0024: etf_markets file not found")

    countries = markets['country'].unique().tolist()

    if country not in countries:
        raise RuntimeError('ERR#0025: specified country value not valid.')

    url = "https://es.investing.com/etfs/" + country.replace(" ", "-") + "-etfs"

    req = requests.get(url, headers=head, timeout=15)

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

            name = element_.xpath(".//a")[0]

            last_path = ".//td[@class='" + 'pid-' + str(id_) + '-last' + "']"
            last = element_.xpath(last_path)[0].text_content()

            change_path = ".//td[contains(@class, '" + 'pid-' + str(id_) + '-pcp' + "')]"
            change = element_.xpath(change_path)[0].text_content()

            turnover_path = ".//td[contains(@class, '" + 'pid-' + str(id_) + '-turnover' + "')]"
            turnover = element_.xpath(turnover_path)[0].text_content()

            if turnover.__contains__('K'):
                turnover = int(float(turnover.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
            elif turnover.__contains__('M'):
                turnover = int(float(turnover.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
            else:
                turnover = int(float(turnover.replace('.', '').replace(',', '.')))

            data = {
                "name": name.text.strip(),
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
