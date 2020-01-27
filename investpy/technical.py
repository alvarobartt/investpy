#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd

import pkg_resources
import requests
import unidecode
from lxml.html import fromstring


def technical_analysis(name, country, product_type, interval):
    """
    This function ...
    """

    product_types = {
        'bond': 'bonds/bonds.csv',
        'certificate': 'certificates/certificates.csv',
        'commodity': 'commodities/commodities.csv',
        'currency_cross': 'currency_crosses/currency_crosses.csv',
        'etf': 'etfs/etfs.csv',
        'fund': 'funds/funds.csv',
        'index': 'indices/indices.csv',
        'stock': 'stocks/stocks.csv'
    }

    product_type = unidecode.unidecode(product_type.lower().strip())

    if product_type not in product_types.keys():
        raise ValueError("")

    intervals = {
        '5mins': 60*5,
        '15mins': 60*15,
        '30mins': 60*30,
        '1hour': 60*60,
        '5hours': 60*60*5,
        'daily': 60*60*24,
        'weekly': 'week',
        'monthly': 'month'
    }

    if interval:
        if interval not in intervals.keys():
            raise ValueError("")
    else:
        interval = 'daily'

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', product_types[product_type]))
    if pkg_resources.resource_exists(resource_package, resource_path):
        data = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0115: data file not found or errored.")

    if data is None:
        raise IOError("ERR#0115: data file not found or errored.")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    if product_type not in ['bond', 'currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("")

            data = data[data['country'] == country]

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("")

    product_id = data.loc[(data[check].str.lower() == name).idxmax(), 'id']

    data = {
        'pairID': product_id,
        'period': intervals[interval],
        'viewType': 'normal'
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    return data


if __name__ == "__main__":
    print(technical_analysis(name='Cyprus 1Y', country=None, product_type='bond', interval='daily'))