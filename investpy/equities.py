#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup
import pkg_resources

from investpy import user_agent as ua


def get_equity_names():
    """
    This function retrieves all the available equities to retrieve data from.
    All the equities available can be found at: https://es.investing.com/equities/spain

    Returns
    -------
        returns a dictionary containing all the equities information
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
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://es.investing.com/equities/StocksFilter"

    req = requests.get(url, params=params, headers=head)

    html = BeautifulSoup(req.content, 'html.parser')

    selection = html.select("table#cross_rate_markets_stocks_1 > tbody > tr")

    results = list()

    for element in selection:
        id_ = element.get("id")
        id_ = id_.replace('pair_', '')
        for nested in element.select("a"):
            info = nested.get("href")
            info = info.replace("/equities/", "")

            data = {
                "name": nested.text,
                "tag": info,
                "id": id_
            }

            results.append(data)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results
