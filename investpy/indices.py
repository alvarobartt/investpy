#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json
import re

import pandas as pd
import pkg_resources

import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_indices(test_mode=False):
    """
    This function retrieves all the available `equities` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the equities available can be found at: https://es.investing.com/equities/. Additionally,
    when equities are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - indices:
            The resulting :obj:`pandas.DataFrame` contains all the indices meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of indices was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                country | name | full_name | tag | id | symbol | currency
                --------|------|-----------|-----|----|--------|----------
                xxxxxxx | xxxx | xxxxxxxxx | xxx | xx | xxxxxx | xxxxxxxx

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        FileNotFoundError: raised if `index_countries.csv` file does not exists or is empty.
        ConnectionError: raised if GET requests did not return 200 status code.
        IndexError: raised if indices information was unavailable or not found.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    results = list()

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'index_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise IOError("ERR#0036: equity countries list not found or unable to retrieve.")

    for country in countries['country'].tolist():
        head = {
            "User-Agent": ua.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/indices/" + country.replace(' ', '-') + "-indices?&majorIndices=on&primarySectors=on&additionalIndices=on&otherIndices=on"

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='cr1']/tbody/tr")

        if path_:
            for elements_ in path_:
                id_ = elements_.get('id').replace('pair_', '')

                for element_ in elements_.xpath('.//a'):
                    tag_ = element_.get('href')

                    if str(tag_).__contains__('/indices/'):
                        tag_ = tag_.replace('/indices/', '')
                        full_name_ = element_.get('title').replace(' (CFD)', '').strip()
                        name = element_.text.strip()

                        info = retrieve_index_info(tag_)

                        data = {
                            'country': 'united kingdom' if country == 'uk' else 'united states' if country == 'usa' else country,
                            'name': name,
                            'full_name': full_name_,
                            'tag': tag_,
                            'id': id_,
                            'symbol': info['symbol'],
                            'currency': info['currency'],
                            'market': 'world_indices'
                        }

                        results.append(data)

                if test_mode is True:
                    break

        if test_mode is True:
            break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'global_indices_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_index_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0036: equity countries list not found or unable to retrieve.")

    for index, row in countries.iterrows():
        head = {
            "User-Agent": ua.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        tag = row['tag'].replace('?',
                                 '?majorIndices=on&primarySectors=on&bonds=on&additionalIndices=on&otherIndices=on&')

        url = "https://www.investing.com/indices/" + tag

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='cr_12']/tbody/tr")

        if path_:
            for elements_ in path_:
                id_ = elements_.get('id').replace('pair_', '')

                for element_ in elements_.xpath('.//a'):
                    tag_ = element_.get('href')

                    if str(tag_).__contains__('/indices/'):
                        tag_ = tag_.replace('/indices/', '')
                        full_name_ = element_.get('title').replace(' (CFD)', '').strip()
                        name = element_.text.strip()

                        info = retrieve_index_info(tag_)

                        data = {
                            'country': row['country'],
                            'name': name,
                            'full_name': full_name_,
                            'tag': tag_,
                            'id': id_,
                            'symbol': info['symbol'],
                            'currency': info['currency'],
                            'market': 'global_indices'
                        }

                        results.append(data)

                if test_mode is True:
                    break

        if test_mode is True:
            break

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/indices/global-indices?majorIndices=on&primarySectors=on&bonds=on&additionalIndices=on&otherIndices=on&commodities=on"

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='cr_12']/tbody/tr")

    if path_:
        for elements_ in path_:
            id_ = elements_.get('id').replace('pair_', '')

            flags = elements_.xpath(".//td[@class='flag']/span")

            region = None

            for flag in flags:
                region = flag.get('title')

            if region == '':
                region = 'world'
            elif region == 'Euro Zone':
                region = region.lower()
            else:
                continue

            for element_ in elements_.xpath('.//a'):
                tag_ = element_.get('href')

                if str(tag_).__contains__('/indices/'):
                    tag_ = tag_.replace('/indices/', '')
                    full_name_ = element_.get('title').replace(' (CFD)', '').strip()
                    name = element_.text.strip()

                    info = retrieve_index_info(tag_)

                    data = {
                        'country': region,
                        'name': name,
                        'full_name': full_name_,
                        'tag': tag_,
                        'id': id_,
                        'symbol': info['symbol'],
                        'currency': info['currency'],
                        'market': 'global_indices'
                    }

                    results.append(data)

            if test_mode is True:
                break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_index_info(tag):
    """
    This function retrieves additional information from an index as listed in Investing.com. Every index data is
    retrieved and stored in a CSV in order to get all the possible information from it.

    Args:
        tag (:obj:`str`): is the identifying tag of the specified index.

    Returns:
        :obj:`dict` - index_data:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'currency': currency,
                    'symbol': symbol,
                }

    Raises:
        ConnectionError: raised if GET requests does not return 200 status code.
        IndexError: raised if fund information was unavailable or not found.
    """

    url = "https://www.investing.com/indices/" + tag

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
        'symbol': None,
    }

    root_ = fromstring(req.text)

    path_ = root_.xpath(".//div[@class='instrumentHead']"
                        "/h1")

    for element_ in path_:
        if element_.text_content():
            pattern = re.compile(r"\([a-zA-Z0-9\.\-\_\=]*?\)$")
            val = element_.text_content().strip()
            res = pattern.search(val)

            if res is not None:
                symbol = res.group()
                result['symbol'] = symbol.replace('(', '').replace(')', '')

    path_ = root_.xpath(".//div[contains(@class, 'bottom')]"
                        "/span[@class='bold']")

    for element_ in path_:
        if element_.text_content():
            result['currency'] = element_.text_content()

    return result


def retrieve_index_countries(test_mode=False):
    """
    This function retrieves all the country names indexed in Investing.com with available indices to
    retrieve data from, via Web Scraping https://www.investing.com/indices/world-indices where the available
    countries are listed.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - index_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries which have indices.

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com index listing.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    headers = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/indices/'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath("//select[@name='country']/option")

    countries = list()

    for element in path:
        if element.get('value') != '/indices/world-indices':
            obj = {
                'country': element.get('value').replace('/indices/', '').replace('-indices', '').replace('-', ' ').strip(),
                'country_name': unidecode.unidecode(element.text_content().strip().lower()),
            }

            countries.append(obj)

    if len(countries) <= 0:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'index_countries.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_global_indices_countries(test_mode=False):
    """
    This function retrieves all the country names & tags indexed in Investing.com with available indices to
    retrieve data from, via Web Scraping https://www.investing.com/global-indices/ where the available countries are
    listed, and from their names the specific indices website of every country is retrieved in order to get the tag
    which will later be used when retrieving all the information from the available indices in every country.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - equity_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries with their corresponding tag,
            which will be used later by investpy.

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com index listing.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    headers = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/indices/global-indices'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath("//select[@name='country']/option")

    countries = list()

    for element in path:
        if element.get('value') != '/indices/global-indices':
            obj = {
                'tag': element.get('value').replace('/indices/', ''),
                'country': unidecode.unidecode(element.text_content().strip().lower()),
            }

            countries.append(obj)

            if test_mode is True:
                break

    if len(countries) <= 0:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'global_indices_countries.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def index_countries_as_list():
    """
    This function retrieves all the country names indexed in Investing.com with available global indices to retrieve data
    from, via reading the `index_countries.csv` file from the resources directory. So on, this function will
    display a listing containing a set of countries, in order to let the user know which countries are taken into
    consideration and also the return listing from this function can be used for country param check if needed.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with indices as indexed in Investing.com

    Raises:
        IndexError: if `index_countries.csv` was unavailable or not found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'index_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_index_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0036: equity countries list not found or unable to retrieve.")
    else:
        for index, row in countries.iterrows():
            if row['country'] == 'uk':
                countries.loc[index, 'country'] = 'united kingdom'
            elif row['country'] == 'usa':
                countries.loc[index, 'country'] = 'united states'

        return countries['country'].tolist()


def global_indices_countries_as_list():
    """
    This function retrieves all the country names indexed in Investing.com with available global indices to retrieve data
    from, via reading the `global_indices_countries.csv` file from the resources directory. So on, this function will
    display a listing containing a set of countries, in order to let the user know which countries are taken into
    consideration and also the return listing from this function can be used for country param check if needed.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with global indices as indexed in Investing.com

    Raises:
        IndexError: if `global_indices_countries.csv` was unavailable or not found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'global_indices_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_index_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0036: equity countries list not found or unable to retrieve.")
    else:
        return countries['country'].tolist()


def indices_as_df(country=None):
    """
    This function retrieves all the available `indices` from Investing.com and returns them as a :obj:`pandas.DataFrame`,
    which contains not just the index names, but all the fields contained on the indices file.
    All the available indices can be found at: https://es.investing.com/indices/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`pandas.DataFrame` - indices_df:
            The resulting :obj:`pandas.DataFrame` contains all the indices basic information retrieved from Investing.com,
            some of which is not useful for the user, but for the inner package functions, such as the `tag` field,
            for example.

            In case the information was successfully retrieved, the :obj:`pandas.DataFrame` will look like::

                country | name | full_name | tag | id | symbol | currency
                --------|------|-----------|-----|----|--------|----------
                xxxxxxx | xxxx | xxxxxxxxx | xxx | xx | xxxxxx | xxxxxxxx

            Just like `investpy.indices.retrieve_indices()`, the output of this function is a :obj:`pandas.DataFrame`,
            but instead of generating the CSV file, this function just reads it and loads it into a
            :obj:`pandas.DataFrame` object.

    Raises:
        IOError: raised if the indices file from `investpy` is missing or errored.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        indices = retrieve_indices()

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    if country is None:
        indices.reset_index(drop=True, inplace=True)
        return indices
    elif unidecode.unidecode(country.lower()) in index_countries_as_list():
        indices = indices[indices['country'] == unidecode.unidecode(country.lower())]
        indices.reset_index(drop=True, inplace=True)
        return indices


def indices_as_list(country=None):
    """
    This function retrieves all the available indices and returns a list of each one of them.
    All the available indices can be found at: https://es.investing.com/indices/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`list` - indices_list:
            The resulting :obj:`list` contains the retrieved data, which corresponds to the index names of
            every index listed on Investing.com.

            In case the information was successfully retrieved from the CSV file, the :obj:`list` will look like::

                indices = ['S&P Merval', 'S&P Merval Argentina', 'S&P/BYMA Argentina General', ...]

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: raised if the indices file from `investpy` is missing or errored.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        indices = retrieve_indices()

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    if country is None:
        return indices['name'].tolist()
    elif unidecode.unidecode(country.lower()) in index_countries_as_list():
        return indices[indices['country'] == unidecode.unidecode(country.lower())]['name'].tolist()


def indices_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available indices on Investing.com and returns them as a :obj:`dict` containing the
    `country`, `name`, `full_name`, `symbol`, `tag` and `currency`. All the available indices can be found at:
    https://es.investing.com/indices/

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
        ValueError: raised when the introduced arguments are not correct.
        IOError: raised if the indices file from `investpy` is missing or errored.
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        indices = retrieve_indices()

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    if columns is None:
        columns = indices.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in indices.columns.tolist() for column in columns):
        raise ValueError("ERR#0023: specified columns does not exist, available columns are "
                         "<country, name, full_name, symbol, tag, id, currency>")

    if country is None:
        if as_json:
            return json.dumps(indices[columns].to_dict(orient='records'))
        else:
            return indices[columns].to_dict(orient='records')
    elif country in index_countries_as_list():
        if as_json:
            return json.dumps(indices[indices['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records'))
        else:
            return indices[indices['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records')
