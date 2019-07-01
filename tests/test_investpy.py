#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import pytest

import investpy

from investpy.equities import retrieve_equities
from investpy.funds import retrieve_funds
from investpy.etfs import retrieve_etfs


def test_investpy():
    """
    This function checks that main functions of investpy work properly.
    """

    investpy.get_equities()
    investpy.get_equities_list()

    params = [
        {'as_json': False, 'order': 'ascending'},
        {'as_json': True, 'order': 'descending'},
        {'as_json': True, 'order': 'ascending'},
        {'as_json': False, 'order': 'descending'},
    ]

    for param in params:
        investpy.get_recent_data(equity='enagás', as_json=param['as_json'], order=param['order'])
        investpy.get_historical_data(equity='enagás', start='01/01/1990', end='01/01/2019', as_json=param['as_json'], order=param['order'])

    for value in ['spanish', 'english']:
        investpy.get_equity_company_profile(equity='enagás', language=value)

    retrieve_equities()

    investpy.get_funds()
    investpy.get_funds_list()

    for value in [True, False]:
        investpy.get_funds_dict(columns=['id', 'name'], as_json=value)
        investpy.get_fund_information(fund='bbva multiactivo conservador pp', as_json=value)

    params = [
        {'as_json': False, 'order': 'ascending'},
        {'as_json': True, 'order': 'descending'},
        {'as_json': True, 'order': 'ascending'},
        {'as_json': False, 'order': 'descending'},
    ]

    for param in params:
        investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp', as_json=param['as_json'], order=param['order'])
        investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', start='01/01/2010', end='01/01/2019', as_json=param['as_json'], order=param['order'])

    investpy.get_funds()

    retrieve_funds()

    investpy.get_etfs()
    investpy.get_etf_countries()

    for value in ['spain', None]:
        investpy.get_etf_df(country=value)
        investpy.get_etf_list(country=value)

    params = [
        {'country': None, 'columns': ['id', 'name'], 'as_json': False},
        {'country': None, 'columns': ['id', 'name'], 'as_json': True},
        {'country': 'spain', 'columns': None, 'as_json': False},
        {'country': 'spain', 'columns': ['id', 'name'], 'as_json': True},
    ]

    for param in params:
        investpy.get_etf_dict(country=param['country'], columns=param['columns'], as_json=param['as_json'])

    params = [
        {'as_json': False, 'order': 'ascending'},
        {'as_json': True, 'order': 'descending'},
        {'as_json': True, 'order': 'ascending'},
        {'as_json': False, 'order': 'descending'},
    ]

    for param in params:
        investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50', as_json=param['as_json'], order=param['order'])
        investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50', start='01/01/2010', end='01/01/2019', as_json=param['as_json'], order=param['order'])

    retrieve_etfs()


if __name__ == '__main__':
    test_investpy()