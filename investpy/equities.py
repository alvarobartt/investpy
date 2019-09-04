#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import time

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_equities(test_mode=False):
    """
    This function retrieves all the available `spanish equities` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the equities available can be found at: https://es.investing.com/equities/spain. Additionally,
    when equities are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to determine code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - equities:
            The resulting :obj:`pandas.DataFrame` contains all the spanish equities meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of spanish equities was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                name | full name | tag | isin | id
                -----|-----------|-----|------|----
                xxxx | xxxxxxxxx | xxx | xxxx | xx

    Raises:
        ValueError: if any of the introduced arguments is not valid.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if equities information was unavailable or not found.
    """

    params = {
        "noconstruct": "1",
        "smlID": "10119",
        "sid": "",
        "tabletype": "price",
        "index_id": "all"
    }

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/equities/StocksFilter"

    req = requests.get(url, params=params, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='cross_rate_markets_stocks_1']"
                        "/tbody"
                        "/tr")

    results = list()

    if path_:
        for elements_ in path_:
            id_ = elements_.get('id').replace('pair_', '')

            for element_ in elements_.xpath('.//a'):
                tag_ = element_.get('href').replace('/equities/', '')
                full_name_ = element_.get('title').replace(' (CFD)', '')

                info = retrieve_info(tag_)

                data = {
                    'name': element_.text.strip(),
                    'full_name': full_name_.rstrip(),
                    'tag': tag_,
                    'isin': info['isin'],
                    'id': id_,
                    'currency': info['currency'],
                }

                print(data)

                results.append(data)

            if test_mode is True:
                break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_info(tag):
    """
    This function retrieves both the ISIN code and the currency of an equity indexed in Investing.com, so to add
    additional information to the `equities.csv` file. The ISIN code will later be used in order to retrieve more
    information from the specified equity as the ISIN code is an unique identifier of every equity; and the currency
    which will be required in order to know which currency is the value in.

    Args:
        tag (:obj:`str`): is the tag of the equity to retrieve the information from as indexed by Investing.com.

    Returns:
        :obj:`dict` - info:
            The resulting :obj:`dict` contains the needed information for the equities listing, so on, both the the ISIN
             code of the introduced equity and the currency of its values.

    Raises:
        ConnectionError: raised if GET requests does not return 200 status code.
        IndexError: raised if either the isin code or the currency were unable to retrieve.
    """

    url = "https://es.investing.com/equities/" + tag

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

    result = {
        'isin': None,
        'currency': None
    }

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for element_ in path_:
        try:
            if element_.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
                code = element_.xpath("span[@class='elp']")[0].text_content().rstrip()
                # time.sleep(.5)
                result['isin'] = code
        except IndexError:
            raise IndexError("ERR#0017: isin code unable to retrieve.")

    path_ = root_.xpath(".//div[contains(@class, 'bottom')]"
                        "/span[@class='bold']")

    for element_ in path_:
        try:
            if element_.text_content():
                result['currency'] = element_.text_content()
        except IndexError:
            raise IndexError("ERR#0036: currency unable to retrieve.")

    return result


def retrieve_equity_countries(test_mode=False):
    """
    This function retrieves all the country names indexed in Investing.com with available equities to retrieve data
    from, via Web Scraping https://www.investing.com/equities/ where the available countries are listed, and from their
    names the specific equity website of every country is retrieved in order to get the ID which will later be used
    when retrieving all the information from the available equities in every country.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to determine code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - equity_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries with their corresponding ID,
            which will be used later by investpy.

    Raises:
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com equity listing.
    """

    headers = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/equities/'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath("//*[@id='countryDropdownContainer']/div")

    countries = list()

    for element in path:
        if element.get('id') != 'regionsSelectorContainer' and element.get('id') != 'cdregion0':
            for value in element.xpath(".//ul/li/a"):
                countries.append(value.get('href').replace('/equities/', '').strip())

    results = list()

    if len(countries) > 0:
        for country in countries:
            country_url = url + country

            req = requests.get(country_url, headers=headers)

            root = fromstring(req.text)
            path = root.xpath(".//*[@id='leftColumn']/input[@id='smlID']")

            country_id = path[0].get('value')

            obj = {
                'country': country,
                'id': country_id
            }

            results.append(obj)

            if test_mode:
                break
    else:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equity_countries.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def equity_countries_as_list():
    """
    This function retrieves all the country names indexed in Investing.com with available equities to retrieve data
    from, via reading the `equity_countries.csv` file from the resources directory. So on, this function will display a
    listing containing a set of countries, in order to let the user know which countries are taken into account and also
    the return listing from this function can be used for country param check if needed.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with equities as indexed in Investing.com

    Raises:
        IndexError: if `equity_countries.csv` was unavailable or not found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equity_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_equity_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0036: equity countries list not found or unable to retrieve.")
    else:
        return countries['country'].tolist()


def equities_as_df():
    """
    This function retrieves all the equities previously stored on `equities.csv` file, via
    `investpy.equities.retrieve_equities()`. The CSV file is read and if it does not exists,
    it is created again; but if it does exists, it is loaded into a :obj:`pandas.DataFrame`.

    Returns:
        :obj:`pandas.DataFrame` - equities_df:
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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = retrieve_equities()

    if equities is None:
        raise IOError("ERR#0001: equities list not found or unable to retrieve.")
    else:
        return equities


def equities_as_list():
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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        equities = retrieve_equities()

    if equities is None:
        raise IOError("ERR#0001: equities list not found or unable to retrieve.")
    else:
        return equities['name'].tolist()
