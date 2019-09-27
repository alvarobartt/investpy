#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import pytest

import investpy

from investpy.equities import retrieve_equities, retrieve_equity_countries
from investpy.funds import retrieve_funds, retrieve_fund_countries
from investpy.etfs import retrieve_etfs
from investpy.indices import retrieve_indices, retrieve_index_countries
from investpy.currency_crosses import retrieve_currency_crosses


def test_investpy():
    """
    This function checks that both the investpy's author and version are the correct ones.
    """

    print(investpy.__author__, investpy.__version__)


def test_investpy_equities():
    """
    This function checks that equity data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'country': 'spain',
        },
        {
            'country': None,
        },
    ]

    for param in params:
        investpy.get_equities(country=param['country'])
        investpy.get_equities_list(country=param['country'])

    params = [
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_equities_dict(country=param['country'],
                                   columns=param['columns'],
                                   as_json=param['as_json'])

    investpy.get_equity_countries()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'as_json': True,
            'order': 'descending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'descending',
            'debug': False
        },
    ]

    for param in params:
        investpy.get_recent_data(equity='enagás',
                                 country='spain',
                                 as_json=param['as_json'],
                                 order=param['order'],
                                 debug=param['debug'])

        investpy.get_historical_data(equity='enagás',
                                     country='spain',
                                     from_date='01/01/1990',
                                     to_date='01/01/2019',
                                     as_json=param['as_json'],
                                     order=param['order'],
                                     debug=param['debug'])

    for value in ['spanish', 'english']:
        investpy.get_equity_company_profile(equity='enagás',
                                            country='spain',
                                            language=value)

    investpy.search_equities(by='name', value='bbva')

    retrieve_equities(test_mode=True)
    retrieve_equity_countries(test_mode=True)


def test_investpy_funds():
    """
    This function checks that fund data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'country': 'spain',
        },
        {
            'country': None,
        },
    ]

    for param in params:
        investpy.get_funds(country=param['country'])
        investpy.get_funds_list(country=param['country'])

    params = [
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_funds_dict(country=param['country'],
                                columns=param['columns'],
                                as_json=param['as_json'])

    investpy.get_fund_countries()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'as_json': True,
            'order': 'descending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'descending',
            'debug': False
        },
    ]

    for param in params:
        investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp',
                                      country='spain',
                                      as_json=param['as_json'],
                                      order=param['order'],
                                      debug=param['debug'])

        investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp',
                                          country='spain',
                                          from_date='01/01/2010',
                                          to_date='01/01/2019',
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          debug=param['debug'])

    params = [
        {
            'fund': 'bbva multiactivo conservador pp',
            'country': 'spain',
            'as_json': True,
        },
        {
            'fund': 'bbva multiactivo conservador pp',
            'country': 'spain',
            'as_json': False,
        },
    ]

    for param in params:
        investpy.get_fund_information(fund=param['fund'],
                                      country=param['country'],
                                      as_json=param['as_json'])

    investpy.search_funds(by='name', value='bbva')

    retrieve_funds(test_mode=True)
    retrieve_fund_countries(test_mode=True)


def test_investpy_etfs():
    """
    This function checks that etf data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'country': 'spain',
        },
        {
            'country': None,
        },
    ]

    for param in params:
        investpy.get_etfs(country=param['country'])
        investpy.get_etfs_list(country=param['country'])

    params = [
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_etfs_dict(country=param['country'],
                               columns=param['columns'],
                               as_json=param['as_json'])

    investpy.get_etf_countries()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'as_json': True,
            'order': 'descending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'descending',
            'debug': False
        },
    ]

    for param in params:
        investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                     country='spain',
                                     as_json=param['as_json'],
                                     order=param['order'],
                                     debug=param['debug'])

        investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50',
                                         country='spain',
                                         from_date='01/01/2010',
                                         to_date='01/01/2019',
                                         as_json=param['as_json'],
                                         order=param['order'],
                                         debug=param['debug'])

    params = [
        {
            'country': 'france',
            'as_json': True,
        },
        {
            'country': 'france',
            'as_json': False,
        },
    ]

    for param in params:
        investpy.get_etfs_overview(country=param['country'], as_json=param['as_json'])

    investpy.search_etfs(by='name', value='bbva')

    retrieve_etfs(test_mode=True)


def test_investpy_indices():
    """
    This function checks that index data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'country': 'spain',
        },
        {
            'country': None,
        },
    ]

    for param in params:
        investpy.get_indices(country=param['country'])
        investpy.get_indices_list(country=param['country'])

    params = [
        {
            'country': None,
            'columns': ['name', 'currency'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['name', 'currency'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['name', 'currency'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['name', 'currency'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_indices_dict(country=param['country'],
                                  columns=param['columns'],
                                  as_json=param['as_json'])

    investpy.get_index_countries()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'as_json': True,
            'order': 'descending',
            'debug': False
        },
        {
            'as_json': False,
            'order': 'descending',
            'debug': False
        },
    ]

    for param in params:
        investpy.get_index_recent_data(index='ibex 35',
                                       country='spain',
                                       as_json=param['as_json'],
                                       order=param['order'],
                                       debug=param['debug'])

        investpy.get_index_historical_data(index='ibex 35',
                                           country='spain',
                                           from_date='01/01/2018',
                                           to_date='01/01/2019',
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           debug=param['debug'])

    investpy.search_indices(by='name', value='ibex')

    retrieve_indices(test_mode=True)
    retrieve_index_countries(test_mode=True)


# def test_investpy_currencies():
#     retrieve_currency_crosses()
#     investpy.get_currency_crosses()
#     investpy.get_currency_crosses_list()
#     investpy.get_currency_crosses_dict()
#
#     params = [
#         {
#             'currency_cross': 'EUR/USD',
#             'from_date': '08/07/2019',
#             'to_date': '08/08/2019',
#             'as_json': True,
#         },
#         {
#             'currency_cross': 'EUR/USD',
#             'from_date': '08/07/2019',
#             'to_date': '08/08/2019',
#             'as_json': False,
#         }]
#
#     for param in params:
#         investpy.get_currency_cross_recent_data(currency_cross=param['currency_cross'], as_json=param['as_json'])
#         investpy.get_currency_cross_historical_data(currency_cross=param['currency_cross'],
#                                                     from_date=param['from_date'],
#                                                     to_date=param['to_date'],
#                                                     as_json=param['as_json'])


if __name__ == '__main__':
    test_investpy()
    test_investpy_equities()
    test_investpy_funds()
    test_investpy_etfs()
    test_investpy_indices()
    # test_investpy_currencies()
