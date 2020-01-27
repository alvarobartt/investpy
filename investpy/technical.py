#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd

import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy.utils.user_agent import get_random
from investpy.utils.auxiliar import resource_to_data


def technical_indicators(name, country, product_type, interval):
    """
    This function ...
    """

    product_types = {
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

    data = resource_to_data(path_to_data=product_types[product_type])

    if product_type not in ['currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("")

            data = data[data['country'] == country]
        else:
            if product_type != 'commodity':
                raise ValueError("")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("")

    product_id = data.loc[(data[check].str.lower() == name).idxmax(), 'id']

    data_values = {
        'pairID': product_id,
        'period': intervals[interval],
        'viewType': 'normal'
    }

    headers = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    table = root.xpath(".//table[contains(@class, 'technicalIndicatorsTbl')]/tbody/tr")

    tech_indicators = list()

    for row in table:
        for value in row.xpath("td"):
            if value.get('class').__contains__('symbol'):
                tech_ind = value.text_content().strip()
                tech_val = float(value.getnext().text_content().strip())
                tech_sig = value.getnext().getnext().text_content().strip().lower()
                
                tech_indicators.append({
                    'technical_indicator': tech_ind,
                    'value': tech_val,
                    'signal': tech_sig 
                })

    result = pd.DataFrame(tech_indicators)

    return result


def moving_averages(name, country, product_type, interval):
    """
    This function ...
    """

    product_types = {
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

    data = resource_to_data(path_to_data=product_types[product_type])

    if product_type not in ['currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("")

            data = data[data['country'] == country]
        else:
            if product_type != 'commodity':
                raise ValueError("")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("")

    product_id = data.loc[(data[check].str.lower() == name).idxmax(), 'id']

    data_values = {
        'pairID': product_id,
        'period': intervals[interval],
        'viewType': 'normal'
    }

    headers = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    table = root.xpath(".//table[contains(@class, 'technicalIndicatorsTbl')]/tbody/tr")

    tech_indicators = list()

    for row in table:
        for value in row.xpath("td"):
            if value.get('class').__contains__('symbol'):
                tech_ind = value.text_content().strip()
                tech_val = float(value.getnext().text_content().strip())
                tech_sig = value.getnext().getnext().text_content().strip().lower()
                
                tech_indicators.append({
                    'technical_indicator': tech_ind,
                    'value': tech_val,
                    'signal': tech_sig 
                })

    result = pd.DataFrame(tech_indicators)

    return result


def pivot_points(name, country, product_type, interval):
    """
    This function ...
    """

    product_types = {
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

    data = resource_to_data(path_to_data=product_types[product_type])

    if product_type not in ['currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("")

            data = data[data['country'] == country]
        else:
            if product_type != 'commodity':
                raise ValueError("")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("")

    product_id = data.loc[(data[check].str.lower() == name).idxmax(), 'id']

    data_values = {
        'pairID': product_id,
        'period': intervals[interval],
        'viewType': 'normal'
    }

    headers = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    header = root.xpath(".//table[contains(@class, 'crossRatesTbl')]/thead/tr/th")

    values = dict()

    for index, column in enumerate(header):
        values.update({index: column.text_content().strip().lower().replace(' ', '_')})

    table = root.xpath(".//table[contains(@class, 'crossRatesTbl')]/tbody/tr")

    results = list()

    for row in table:
        result = dict()
        elements = row.xpath("td")

        for key, value in values.items():
            if value != 'name':
                val = elements[key].text_content().strip()
                try:
                    result.update({value: float(val)})
                except:
                    result.update({value: None})
            else:
                result.update({value: elements[key].text_content().strip()})
        
        results.append(result)

    result = pd.DataFrame(results)

    return result
