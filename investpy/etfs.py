#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json

import unidecode

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_etfs(test_mode=False):
    """
    This function retrieves all the available `world etfs` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the etfs available can be found at: https://es.investing.com/etfs/world-etfs. Additionally,
    when etfs are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - etfs:
            The resulting :obj:`pandas.DataFrame` contains all the world etfs meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of world etfs was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                country | name | symbol | tag | id | currency
                --------|------|--------|-----|----|----------
                xxxxxxx | xxxx | xxxxxx | xxx | xx | xxxxxxxx

    Raises:
        ValueError: if any of the introduced arguments is not valid.
        FileNotFoundError: raised when `etf_countries.csv` file is missing.
        ConnectionError: if GET requests does not return 200 status code.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etf_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        markets = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0044: etf_countries file not found")

    final = list()

    for index, row in markets.iterrows():
        url = "https://es.investing.com/etfs/" + row['country'].replace(" ", "-") + "-etfs"

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='etfs']"
                            "/tbody"
                            "/tr")

        results = list()

        if path_:
            for elements_ in path_:
                id_ = elements_.get('id').replace('pair_', '')
                symbol = elements_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

                nested = elements_.xpath(".//a")[0]
                tag = nested.get('href').replace('/etfs/', '')

                info = retrieve_etf_info(tag)

                data = {
                    "country": 'united kingdom' if row['country'] == 'uk' else 'united states' if row['country'] == 'usa' else row['country'],
                    "name": nested.text.strip(),
                    "symbol": symbol,
                    "tag": tag,
                    "id": id_,
                    "currency": info['currency'],
                }

                results.append(data)

                if test_mode is True:
                    break

        final.extend(results)

        if test_mode is True:
            break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(final)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_etf_info(tag):
    """
    This function retrieves additional information from the specified etf as indexed in Investing.com, in order to add
    more information to `etfs.csv` which can later be useful. Currently just the currency value is retrieved, since it
    is needed so to determine in which currency the historical data values are.

    Args:
       tag (:obj:`str`): is the tag of the etf to retrieve the information from as indexed by Investing.com.

    Returns:
       :obj:`dict` - info:
           The resulting :obj:`dict` contains the needed information for the etfs listing.

    Raises:
       ConnectionError: raised if GET requests does not return 200 status code.
       IndexError: raised if the information from the etf was not found or unable to retrieve.
    """

    url = "https://es.investing.com/etfs/" + tag

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

    result = {
        'currency': None,
    }

    root_ = fromstring(req.text)

    path_ = root_.xpath(".//div[contains(@class, 'bottom')]"
                        "/span[@class='bold']")

    for element_ in path_:
        if element_.text_content():
            result['currency'] = element_.text_content()

    return result


def etf_countries_as_list():
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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etf_countries.csv'))

    if pkg_resources.resource_exists(resource_package, resource_path):
        markets = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0044: etf_countries file not found")

    for index, row in markets.iterrows():
        if row['country'] == 'uk':
            markets.iloc[index, 'country'] = 'united kingdom'
        elif row['country'] == 'usa':
            markets.iloc[index, 'country'] = 'united states'

    return markets['country'].tolist()


def etfs_as_df(country=None):
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

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        etfs = retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etf list not found or unable to retrieve.")

    if country is None:
        etfs.reset_index(drop=True, inplace=True)
        return etfs
    elif unidecode.unidecode(country.lower()) in etf_countries_as_list():
        etfs = etfs[etfs['country'] == unidecode.unidecode(country.lower())]
        etfs.reset_index(drop=True, inplace=True)
        return etfs


def etfs_as_list(country=None):
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

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        etfs = retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etf list not found or unable to retrieve.")

    if country is None:
        return etfs['name'].tolist()
    elif country in etf_countries_as_list():
        return etfs[etfs['country'] == unidecode.unidecode(country.lower())]['name'].tolist()


def etfs_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available etfs indexed on Investing.com, already
    stored on `etfs.csv`, which if does not exists, will be created by `investpy.etfs.retrieve_etfs()`.
    This function also allows the user to specify which country do they want to retrieve data from,
    or from every listed country; the columns which the user wants to be included on the resulting
    :obj:`dict`; and the output of the function will either be a :obj:`dict` or a :obj:`json`.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.
        columns (:obj:`list`, optional):
            names of the columns of the etf data to retrieve <country, country_code, id, name, symbol, tag>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

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

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        etfs = retrieve_etfs()

    if etfs is None:
        raise IOError("ERR#0009: etf list not found or unable to retrieve.")

    if columns is None:
        columns = etfs.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in etfs.columns.tolist() for column in columns):
        raise ValueError("ERR#0021: specified columns does not exist, available columns are "
                         "<country, id, name, symbol, tag, currency>")

    if country is None:
        if as_json:
            return json.dumps(etfs[columns].to_dict(orient='records'))
        else:
            return etfs[columns].to_dict(orient='records')
    elif country in etf_countries_as_list():
        if as_json:
            return json.dumps(etfs[etfs['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records'))
        else:
            return etfs[etfs['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records')
