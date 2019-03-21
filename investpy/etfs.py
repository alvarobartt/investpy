#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pkg_resources

from investpy import user_agent as ua


def get_etf_names():
    """
    This function retrieves all the available etfs to retrieve data from.
    All the funds available can be found at: https://es.investing.com/etfs/spain-etfs

    Returns
    -------
        returns a dictionary containing all the etfs information
    """

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://es.investing.com/etfs/spain-etfs"

    req = requests.get(url, headers=head, timeout=5)
    html = BeautifulSoup(req.content, 'html.parser')
    selection = html.select("table#etfs > tbody > tr")

    results = list()

    for element in selection:
        id_ = element.get('id')
        id_ = id_.replace('pair_', '')

        symbol = None
        for symbol in element.select("td.symbol"):
            symbol = symbol.get("title")

        for nested in element.select("a"):
            info = nested.get("href")
            info = info.replace("/etfs/", "")

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
    resource_path = '/'.join(('resources', 'etfs.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results


def list_etfs():
    resource_package = __name__
    resource_path = '/'.join(('resources', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_etf_names()
        etfs = pd.DataFrame(names)

    return etfs['name'].tolist()
