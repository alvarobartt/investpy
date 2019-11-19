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

from investpy.data.commodities_data import commodities_as_df, commodities_as_list, commodities_as_dict
from investpy.data.commodities_data import commodity_groups_list


def get_commodities(group=None):
    """
    This function retrieves all the commodities data stored in `commodities.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the commodities data is properly
    structured in rows and columns, where columns are the commodity data attribute names. Additionally, group
    filtering can be specified, so that the return commodities are from the specified group instead from every
    available group. Anyways, since it is an optional parameter it does not need to be specified, which means that
    if it is None or not specified, all the available commodities will be returned.

    Args:
        group (:obj:`str`, optional): name of the group to retrieve all the available commodities from.

    Returns:
        :obj:`pandas.DataFrame` - commodities_df:
            The resulting :obj:`pandas.DataFrame` contains all the commodities data from the introduced group if specified,
            or from all the commodity groups if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                title | country | name | full_name | currency | group 
                ------|---------|------|-----------|----------|-------
                xxxxx | xxxxxxx | xxxx | xxxxxxxxx | xxxxxxxx | xxxxx 

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when commodities file was not found.
        IOError: raised when commodities file is missing or empty.

    """

    return commodities_as_df(group=group)


def get_commodities_list(group=None):
    """
    This function retrieves all the commodity names as stored in `commodities.csv` file, which contains all the
    data from the commodities as previously retrieved from Investing.com. So on, this function will just return
    the commodity names from either all the available groups or from any group, which will later be used when it 
    comes to both recent and historical data retrieval.

    Args:
        group (:obj:`str`, optional): name of the group to retrieve all the available commodities from.

    Returns:
        :obj:`list` - commodities_list:
            The resulting :obj:`list` contains the all the commodity names from the introduced group if specified,
            or from every group if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of commodity names will look like::

                commodities_list = ['Gold', 'Copper', 'Silver', 'Palladium', 'Platinum', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when commodities file was not found.
        IOError: raised when commodities file is missing or empty.
    
    """

    return commodities_as_list(group=group)


def get_commodities_dict(group=None, columns=None, as_json=False):
    """
    This function retrieves all the commodities information stored in the `commodities.csv` file and formats it as a
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the
    JSON structure. Some optional paramaters can be specified such as the group, columns or as_json, which
    are the name of the commodity group to filter between all the available commodities so not to return all the 
    commodities but just the ones from the introduced group, the column names that want to be retrieved in case 
    of needing just some columns to avoid unnecessary information load, and whether the information wants to be 
    returned as a JSON object or as a dictionary; respectively.

    Args:
        group (:obj:`str`, optional): name of the group to retrieve all the available commodities from.
        columns (:obj:`list`, optional):
            column names of the commodities data to retrieve, can be: <title, country, name, full_name, currency, group>
        as_json (:obj:`bool`, optional):
            if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - bonds_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every bond as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                commodities_dict = {
                    'title': title,
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'currency': currency,
                    'group': group,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when commodities file was not found.
        IOError: raised when commodities file is missing or empty.

    """

    return commodities_as_dict(group=group, columns=columns, as_json=as_json)


def get_commodity_groups():
    """
    This function returns a listing with all the available commodity groupsson that a filtering can be applied when
    retrieving data from commodities. The current available commodity groups are metals, agriculture and energy, 
    which include all the raw materials or commodities included in them.

    Returns:
        :obj:`list` - commodity_groups:
            The resulting :obj:`list` contains all the available commodity groups as indexed in Investing.com

    Raises:
        FileNotFoundError: raised when commodities file was not found.
        IOError: raised when comodities file is missing or empty.

    """

    return commodity_groups_list()


def get_commodity_recent_data(commodity, as_json=False, order='ascending', interval='Daily'):
    """
    """

    if not commodity:
        raise ValueError("ERR#0078: commodity parameter is mandatory and must be a valid commodity name.")

    if not isinstance(commodity, str):
        raise ValueError("ERR#0078: commodity parameter is mandatory and must be a valid commodity name.")

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
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodity = commodity.strip()
    commodity = commodity.lower()

    if unidecode.unidecode(commodity) not in [unidecode.unidecode(value.lower()) for value in commodities['name'].tolist()]:
        raise RuntimeError("ERR#0079: commodity " + commodity + " not found, check if it is correct.")

    full_name = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'full_name']
    id_ = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'id']
    name = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'name']

    currency = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'currency']

    header = full_name + ' Historical Data'

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
                raise IndexError("ERR#0080: commodity information unavailable or not found.")

            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get('data-real-value'))

            commodity_date = datetime.fromtimestamp(int(info[0]))
            commodity_date = date(commodity_date.year, commodity_date.month, commodity_date.day)
            
            commodity_close = float(info[1].replace(',', ''))
            commodity_open = float(info[2].replace(',', ''))
            commodity_high = float(info[3].replace(',', ''))
            commodity_low = float(info[4].replace(',', ''))

            result.insert(len(result),
                          Data(commodity_date, commodity_open, commodity_high, commodity_low,
                               commodity_close, None, currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        if as_json is True:
            json_ = {
                'name': name,
                'recent':
                    [value.commodity_as_json() for value in result]
            }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.commodity_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_commodity_historical_data(commodity, from_date, to_date, as_json=False, order='ascending', interval='Daily'):
    """
    """

    if not commodity:
        raise ValueError("ERR#0078: commodity parameter is mandatory and must be a valid commodity name.")

    if not isinstance(commodity, str):
        raise ValueError("ERR#0078: commodity parameter is mandatory and must be a valid commodity name.")

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
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodity = commodity.strip()
    commodity = commodity.lower()

    if unidecode.unidecode(commodity) not in [unidecode.unidecode(value.lower()) for value in commodities['name'].tolist()]:
        raise RuntimeError("ERR#0079: commodity " + commodity + " not found, check if it is correct.")

    full_name = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'full_name']
    id_ = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'id']
    name = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'name']

    currency = commodities.loc[(commodities['name'].str.lower() == commodity).idxmax(), 'currency']

    header = full_name + ' Historical Data'

    final = list()

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
                        raise IndexError("ERR#0080: commodity information unavailable or not found.")
                else:
                    data_flag = True
                
                info = []
            
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get('data-real-value'))

                if data_flag is True:
                    commodity_date = datetime.fromtimestamp(int(info[0]))
                    commodity_date = date(commodity_date.year, commodity_date.month, commodity_date.day)
                    
                    commodity_close = float(info[1].replace(',', ''))
                    commodity_open = float(info[2].replace(',', ''))
                    commodity_high = float(info[3].replace(',', ''))
                    commodity_low = float(info[4].replace(',', ''))

                    result.insert(len(result),
                                Data(commodity_date, commodity_open, commodity_high, commodity_low,
                                    commodity_close, None, currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {
                        'name': name,
                        'recent':
                            [value.commodity_as_json() for value in result]
                    }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.commodity_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)

        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def search_commodities(by, value):
    """
    This function searches commodities by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced one for the specified field which is the
    `commodities.csv` column name to search in. Available fields to search commodities are 'name', 'full_name' and 'title'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name which can be: ''name', 'full_name' or 'title'.
        value (:obj:`str`): value of the field to search for, which is the value that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting :obj:`pandas.DataFrame` contains the search results from the given query, which is
            any match of the specified value in the specified field. If there are no results for the given query,
            an error will be raised, but otherwise the resulting :obj:`pandas.DataFrame` will contain all the
            available commodities that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised if no results were found for the introduced value in the introduced field.

    """

    available_search_fields = ['name', 'full_name', 'title']

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
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities['matches'] = commodities[by].str.contains(value, case=False)

    search_result = commodities.loc[commodities['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result