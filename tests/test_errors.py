#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import pytest

import investpy


def test_equity_errors():

    params = [
        {'equity': 'bbva', 'as_json': 'error', 'order': 'ascending'},
        {'equity': 'bbva', 'as_json': True, 'order': 'error'},
        {'equity': 'error', 'as_json': True, 'order': 'ascending'},
    ]

    for param in params:
        try:
            investpy.get_recent_data(equity=param['equity'], as_json=param['as_json'], order=param['order'])
        except:
            pass

    params = [
        {'equity': 'bbva', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': 'error', 'order': 'ascending'},
        {'equity': 'bbva', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': False, 'order': 'error'},
        {'equity': 'bbva', 'start': 'error', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
        {'equity': 'bbva', 'start': '01/01/2019', 'end': 'error', 'as_json': False, 'order': 'ascending'},
        {'equity': 'error', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
        {'equity': 'bbva', 'start': '01/01/1998', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
    ]

    for param in params:
        try:
            investpy.get_historical_data(equity=param['equity'], start=param['start'], end=param['end'],
                                         as_json=param['as_json'], order=param['order'])
        except:
            pass

    params = [
        {'equity': None, 'language': 'spanish'},
        {'equity': 'bbva', 'language': 'error'},
        {'equity': 'error', 'language': 'spanish'},
    ]

    for param in params:
        try:
            investpy.get_equity_company_profile(equity=param['equity'], language=param['language'])
        except:
            pass


def test_fund_errors():

    params = [
        {'columns': None, 'as_json': 'error'},
        {'columns': 0, 'as_json': True},
        {'columns': ['error'], 'as_json': False},
    ]

    for param in params:
        try:
            investpy.get_funds_dict(columns=param['columns'], as_json=param['as_json'])
        except:
            pass

    params = [
        {'fund': 'quality inversion conservadora fi', 'as_json': 'error', 'order': 'ascending'},
        {'fund': 'quality inversion conservadora fi', 'as_json': True, 'order': 'error'},
        {'fund': 'error', 'as_json': True, 'order': 'ascending'},
    ]

    for param in params:
        try:
            investpy.get_fund_recent_data(fund=param['fund'], as_json=param['as_json'], order=param['order'])
        except:
            pass

    params = [
        {'fund': 'quality inversion conservadora fi', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': 'error', 'order': 'ascending'},
        {'fund': 'quality inversion conservadora fi', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': False, 'order': 'error'},
        {'fund': 'quality inversion conservadora fi', 'start': 'error', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
        {'fund': 'quality inversion conservadora fi', 'start': '01/01/2019', 'end': 'error', 'as_json': False, 'order': 'ascending'},
        {'fund': 'error', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
        {'fund': 'quality inversion conservadora fi', 'start': '01/01/1998', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
    ]

    for param in params:
        try:
            print(param)
            investpy.get_fund_historical_data(fund=param['fund'], start=param['start'], end=param['end'], as_json=param['as_json'], order=param['order'])
        except:
            pass

    params = [
        {'fund': 'quality inversion conservadora fi', 'as_json': 'error'},
        {'fund': 'error', 'as_json': True},
    ]

    for param in params:
        try:
            print('hola')
            investpy.get_fund_information(fund=param['fund'], as_json=param['as_json'])
        except:
            pass


# def test_etf_errors():
#     params = [
#         {'columns': None, 'as_json': 'error'},
#         {'columns': 0, 'as_json': True},
#         {'columns': ['error'], 'as_json': False},
#     ]
#
#     for param in params:
#         try:
#             investpy.get_etfs_dict(columns=param['columns'], as_json=param['as_json'])
#         except:
#             pass
#
#     params = [
#         {'etf': 'bbva accion dj eurostoxx 50', 'as_json': 'error', 'order': 'ascending'},
#         {'etf': 'bbva accion dj eurostoxx 50', 'as_json': True, 'order': 'error'},
#         {'etf': 'error', 'as_json': True, 'order': 'ascending'},
#     ]
#
#     for param in params:
#         try:
#             investpy.get_etf_recent_data(etf=param['etf'], as_json=param['as_json'], order=param['order'])
#         except:
#             pass
#
#     params = [
#         {'etf': 'bbva accion dj eurostoxx 50', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': 'error', 'order': 'ascending'},
#         {'etf': 'bbva accion dj eurostoxx 50', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': False, 'order': 'error'},
#         {'etf': 'bbva accion dj eurostoxx 50', 'start': 'error', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
#         {'etf': 'bbva accion dj eurostoxx 50', 'start': '01/01/2019', 'end': 'error', 'as_json': False, 'order': 'ascending'},
#         {'etf': 'error', 'start': '01/01/2019', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
#         {'etf': 'bbva accion dj eurostoxx 50', 'start': '01/01/1998', 'end': '01/01/2019', 'as_json': False, 'order': 'ascending'},
#     ]
#
#     for param in params:
#         try:
#             investpy.get_etf_historical_data(etf=param['etf'], start=param['start'], end=param['end'], as_json=param['as_json'], order=param['order'])
#         except:
#             pass


if __name__ == '__main__':
    test_equity_errors()
    test_fund_errors()
    # test_etf_errors()