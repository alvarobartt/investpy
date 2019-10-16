#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy.utils import user_agent


def retrieve_bonds(test_mode=False):
    """
    This function retrieves all the available `government bonds` indexed on Investing.com, so to retrieve data 
    from them which will be used later in inner functions for data retrieval. Additionally, when indices are 
    retrieved all the information is both returned as a :obj:`pandas.DataFrame` and stored on a CSV file on a 
    package folder containing all the available resources.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - indices:
            The resulting :obj:`pandas.DataFrame` contains all the bonds information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of indices was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                country | name | full_name | tag | id 
                --------|------|-----------|-----|----
                xxxxxxx | xxxx | xxxxxxxxx | xxx | xx 

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        FileNotFoundError:
            raised if `bond_countries.csv` files do not exist or are empty.
        ConnectionError: raised if GET requests did not return 200 status code.
        IndexError: raised if bonds information was unavailable or not found.
    
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    results = list()

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'bonds', 'bond_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    for country in countries['tag'].tolist():
        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/rates-bonds/" + country + "-government-bonds"

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

                    if str(tag_).__contains__('/rates-bonds/'):
                        tag_ = tag_.replace('/rates-bonds/', '')
                        full_name_ = element_.get('title').strip()
                        name = element_.text.strip()

                        data = {
                            'country': 'united kingdom' if country == 'uk' else 'united states' if country == 'usa' else country,
                            'name': name,
                            'full_name': full_name_,
                            'tag': tag_,
                            'id': id_,
                        }

                        results.append(data)

        if test_mode is True:
            break

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'bonds', 'bonds.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    df = df.where((pd.notnull(df)), None)
    df.drop_duplicates(subset="tag", keep='first', inplace=True)
    df.sort_values('country', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df


def retrieve_bond_countries(test_mode=False):
    """
    This function retrieves all the country names indexed in Investing.com with available government bonds to retrieve data
    from. This process is made in order to dispose of a listing with all the countries from where bond information
    can be retrieved from Investing.com. So on, the retrieved country listing will be used whenever the bonds are
    retrieved, while looping over it.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - bond_countries:
            The resulting :obj:`pandas.DataFrame` contains all the available countries which have available government 
            bonds as indexed in Investing.com, from which bond data is going to be retrieved.

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were found in the Investing.com government bonds listing.

    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    headers = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/rates-bonds/'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath("//select[@name='country']/option")

    countries = list()

    for element in path:
        if element.get('exchangeid') != "":
            obj = {
                'exchange_id': int(element.get('exchangeid')),
                'tag': element.get('value').replace('/rates-bonds/', '').replace('-government-bonds', ''),
                'country_id': int(element.get('data-country-id')),
                'country': element.text_content().lower(),
            }

            countries.append(obj)

    if len(countries) == 0:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'bonds', 'bond_countries.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df
