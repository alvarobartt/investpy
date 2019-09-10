#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import pytest

import investpy

from investpy.user_agent import get_random, clear_file, delete_file


def test_equity_errors():
    """
    This function raises errors on equity functions
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
            investpy.get_equities_list(country=param['country'])
        except:
            pass

        try:
            investpy.get_equities(country=param['country'])
        except:
            pass

    params = [
        {
            'country': None,
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


def test_fund_errors():
    """
    This function raises errors on fund functions
    """

    params = [
        {
            'columns': None,
            'as_json': 'error'
        },
        {
            'columns': 0,
            'as_json': True
        },
        {
            'columns': ['error'],
            'as_json': False
        },
    ]

    for param in params:
        try:
            investpy.get_funds_dict(columns=param['columns'],
                                    as_json=param['as_json'])
        except:
            pass

    params = [
        {
            'fund': None,
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'as_json': True,
            'order': 'error',
            'debug': True
        },
        {
            'fund': 'error',
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': ['error'],
            'as_json': True,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'as_json': True,
            'order': 'ascending',
            'debug': 'error'
        },
    ]

    for param in params:
        try:
            investpy.get_fund_recent_data(fund=param['fund'],
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          debug=param['debug'])
        except:
            pass

    params = [
        {
            'fund': None,
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': 'error',
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'error',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': 'error',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': '01/01/2019',
            'to_date': 'error',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'error',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': ['error'],
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': '01/01/1998',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': '01/01/2019',
            'to_date': '01/01/1998',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
            'from_date': '01/01/1900',
            'to_date': '01/01/1950',
            'as_json': False,
            'order': 'ascending',
            'debug': True
        },
        {
            'fund': 'quality inversion conservadora fi',
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
            'as_json': False
        },
        {
            'fund': 'quality inversion conservadora fi',
            'as_json': 'error'
        },
        {
            'fund': 'error',
            'as_json': True
        },
        {
            'fund': ['error'],
            'as_json': True
        },
    ]

    for param in params:
        try:
            investpy.get_fund_information(fund=param['fund'],
                                          as_json=param['as_json'])
        except:
            pass


def test_etf_errors():
    """
    This function raises errors on etf functions
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
            investpy.get_etfs_list(country=param['country'])
        except:
            pass

        try:
            investpy.get_etfs(country=param['country'])
        except:
            pass

    params = [
        {
            'country': None,
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
    test_equity_errors()
    test_fund_errors()
    test_etf_errors()
    test_user_agent_errors()
