#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pkg_resources

from investpy import user_agent as ua


def get_fund_names():
    """
    This function retrieves all the available funds to retrieve data from.
    All the funds available can be found at: https://es.investing.com/funds/spain-funds?&issuer_filter=0

    Returns
    -------
        returns a dictionary containing all the funds information
    """

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://es.investing.com/funds/spain-funds?&issuer_filter=0"

    req = requests.get(url, headers=head)

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
            info = info.replace("/funds/", "")

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
    resource_path = '/'.join(('resources', 'funds.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results
