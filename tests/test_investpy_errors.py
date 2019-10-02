#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import pytest

import investpy

from investpy.equities import retrieve_equities, retrieve_equity_countries
from investpy.funds import retrieve_funds, retrieve_fund_countries
from investpy.etfs import retrieve_etfs
from investpy.indices import retrieve_indices, retrieve_index_countries, retrieve_global_indices_countries
from investpy.currency_crosses import retrieve_currency_crosses

from investpy.user_agent import get_random, clear_file, delete_file


def test_equities_errors():
    """
    This function raises errors on equity retrieval functions
    """

    try:
        retrieve_equities(test_mode=None)
    except:
        pass

    try:
        retrieve_equity_countries(test_mode=None)
    except:
        pass

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
            investpy.get_equities(country=param['country'])
        except:
            pass

        try:
            investpy.get_equities_list(country=param['country'])
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
            investpy.get_equities_dict(country=param['country'],
                                       columns=param['columns'],
                                       as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'equity': 'Euripo Properties Socimi',
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': None,
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'greece',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'debug': True
        },
        {
            'equity': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_recent_data(equity=param['equity'],
                                     country=param['country'],
                                     as_json=param['as_json'],
                                     order=param['order'],
                                     debug=param['debug'])
        except:
            pass

    params = [
        {
            'equity': 'Euripo Properties Socimi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': None,
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'greece',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/1999',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/1950',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1999',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_historical_data(equity=param['equity'],
                                         country=param['country'],
                                         from_date=param['from_date'],
                                         to_date=param['to_date'],
                                         as_json=param['as_json'],
                                         order=param['order'],
                                         debug=param['debug'])
        except:
            pass

    params = [
        {
            'equity': None,
            'country': 'spain',
            'language': 'spanish'
        },
        {
            'equity': 'bbva',
            'country': None,
            'language': 'spanish'
        },
        {
            'equity': 'bbva',
            'country': 'greece',
            'language': 'spanish'
        },
        {
            'equity': 'bbva',
            'country': 'spain',
            'language': 'error'
        },
        {
            'equity': 'error',
            'country': 'spain',
            'language': 'spanish'
        },
        {
            'equity': ['error'],
            'country': 'spain',
            'language': 'spanish'
        },
    ]

    for param in params:
        try:
            investpy.get_equity_company_profile(equity=param['equity'],
                                                country=param['country'],
                                                language=param['language'])
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
            investpy.search_equities(by=param['by'], value=param['value'])
        except:
            pass


def test_funds_errors():
    """
    This function raises errors on fund retrieval functions
    """

    try:
        retrieve_funds(test_mode=None)
    except:
        pass

    try:
        retrieve_fund_countries(test_mode=None)
    except:
        pass

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
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'germany',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'debug': True
        },
        {
            'fund': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_fund_recent_data(fund=param['fund'],
                                          country=param['country'],
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          debug=param['debug'])
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
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'germany',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': ['error'],
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': 'error'
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
                                              debug=param['debug'])
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

    try:
        retrieve_etfs(test_mode=None)
    except:
        pass

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
            'debug': True
        },
        {
            'etf': ['error'],
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'netherlands',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'debug': True
        },
        {
            'etf': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_etf_recent_data(etf=param['etf'],
                                         country=param['country'],
                                         as_json=param['as_json'],
                                         order=param['order'],
                                         debug=param['debug'])
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
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'netherlands',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
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
                                             debug=param['debug'])
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

    try:
        retrieve_indices(test_mode=None)
    except:
        pass

    try:
        retrieve_index_countries(test_mode=None)
    except:
        pass

    try:
        retrieve_global_indices_countries(test_mode=None)
    except:
        pass

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
            'debug': True
        },
        {
            'index': ['error'],
            'country': 'spain',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': None,
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'netherlands',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': ['error'],
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True,
            'order': 'error',
            'debug': True
        },
        {
            'index': 'error',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': ['error'],
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_index_recent_data(index=param['index'],
                                           country=param['country'],
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           debug=param['debug'])
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
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'netherlands',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'error',
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': ['error'],
            'country': 'spain',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'from_date': '01/01/2019',
            'to_date': '01/03/2019',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
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
                                               debug=param['debug'])
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

    try:
        retrieve_currency_crosses(test_mode=None)
    except:
        pass

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
            'debug': False
        },
        {
            'currency_cross': ['error'],
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': 'error',
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'error',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'ascending',
            'debug': 'error'
        },
        {
            'currency_cross': 'error/error',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
    ]

    for param in params:
        try:
            investpy.get_currency_cross_recent_data(currency_cross=param['currency_cross'],
                                                    as_json=param['as_json'],
                                                    order=param['order'],
                                                    debug=param['debug'])
        except:
            pass

    params = [
        {
            'currency_cross': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': ['error'],
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2017',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': 'error'
        },
        {
            'currency_cross': 'error/error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': False
        },
    ]

    for param in params:
        try:
            investpy.get_currency_cross_historical_data(currency_cross=param['currency_cross'],
                                                        from_date=param['from_date'],
                                                        to_date=param['to_date'],
                                                        as_json=param['as_json'],
                                                        order=param['order'],
                                                        debug=param['debug'])
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
    test_equities_errors()
    test_funds_errors()
    test_etfs_errors()
    test_indices_errors()
    test_currency_crosses_errors()
    test_user_agent_errors()
