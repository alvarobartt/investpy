#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = 'Alvaro Bartolome <alvarob96@usal.es>'
__version__ = '0.8.6'

import time

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_equities(debug_mode=False):
    """
    This function retrieves all the available `spanish equities` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the equities available can be found at: https://es.investing.com/equities/spain. Additionally,
    when equities are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        debug_mode (:obj:`boolean`):
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

                try:
                    isin_ = retrieve_isin_code(tag_)
                except (ConnectionError, IndexError):
                    isin_ = None

                data = {
                    "name": element_.text,
                    "full_name": full_name_.rstrip(),
                    "tag": tag_,
                    "isin": isin_,
                    "id": id_
                }

                results.append(data)

            if debug_mode is True:
                break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities', 'equities.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return df


def retrieve_isin_code(info):
    """
    This function retrieves the ISIN code from an equity which will lead to
    the later company profile extraction as the ISIN code is the identifier
    used by "Bolsa de Madrid", so to retrieve the company profile. The ISIN
    code will be added to the `equities.csv` file, as additional information.

    Args:
        info (:obj:`str`): is the tag of the equity to retrieve the ISIN code from as indexed by Investing.com.

    Returns:
        :obj:`str` - isin_code:
            The resulting :obj:`str` contains the ISIN code of the introduced equity.

    Raises:
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if isin code was unavailable or not found.
    """

    url = "https://es.investing.com/equities/" + info

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
    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for p in path_:
        try:
            if p.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
                code = p.xpath("span[@class='elp']")[0].text_content().rstrip()
                time.sleep(.5)

                return code
            else:
                continue
        except IndexError:
            raise IndexError("ERR#0017: isin code unavailable or not found.")

    return None


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
