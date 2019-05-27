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


if __name__ == '__main__':
    test_equity_errors()