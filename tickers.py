import pandas as pd
import requests
import unidecode
from bs4 import BeautifulSoup

import user_agent as ua


def get_ticker_names():
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
        for nested in element.select("a"):
            info = unidecode.unidecode(nested.text).lower()
            info = info.replace(" ", "-")

            data = {
                "name": nested.text,
                "tag": info
            }

            results.append(data)

    return results


def convert_tickers_into_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('tickers.csv', index=True)