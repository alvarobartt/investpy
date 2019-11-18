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

from investpy.data.bonds_data import bonds_as_df, bonds_as_list, bonds_as_dict
from investpy.data.bonds_data import bond_countries_as_list


def get_bonds(country=None):
    """
    This function retrieves all the bonds data stored in `bonds.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the bonds data is properly
    structured in rows and columns, where columns are the bond data attribute names. Additionally, country
    filtering can be specified, which will make this function return not all the stored bond data, but just
    the data of the bonds from the introduced country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.

    Returns:
        :obj:`pandas.DataFrame` - bonds_df:
            The resulting :obj:`pandas.DataFrame` contains all the bond data from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | full name 
                --------|------|-----------
                xxxxxxx | xxxx | xxxxxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when bonds file was not found.
        IOError: raised when bond countries file is missing or empty.

    """

    return bonds_as_df(country)


def get_bonds_list(country=None):
    """
    This function retrieves all the bond names as stored in `stocks.csv` file, which contains all the
    data from the bonds as previously retrieved from Investing.com. So on, this function will just return
    the government bond names which will be one of the input parameters when it comes to bond data retrieval functions
    from investpy. Additionally, note that the country filtering can be applied, which is really useful since
    this function just returns the names and in bond data retrieval functions both the name and the country
    must be specified and they must match.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.

    Returns:
        :obj:`list` - bonds_list:
            The resulting :obj:`list` contains the all the bond names from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of bond names will look like::

                bonds_list = ['Argentina 1Y', 'Argentina 3Y', 'Argentina 5Y', 'Argentina 9Y', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when bonds file was not found.
        IOError: raised when bond countries file is missing or empty.
    
    """

    return bonds_as_list(country)


def get_bonds_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the bonds information stored in the `bonds.csv` file and formats it as a
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the
    JSON structure. Some optional paramaters can be specified such as the country, columns or as_json, which
    are a filtering by country so not to return all the bonds but just the ones from the introduced country,
    the column names that want to be retrieved in case of needing just some columns to avoid unnecessary information
    load, and whether the information wants to be returned as a JSON object or as a dictionary; respectively.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.
        columns (:obj:`list`, optional): column names of the bonds data to retrieve, can be: <country, name, full_name>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - bonds_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every bond as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                bonds_dict = {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when bonds file was not found.
        IOError: raised when bond countries file is missing or empty.

    """

    return bonds_as_dict(country=country, columns=columns, as_json=as_json)


def get_bond_countries():
    """
    This function returns a listing with all the available countries from where bonds can be retrieved, so to
    let the user know which of them are available, since the parameter country is mandatory in every bond retrieval
    function. Also, not just the available countries, but the required name is provided since Investing.com has a
    certain country name standard and countries should be specified the same way they are in Investing.com.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with government bonds as indexed in Investing.com

    Raises:
        FileNotFoundError: raised when bond countries file was not found.
        IOError: raised when bond countries file is missing or empty.

    """

    return bond_countries_as_list()


def get_bond_recent_data(bond, country, as_json=False, order='ascending', interval='Daily'):
    """
    This function retrieves recent historical data from the introduced bond from Investing.com. So on, the recent data
    of the introduced bond from the specified country will be retrieved and returned as a :obj:`pandas.DataFrame` if
    the parameters are valid and the request to Investing.com succeeds. Note that additionally some optional parameters
    can be specified: as_json and order, which let the user decide if the data is going to be returned as a
    :obj:`json` or not, and if the historical data is going to be ordered ascending or descending (where the index is the 
    date), respectively.

    Args:
        bond (:obj:`str`): name of the bond to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the bond is.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            recent data of the specified bond from the specified country. So on, the resulting dataframe contains the
            open, high, low and close values for the selected bond on market days.

            The resulting recent data, in case that the default parameters were applied, will look like::

                date || open | high | low | close 
                -----||---------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx 

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
        IOError: raised if bonds object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced bond/country was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if bond historical data was unavailable or not found in Investing.com.

    Examples:
        >>> investpy.get_bond_recent_data(bond='Argentina 3Y', country='argentina')
                        Open    High     Low   Close
            Date                                      
            2019-09-23  52.214  52.214  52.214  52.214
            2019-09-24  52.323  52.323  52.323  52.323
            2019-09-25  52.432  52.432  52.432  52.432
            2019-09-26  52.765  52.765  52.765  52.765
            2019-09-27  52.876  52.876  52.876  52.876
    
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

    if not interval:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

    if interval not in ['Daily', 'Weekly', 'Monthly']:
        raise ValueError("ERR#0073: interval value should be a str type and it can just be either 'Daily', 'Weekly' or 'Monthly'.")

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

    id_ = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'id']
    name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'name']
    full_name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'full_name']

    header = full_name + " Bond Yield Historical Data"

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
                raise IndexError("ERR#0069: bond information unavailable or not found.")
            
            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get('data-real-value'))

            bond_date = datetime.fromtimestamp(int(info[0]))
            bond_date = date(bond_date.year, bond_date.month, bond_date.day)

            bond_close = float(info[1].replace(',', ''))
            bond_open = float(info[2].replace(',', ''))
            bond_high = float(info[3].replace(',', ''))
            bond_low = float(info[4].replace(',', ''))

            result.insert(len(result),
                          Data(bond_date, bond_open, bond_high, bond_low, bond_close, None, None))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        if as_json is True:
            json_ = {
                'name': name,
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


def get_bond_historical_data(bond, country, from_date, to_date, as_json=False, order='ascending', interval='Daily'):
    """
    This function retrieves historical data from the introduced bond from Investing.com. So on, the historical data
    of the introduced bond from the specified country in the specified data range will be retrieved and returned as
    a :obj:`pandas.DataFrame` if the parameters are valid and the request to Investing.com succeeds. Note that additionally
    some optional parameters can be specified: as_json and order, which let the user decide if the data is going to
    be returned as a :obj:`json` or not, and if the historical data is going to be ordered ascending or descending (where the
    index is the date), respectively.

    Args:
        bond (:obj:`str`): name of the bond to retrieve historical data from.
        country (:obj:`str`): name of the country from where the bond is.
        from_date (:obj:`str`): date formatted as `dd/mm/yyyy`, since when data is going to be retrieved.
        to_date (:obj:`str`): date formatted as `dd/mm/yyyy`, until when data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified bond via argument. The dataset contains the open, high, low and close for the 
            selected bond on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close 
                -----||---------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx 

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
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
        IOError: raised if bonds object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced bond/country was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if bond historical data was unavailable or not found in Investing.com.

    Examples:
        >>> investpy.get_bond_historical_data(bond='Argentina 3Y', country='argentina', from_date='01/01/2010', to_date='01/01/2019')
                        Open  High   Low  Close
            Date                               
            2011-01-03  4.15  4.15  4.15   5.15
            2011-01-04  4.07  4.07  4.07   5.45
            2011-01-05  4.27  4.27  4.27   5.71
            2011-01-10  4.74  4.74  4.74   6.27
            2011-01-11  4.30  4.30  4.30   6.56

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

    id_ = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'id']
    name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'name']
    full_name = bonds.loc[(bonds['name'].str.lower() == bond).idxmax(), 'full_name']

    final = list()

    header = full_name + " Bond Yield Historical Data"

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
                        raise IndexError("ERR#0069: bond information unavailable or not found.")
                else:
                    data_flag = True
                
                if data_flag is True:
                    info = []

                    for nested_ in elements_.xpath(".//td"):
                        info.append(nested_.get('data-real-value'))

                    bond_date = datetime.fromtimestamp(int(info[0]))
                    bond_date = date(bond_date.year, bond_date.month, bond_date.day)

                    bond_close = float(info[1].replace(',', ''))
                    bond_open = float(info[2].replace(',', ''))
                    bond_high = float(info[3].replace(',', ''))
                    bond_low = float(info[4].replace(',', ''))

                    result.insert(len(result),
                                  Data(bond_date, bond_open, bond_high, bond_low, bond_close, None, None))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {
                        'name': name,
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

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def search_bonds(by, value):
    """
    This function searches bonds by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced one for the specified field which is the
    `bonds.csv` column name to search in. Available fields to search bonds are 'name' or 'full_name'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name which can be: 'name' or 'full_name'.
        value (:obj:`str`): value of the field to search for, which is the value that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting :obj:`pandas.DataFrame` contains the search results from the given query, which is
            any match of the specified value in the specified field. If there are no results for the given query,
            an error will be raised, but otherwise the resulting :obj:`pandas.DataFrame` will contain all the
            available bonds that match the introduced query.

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
