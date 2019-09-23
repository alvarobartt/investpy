#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import pytest

import investpy

from investpy.equities import retrieve_equities, retrieve_equity_countries
from investpy.funds import retrieve_funds, retrieve_fund_countries
from investpy.etfs import retrieve_etfs


def test_investpy():
    """
    This function checks that main functions of investpy work properly.
    """

    print(investpy.__author__, investpy.__version__)

    for value in ['spain', None]:
        investpy.get_equities(country=value)
        investpy.get_equities_list(country=value)

    params = [
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
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
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
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
            'as_json': True,
            'order': 'ascending',
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
            'country': 'spain',
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
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_funds_dict(country=param['country'],
                                columns=param['columns'],
                                as_json=param['as_json'])

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

    params = [
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
            'as_json': True,
            'order': 'ascending',
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

    investpy.get_fund_countries()

    investpy.get_funds()

    investpy.search_funds(by='name', value='bbva')

    retrieve_funds(test_mode=True)
    retrieve_fund_countries(test_mode=True)

    investpy.get_etf_countries()

    for value in ['spain', None]:
        investpy.get_etfs(country=value)
        investpy.get_etfs_list(country=value)

    params = [
        {
            'country': None,
            'columns': ['id', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
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
            'columns': None,
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['id', 'name'],
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_etfs_dict(country=param['country'],
                               columns=param['columns'],
                               as_json=param['as_json'])

    params = [
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
            'as_json': True,
            'order': 'ascending',
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
            'country': 'usa',
            'as_json': False,
        },
    ]

    for param in params:
        investpy.get_etfs_overview(country=param['country'], as_json=param['as_json'])

    investpy.search_etfs(by='name', value='bbva')

    retrieve_etfs(test_mode=True)


if __name__ == '__main__':
    test_investpy()
