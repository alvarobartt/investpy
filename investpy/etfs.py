#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import time

import pandas as pd
import requests
import json
import pkg_resources
from lxml.html import fromstring

from investpy import user_agent as ua


def get_etf_names():
    """
    This function retrieves all the available etfs to retrieve data from.
    All the available etfs available can be found at: https://es.investing.com/etfs/spain-etfs

    Returns
    -------
        :returns a dictionary containing all the etfs information
    """

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/etfs/spain-etfs"

    req = requests.get(url, headers=head, timeout=5)

    if req.status_code != 200:
        raise ConnectionError("ERR#015: error " + req.status_code + ", try again later.")

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
            info = nested.get('href').replace('/etfs/', '')

            if symbol:
                data = {
                    "name": nested.text,
                    "symbol": symbol,
                    "tag": info,
                    "id": id_
                }
            else:
                data = {
                    "name": nested.text,
                    "symbol": "undefined",
                    "tag": info,
                    "id": id_
                }

            results.append(data)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'etfs.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results


def list_etfs():
    """
    This function retrieves all the available etfs and returns a list of each one of them.
    All the available etfs can be found at: https://es.investing.com/etfs/spain-etfs

    Returns
    -------
        :returns a list with all the available etfs to retrieve data from
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_etf_names()
        etfs = pd.DataFrame(names)

    if etfs is None:
        raise IOError("ERR#009: etf list not found or unable to retrieve.")
    else:
        return etfs['name'].tolist()


def dict_etfs(columns=None, as_json=False):
    """
    This function retrieves all the available etfs and returns a dictionary with the specified columns.
    Available columns are: 'id', 'name', 'symbol' and 'tag'
    All the available etfs can be found at: https://es.investing.com/etfs/spain-etfs

    Returns
    -------
        :returns a dictionary that contains all the available etf values specified in the columns
    """

    if columns is None:
        columns = ['id', 'name', 'symbol', 'tag']
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#020: specified columns argument is not a list, it can just be list type.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'es', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_etf_names()
        etfs = pd.DataFrame(names)

    if etfs is None:
        raise IOError("ERR#009: etf list not found or unable to retrieve.")

    if not all(column in etfs.columns.tolist() for column in columns):
        raise ValueError("ERR#021: specified columns does not exist, available columns are <id, name, symbol, tag>")

    if as_json:
        return json.dumps(etfs[columns].to_dict(orient='records'))
    else:
        return etfs[columns].to_dict(orient='records')
