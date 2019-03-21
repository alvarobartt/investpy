#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
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

            isin_code = get_isin_code(info)

            data = {
                "name": nested.text,
                "tag": info,
                "isin": isin_code,
                "id": id_
            }

            results.append(data)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results


def get_isin_code(info):
    url = "https://es.investing.com/equities/" + info
    headers = {
        'User-Agent': ua.get_random(),
        "X-Requested-With": "XMLHttpRequest"
    }

    req = requests.get(url, headers=headers, timeout=5)

    if req.status_code != 200:
        return None

    print(req.status_code)

    root_ = fromstring(req.text)
    path_ = root_.xpath("/html/body/div[5]/section/div[4]/div[1]/div[2]/div[3]/span[2]")

    return path_[0].text_content().rstrip()


def list_equities():
    resource_package = __name__
    resource_path = '/'.join(('resources', 'equities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        equities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        names = get_equity_names()
        equities = pd.DataFrame(names)

    return equities['name'].tolist()
