import pandas as pd
import requests
from bs4 import BeautifulSoup
import pkg_resources

from investing_scrapper import user_agent as ua


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
            info = nested.text.lower()
            info = info.replace(" ", "-")

            data = {
                "name": nested.text,
                "tag": info
            }

            results.append(data)

    resource_package = __name__
    resource_path = '/'.join(('resources', 'tickers.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)
    df.to_csv(file, index=False)

    return results