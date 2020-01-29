#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd

import pkg_resources
import unidecode

import requests
from lxml.html import fromstring

from investpy.utils.user_agent import get_random
from investpy.utils.auxiliar import resource_to_data


def technical_indicators(name, country, product_type, interval='daily'):
    """
    This function ...
    """

    if not name:
        raise ValueError("ERR#0116: the parameter name must be specified and must be a string.")

    if not isinstance(name, str):
        raise ValueError("ERR#0116: the parameter name must be specified and must be a string.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0117: this parameter can just be None or a string, if required.")

    if not product_type:
        raise ValueError("ERR#0118: product_type value is mandatory and must be a string.")

    if not isinstance(product_type, str):
        raise ValueError("ERR#0118: product_type value is mandatory and must be a string.")

    if not interval:
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

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
        raise ValueError("ERR#0119: introduced product_type value does not exist. Available values are: " + ', '.join(product_types.keys()))

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
            raise ValueError("ERR#0120: introduced interval value does not exist. Available values are: " + ', '.join(product_types.keys()))
    else:
        interval = 'daily'

    data = resource_to_data(path_to_data=product_types[product_type])

    if product_type not in ['currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("ERR#0124: introduced country does not exist or is not available.")

            data = data[data['country'] == country]
        else:
            if product_type != 'commodity':
                raise ValueError("ERR#0123: country parameter is required with the introduced product_type.")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("ERR#0122: introduced name does not exist in the introduced country (if required).")

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


def moving_averages(name, country, product_type, interval='daily'):
    """
    This function ...
    """

    if not name:
        raise ValueError("ERR#0116: the parameter name must be specified and must be a string.")

    if not isinstance(name, str):
        raise ValueError("ERR#0116: the parameter name must be specified and must be a string.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0117: this parameter can just be None or a string, if required.")

    if not product_type:
        raise ValueError("ERR#0118: product_type value is mandatory and must be a string.")

    if not isinstance(product_type, str):
        raise ValueError("ERR#0118: product_type value is mandatory and must be a string.")

    if not interval:
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

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
        raise ValueError("ERR#0119: introduced product_type value does not exist. Available values are: " + ', '.join(product_types.keys()))

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
            raise ValueError("ERR#0120: introduced interval value does not exist. Available values are: " + ', '.join(product_types.keys()))
    else:
        interval = 'daily'

    data = resource_to_data(path_to_data=product_types[product_type])

    if product_type not in ['currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("ERR#0124: introduced country does not exist or is not available.")

            data = data[data['country'] == country]
        else:
            if product_type != 'commodity':
                raise ValueError("ERR#0123: country parameter is required with the introduced product_type.")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("ERR#0122: introduced name does not exist in the introduced country (if required).")

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
    table = root.xpath(".//table[contains(@class, 'movingAvgsTbl')]/tbody/tr")

    moving_avgs = list()

    for row in table:
        for value in row.xpath("td"):
            if value.get('class') is not None:
                if value.get('class').__contains__('symbol'):
                    ma_period = value.text_content().strip().replace('MA', '')
                    sma_signal = value.getnext().xpath("span")[0].text_content().strip().lower()
                    sma_value = float(value.getnext().text_content().lower().replace(sma_signal, '').strip())
                    value = value.getnext()
                    ema_signal = value.getnext().xpath(".//span")[0].text_content().strip().lower()
                    ema_value = float(value.getnext().text_content().lower().replace(ema_signal, '').strip())

                    moving_avgs.append({
                        'period': ma_period,
                        'sma_value': sma_value,
                        'sma_signal': sma_signal,
                        'ema_value': ema_value,
                        'ema_signal': ema_signal
                    })

    result = pd.DataFrame(moving_avgs)

    return result


def pivot_points(name, country, product_type, interval='daily'):
    """
    This function ...
    """

    if not name:
        raise ValueError("ERR#0116: the parameter name must be specified and must be a string.")

    if not isinstance(name, str):
        raise ValueError("ERR#0116: the parameter name must be specified and must be a string.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0117: this parameter can just be None or a string, if required.")

    if not product_type:
        raise ValueError("ERR#0118: product_type value is mandatory and must be a string.")

    if not isinstance(product_type, str):
        raise ValueError("ERR#0118: product_type value is mandatory and must be a string.")

    if not interval:
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

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
        raise ValueError("ERR#0119: introduced product_type value does not exist. Available values are: " + ', '.join(product_types.keys()))

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
            raise ValueError("ERR#0120: introduced interval value does not exist. Available values are: " + ', '.join(product_types.keys()))
    else:
        interval = 'daily'

    data = resource_to_data(path_to_data=product_types[product_type])

    if product_type not in ['currency_cross']:
        if country is not None:
            country = unidecode.unidecode(country.lower().strip())

            if country not in data['country'].tolist():
                raise ValueError("ERR#0124: introduced country does not exist or is not available.")

            data = data[data['country'] == country]
        else:
            if product_type != 'commodity':
                raise ValueError("ERR#0123: country parameter is required with the introduced product_type.")

    if product_type == 'stock':
        check = 'symbol'
    else:
        check = 'name'

    name = unidecode.unidecode(name.lower().strip())

    if name not in [unidecode.unidecode(value.lower()) for value in data[check].tolist()]:
        raise RuntimeError("ERR#0122: introduced name does not exist in the introduced country (if required).")

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
