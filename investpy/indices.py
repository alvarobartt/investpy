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

from investpy.data.indices_data import indices_as_df, indices_as_list, indices_as_dict
from investpy.data.indices_data import index_countries_as_list


def get_indices(country=None):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`pandas.DataFrame` with all the information of every available index. If the country
    filtering is applied, just the indices from the introduced country are going to be returned.
    All the available indices can be found at: https://www.investing.com/indices/world-indices and at
    https://www.investing.com/indices/world-indices, since both world and global indices are retrieved.

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
        FileNotFoundError: raised if the indices file was not found.
        IOError: raised if the indices file from `investpy` is missing or errored.
    
    """

    return indices_as_df(country=country)


def get_indices_list(country=None):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`list` with the names of every available index. If the country filtering is applied, just
    the indices from the introduced country are going to be returned.
    All the available indices can be found at: https://www.investing.com/indices/world-indices and at
    https://www.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`list` - indices_list:
            The resulting :obj:`list` contains the retrieved data, which corresponds to the index names of
            every index listed in Investing.com.

            In case the information was successfully retrieved, the :obj:`list` will look like::

                indices = ['S&P Merval', 'S&P Merval Argentina', 'S&P/BYMA Argentina General', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if the indices file was not found.
        IOError: raised if the indices file is missing or errored.
    
    """

    return indices_as_list(country=country)


def get_indices_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`dict` with all the information of every available index. If the country
    filtering is applied, just the indices from the introduced country are going to be returned. Additionally, the
    columns to retrieve data from can be specified as a parameter formatted as a :obj:`list`.
    All the available indices can be found at: https://www.investing.com/indices/world-indices and at
    https://www.investing.com/indices/world-indices, since both world and global indices are retrieved.

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
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if the indices file was not found.
        IOError: raised if the indices file is missing or errored.
    
    """

    return indices_as_dict(country=country, columns=columns, as_json=as_json)


def get_index_countries():
    """
    This function retrieves all the country names indexed in Investing.com with available indices to retrieve data
    from, via reading the `indices.csv` file from the resources directory. So on, this function will display a listing
    containing a set of countries, in order to let the user know which countries are available for indices data retrieval.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with indices as indexed in Investing.com

    Raises:
        FileNotFoundError: raised if the indices file was not found.
        IOError: raised if the indices file is missing or errored.
    
    """

    return index_countries_as_list()


def get_index_recent_data(index, country, as_json=False, order='ascending', interval='Daily'):
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
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

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

    if not interval:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if interval not in ['Daily', 'Weekly', 'Monthly']:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    resource_package = 'investpy'
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

    full_name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'full_name']
    id_ = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'id']
    name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'name']

    index_currency = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'currency']

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
                raise IndexError("ERR#0046: index information unavailable or not found.")

            info = []
        
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get('data-real-value'))

            index_date = datetime.fromtimestamp(int(info[0]))
            index_date = date(index_date.year, index_date.month, index_date.day)
            
            index_close = float(info[1].replace(',', ''))
            index_open = float(info[2].replace(',', ''))
            index_high = float(info[3].replace(',', ''))
            index_low = float(info[4].replace(',', ''))

            index_volume = 0

            if info[5].__contains__('K'):
                index_volume = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
            elif info[5].__contains__('M'):
                index_volume = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
            elif info[5].__contains__('B'):
                index_volume = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

            result.insert(len(result), Data(index_date, index_open, index_high, index_low,
                                            index_close, index_volume, index_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

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



def get_index_historical_data(index, country, from_date, to_date, as_json=False, order='ascending', interval='Daily'):
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
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            historical data from the specified index via argument. The dataset contains the open, high, low, close and
            volume values for the selected index on market days, additionally the currency in which those values are
            specified is returned.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Volume | Currency
                -----||------|------|-----|-------|--------|----------
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
        datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

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

    full_name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'full_name']
    id_ = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'id']
    name = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'name']

    index_currency = indices.loc[(indices['name'].str.lower() == index).idxmax(), 'currency']

    final = list()

    header = full_name + ' Historical Data'

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
                        raise IndexError("ERR#0046: index information unavailable or not found.")
                else:
                    data_flag = True

                info = []
        
                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get('data-real-value'))

                if data_flag is True:
                    index_date = datetime.fromtimestamp(int(info[0]))
                    index_date = date(index_date.year, index_date.month, index_date.day)
                    
                    index_close = float(info[1].replace(',', ''))
                    index_open = float(info[2].replace(',', ''))
                    index_high = float(info[3].replace(',', ''))
                    index_low = float(info[4].replace(',', ''))

                    index_volume = 0

                    if info[5].__contains__('K'):
                        index_volume = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
                    elif info[5].__contains__('M'):
                        index_volume = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
                    elif info[5].__contains__('B'):
                        index_volume = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

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

    resource_package = 'investpy'
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
