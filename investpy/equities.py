#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import time

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy import user_agent as ua


def get_equity_names():
    """
    This function retrieves all the available equities to retrieve data from.
    All the equities available can be found at: https://es.investing.com/equities/spain

    Returns
    -------
        :returns a dictionary containing all the equities information
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
        raise ConnectionError("ERR#015: error " + req.status_code + ", try again later.")

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
                    isin_ = get_isin_code(tag_)
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

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'equities.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results


def get_isin_code(info):
    """
    This is an additional function that adds data to the equities pandas.DataFrame.
    Added data in this case, are the ISIN codes of every company in order to identify it.

    Returns
    -------
        :returns a str that contains the ISIN code of the specified equity
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
        raise ConnectionError("ERR#015: error " + req.status_code + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for p in path_:
        try:
            if p.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
                try:
                    code = p.xpath("span[@class='elp']")[0].text_content().rstrip()
                    time.sleep(.5)

                    return code
                except IndexError:
                    raise IndexError("ERR#017: isin code unavailable or not found.")
            else:
                continue
        except IndexError:
            raise IndexError("ERR#017: isin code unavailable or not found.")

    return None


def list_equities():
    """
    This function retrieves all the available equities and returns a list of each one of them.
    All the available equities can be found at: https://es.investing.com/equities/spain

    Returns
    -------
        :returns a list with all the available equities to retrieve data from
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_equity_names()
        equities = pd.DataFrame(names)

    if equities is None:
        raise IOError("ERR#001: equities list not found or unable to retrieve.")
    else:
        return equities['name'].tolist()
