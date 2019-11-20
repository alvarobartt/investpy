#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import investpy

from investpy.utils.user_agent import get_random, clear_file, delete_file


def test_stocks_errors():
    """
    This function raises errors on stock retrieval functions
    """

    params = [
        {
            'country': ['error']
        },
        {
            'country': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_stocks(country=param['country'])
        except:
            pass

        try:
            investpy.get_stocks_list(country=param['country'])
        except:
            pass

    params = [
        {
            'country': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': 'error'
        },
        {
            'country': 'spain',
            'columns': 0,
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_stocks_dict(country=param['country'],
                                     columns=param['columns'],
                                     as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'stock': 'FERR',
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': None,
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'greece',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'stock': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': None,
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error'],
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error',
        },
    ]

    for param in params:
        try:
            investpy.get_stock_recent_data(stock=param['stock'],
                                           country=param['country'],
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           interval=param['interval'])
        except:
            pass

    params = [
        {
            'stock': 'FERR',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': None,
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'greece',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/1999',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/1950',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1999',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': None
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_stock_historical_data(stock=param['stock'],
                                               country=param['country'],
                                               from_date=param['from_date'],
                                               to_date=param['to_date'],
                                               as_json=param['as_json'],
                                               order=param['order'],
                                               interval=param['interval'])
        except:
            pass

    params = [
        {
            'stock': None,
            'country': 'spain',
            'language': 'spanish'
        },
        {
            'stock': 'BBVA',
            'country': None,
            'language': 'spanish'
        },
        {
            'stock': 'BBVA',
            'country': 'greece',
            'language': 'spanish'
        },
        {
            'stock': 'BBVA',
            'country': 'spain',
            'language': 'error'
        },
        {
            'stock': 'error',
            'country': 'spain',
            'language': 'spanish'
        },
        {
            'stock': ['error'],
            'country': 'spain',
            'language': 'spanish'
        },
    ]

    for param in params:
        try:
            investpy.get_stock_company_profile(stock=param['stock'],
                                               country=param['country'],
                                               language=param['language'])
        except:
            pass

    params = [
        {
            'stock': None,
            'country': 'spain',
        },
        {
            'stock': ['error'],
            'country': 'spain',
        },
        {
            'stock': 'bbva',
            'country': ['error'],
        },
        {
            'stock': 'bbva',
            'country': 'error',
        },
        {
            'stock': 'error',
            'country': 'spain',
        },
        {
            'stock': 'ALUA',
            'country': 'argentina',
        },
    ]

    for param in params:
        try:
            investpy.get_stock_dividends(stock=param['stock'], country=param['country'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'BBVA',
        },
        {
            'by': ['error'],
            'value': 'BBVA',
        },
        {
            'by': 'error',
            'value': 'BBVA',
        },
        {
            'by': 'name',
            'value': None,
        },
        {
            'by': 'name',
            'value': ['error'],
        },
        {
            'by': 'isin',
            'value': 'BBVA',
        },
    ]

    for param in params:
        try:
            investpy.search_stocks(by=param['by'], value=param['value'])
        except:
            pass


def test_funds_errors():
    """
    This function raises errors on fund retrieval functions
    """

    params = [
        {
            'country': ['error'],
        },
    ]

    for param in params:
        try:
            investpy.get_funds(country=param['country'])
        except:
            pass

        try:
            investpy.get_funds_list(country=param['country'])
        except:
            pass

    params = [
        {
            'country': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'country': None,
            'columns': None,
            'as_json': 'error'
        },
        {
            'country': None,
            'columns': 0,
            'as_json': True
        },
        {
            'country': None,
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_funds_dict(country=param['country'],
                                    columns=param['columns'],
                                    as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'fund': None,
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'germany',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'fund': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': None
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_fund_recent_data(fund=param['fund'],
                                          country=param['country'],
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          interval=param['interval'])
        except:
            pass

    params = [
        {
            'fund': None,
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'germany',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': ['error'],
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': None
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_fund_historical_data(fund=param['fund'],
                                              country=param['country'],
                                              from_date=param['from_date'],
                                              to_date=param['to_date'],
                                              as_json=param['as_json'],
                                              order=param['order'],
                                              interval=param['interval'])
        except:
            pass

    params = [
        {
            'fund': None,
            'country': 'spain',
            'as_json': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': None,
            'as_json': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': ['error'],
            'as_json': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'error',
            'as_json': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'germany',
            'as_json': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': 'error'
        },
        {
            'fund': 'error',
            'country': 'spain',
            'as_json': True
        },
        {
            'fund': ['error'],
            'country': 'spain',
            'as_json': True
        },
    ]

    for param in params:
        try:
            investpy.get_fund_information(fund=param['fund'],
                                          country=param['country'],
                                          as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'bbva',
        },
        {
            'by': ['error'],
            'value': 'bbva',
        },
        {
            'by': 'error',
            'value': 'bbva',
        },
        {
            'by': 'name',
            'value': None,
        },
        {
            'by': 'name',
            'value': ['error'],
        },
        {
            'by': 'isin',
            'value': 'error',
        },
    ]

    for param in params:
        try:
            investpy.search_funds(by=param['by'], value=param['value'])
        except:
            pass


def test_etfs_errors():
    """
    This function raises errors on etf retrieval functions
    """

    params = [
        {
            'country': ['error']
        },
        {
            'country': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_etfs(country=param['country'])
        except:
            pass

        try:
            investpy.get_etfs_list(country=param['country'])
        except:
            pass

    params = [
        {
            'country': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': 'error'
        },
        {
            'country': 'spain',
            'columns': 0,
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_etfs_dict(country=param['country'],
                                   columns=param['columns'],
                                   as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'etf': None,
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': ['error'],
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'netherlands',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'etf': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': None
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_etf_recent_data(etf=param['etf'],
                                         country=param['country'],
                                         as_json=param['as_json'],
                                         order=param['order'],
                                         interval=param['interval'])
        except:
            pass

    params = [
        {
            'etf': None,
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'netherlands',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'interval': None
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_etf_historical_data(etf=param['etf'],
                                             country=param['country'],
                                             from_date=param['from_date'],
                                             to_date=param['to_date'],
                                             as_json=param['as_json'],
                                             order=param['order'],
                                             interval=param['interval'])
        except:
            pass

    params = [
        {
            'country': 'error',
            'as_json': False,
        },
        {
            'country': None,
            'as_json': False,
        },
        {
            'country': ['error'],
            'as_json': False,
        },
        {
            'country': 'spain',
            'as_json': None,
        },
        {
            'country': 'spain',
            'as_json': ['error'],
        },
    ]

    for param in params:
        try:
            investpy.get_etfs_overview(country=param['country'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'bbva',
        },
        {
            'by': ['error'],
            'value': 'bbva',
        },
        {
            'by': 'error',
            'value': 'bbva',
        },
        {
            'by': 'name',
            'value': None,
        },
        {
            'by': 'name',
            'value': ['error'],
        },
        {
            'by': 'isin',
            'value': 'error',
        },
    ]

    for param in params:
        try:
            investpy.search_etfs(by=param['by'], value=param['value'])
        except:
            pass


def test_indices_errors():
    """
    This function raises errors on index retrieval functions
    """

    params = [
        {
            'country': ['error']
        },
        {
            'country': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_indices(country=param['country'])
        except:
            pass

        try:
            investpy.get_indices_list(country=param['country'])
        except:
            pass

    params = [
        {
            'country': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': 'error'
        },
        {
            'country': 'spain',
            'columns': 0,
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_indices_dict(country=param['country'],
                                      columns=param['columns'],
                                      as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'index': None,
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': ['error'],
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'netherlands',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'index': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': None
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_index_recent_data(index=param['index'],
                                           country=param['country'],
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           interval=param['interval'])
        except:
            pass

    params = [
        {
            'index': None,
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'netherlands',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'interval': None
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_index_historical_data(index=param['index'],
                                               country=param['country'],
                                               from_date=param['from_date'],
                                               to_date=param['to_date'],
                                               as_json=param['as_json'],
                                               order=param['order'],
                                               interval=param['interval'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'ibex',
        },
        {
            'by': ['error'],
            'value': 'ibex',
        },
        {
            'by': 'error',
            'value': 'ibex',
        },
        {
            'by': 'name',
            'value': None,
        },
        {
            'by': 'name',
            'value': ['error'],
        },
        {
            'by': 'name',
            'value': 'error',
        },
    ]

    for param in params:
        try:
            investpy.search_indices(by=param['by'], value=param['value'])
        except:
            pass


def test_currency_crosses_errors():
    """
    This function raises errors on currency cross retrieval functions
    """

    params = [
        {
            'base': ['error'],
            'second': None
        },
        {
            'base': None,
            'second': ['error']
        },
        {
            'base': 'error',
            'second': None
        },
        {
            'base': 'EUR',
            'second': 'error'
        },
        {
            'base': None,
            'second': 'error'
        },
        {
            'base': 'EUR',
            'second': 'EUR',
        }
    ]

    for param in params:
        try:
            investpy.get_currency_crosses(base=param['base'],
                                          second=param['second'])
        except:
            pass

        try:
            investpy.get_currency_crosses_list(base=param['base'],
                                               second=param['second'])
        except:
            pass

    params = [
        {
            'base': ['error'],
            'second': None,
            'columns': None,
            'as_json': False
        },
        {
            'base': None,
            'second': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'base': None,
            'second': None,
            'columns': None,
            'as_json': 'error'
        },
        {
            'base': None,
            'second': None,
            'columns': 'error',
            'as_json': False
        },
        {
            'base': None,
            'second': None,
            'columns': ['error'],
            'as_json': False
        },
        {
            'base': 'error',
            'second': None,
            'columns': None,
            'as_json': False
        },
        {
            'base': 'EUR',
            'second': 'error',
            'columns': None,
            'as_json': False
        },
        {
            'base': None,
            'second': 'error',
            'columns': None,
            'as_json': False
        },
        {
            'base': 'EUR',
            'second': 'Eur',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_currency_crosses_dict(base=param['base'],
                                               second=param['second'],
                                               columns=param['columns'],
                                               as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'currency_cross': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'error/error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'ascending',
            'interval': None
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_currency_cross_recent_data(currency_cross=param['currency_cross'],
                                                    as_json=param['as_json'],
                                                    order=param['order'],
                                                    interval=param['interval'])
        except:
            pass

    params = [
        {
            'currency_cross': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2017',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'error/error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': None
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_currency_cross_historical_data(currency_cross=param['currency_cross'],
                                                        from_date=param['from_date'],
                                                        to_date=param['to_date'],
                                                        as_json=param['as_json'],
                                                        order=param['order'],
                                                        interval=param['interval'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'EUR',
        },
        {
            'by': ['error'],
            'value': 'EUR',
        },
        {
            'by': 'error',
            'value': 'EUR',
        },
        {
            'by': 'base',
            'value': None,
        },
        {
            'by': 'base',
            'value': ['error'],
        },
        {
            'by': 'base',
            'value': 'error',
        },
    ]

    for param in params:
        try:
            investpy.search_currency_crosses(by=param['by'], value=param['value'])
        except:
            pass


def test_bonds_errors():
    """
    This function raises errors on bond retrieval functions
    """

    params = [
        {
            'country': ['error']
        },
        {
            'country': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_bonds(country=param['country'])
        except:
            pass

        try:
            investpy.get_bonds_list(country=param['country'])
        except:
            pass

    params = [
        {
            'country': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': 'error'
        },
        {
            'country': 'spain',
            'columns': 0,
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_bonds_dict(country=param['country'],
                                    columns=param['columns'],
                                    as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'bond': None,
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'as_json': True,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'bond': 'error',
            'country': 'argentina',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': ['error'],
            'country': 'argentina',
            'as_json': True,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'as_json': True,
            'order': 'ascending',
            'interval': None
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'as_json': True,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'as_json': True,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_bond_recent_data(bond=param['bond'],
                                          country=param['country'],
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          interval=param['interval'])
        except:
            pass

    params = [
        {
            'bond': 'Argentina 3Y',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'stock': None,
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/1999',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/1950',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2019',
            'to_date': '01/01/1999',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily'
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': None
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error']
        },
        {
            'bond': 'Argentina 3Y',
            'country': 'argentina',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_bond_historical_data(bond=param['bond'],
                                              country=param['country'],
                                              from_date=param['from_date'],
                                              to_date=param['to_date'],
                                              as_json=param['as_json'],
                                              order=param['order'],
                                              interval=param['interval'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'Argentina',
        },
        {
            'by': ['error'],
            'value': 'Argentina',
        },
        {
            'by': 'error',
            'value': 'Argentina',
        },
        {
            'by': 'name',
            'value': None,
        },
        {
            'by': 'name',
            'value': ['error'],
        },
        {
            'by': 'name',
            'value': 'error',
        },
    ]

    for param in params:
        try:
            investpy.search_bonds(by=param['by'], value=param['value'])
        except:
            pass


def test_commodities_errors():
    """
    This function raises errors on commodity retrieval functions
    """

    params = [
        {
            'group': ['error']
        },
        {
            'group': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_commodities(group=param['group'])
        except:
            pass

        try:
            investpy.get_commodities_list(group=param['group'])
        except:
            pass

    params = [
        {
            'group': ['error'],
            'columns': None,
            'as_json': False
        },
        {
            'group': 'metals',
            'columns': None,
            'as_json': 'error'
        },
        {
            'group': 'metals',
            'columns': 0,
            'as_json': True
        },
        {
            'group': 'metals',
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_commodities_dict(group=param['group'],
                                          columns=param['columns'],
                                          as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'commodity': None,
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': ['error'],
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily',
        },
        {
            'commodity': 'chocolate',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'as_json': False,
            'order': 'ascending',
            'interval': None,
        },
        {
            'commodity': 'gold',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error'],
        },
        {
            'commodity': 'gold',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error',
        },
    ]

    for param in params:
        try:
            investpy.get_commodity_recent_data(commodity=param['commodity'],
                                               as_json=param['as_json'],
                                               order=param['order'],
                                               interval=param['interval'])
        except:
            pass

    params = [
        {
            'commodity': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'interval': 'Daily',
        },
        {
            'commodity': 'chocolate',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2018',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/1999',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/1950',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2019',
            'to_date': '01/01/1999',
            'as_json': False,
            'order': 'ascending',
            'interval': 'Daily',
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': None,
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': ['error'],
        },
        {
            'commodity': 'gold',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'interval': 'error',
        },
    ]

    for param in params:
        try:
            investpy.get_commodity_historical_data(commodity=param['commodity'],
                                                   from_date=param['from_date'],
                                                   to_date=param['to_date'],
                                                   as_json=param['as_json'],
                                                   order=param['order'],
                                                   interval=param['interval'])
        except:
            pass

    params = [
        {
            'by': None,
            'value': 'silver',
        },
        {
            'by': ['error'],
            'value': 'silver',
        },
        {
            'by': 'error',
            'value': 'silver',
        },
        {
            'by': 'name',
            'value': None,
        },
        {
            'by': 'name',
            'value': ['error'],
        },
        {
            'by': 'name',
            'value': 'error',
        },
    ]

    for param in params:
        try:
            investpy.search_commodities(by=param['by'], value=param['value'])
        except:
            pass
    

def test_search_errors():
    """
    This function raises errors on search functions
    """

    params = [
        {
            'text': None
        },
        {
            'text': ['error']
        },
        {
            'text': 'error'
        },
    ]

    for param in params:
        try:
            investpy.search_text(text=param['text'])
        except:
            pass


def test_user_agent_errors():
    """
    This function raises errors on user_agent functions
    """

    clear_file()
    try:
        get_random()
    except:
        pass

    delete_file()
    try:
        get_random()
    except:
        pass


if __name__ == '__main__':
    test_stocks_errors()
    test_funds_errors()
    test_etfs_errors()
    test_indices_errors()
    test_currency_crosses_errors()
    test_bonds_errors()
    test_commodities_errors()
    test_search_errors()
    test_user_agent_errors()
