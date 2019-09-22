#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_index_countries(test_mode=False):
    """
    This function retrieves all the country names indexed in Investing.com with available equities to retrieve data
    from, via Web Scraping https://www.investing.com/equities/ where the available countries are listed, and from their
    names the specific equity website of every country is retrieved in order to get the ID which will later be used
    when retrieving all the information from the available equities in every country.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - equity_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries with their corresponding ID,
            which will be used later by investpy.

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com equity listing.
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


def index_countries_as_list():
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
    resource_path = '/'.join(('resources', 'indices', 'index_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        countries = retrieve_index_countries(test_mode=False)

    if countries is None:
        raise IOError("ERR#0036: equity countries list not found or unable to retrieve.")
    else:
        return countries['country'].tolist()
