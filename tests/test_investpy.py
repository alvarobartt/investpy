#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import pytest
import investpy
from investpy.equities import get_equity_names
from investpy.funds import get_fund_names
from investpy.etfs import get_etf_names


def test_investing():
    """
    This function checks that main functions of investpy work properly.
    """

    investpy.get_equities()
    investpy.get_equities_list()
    investpy.get_recent_data(equity='enagás', as_json=True, order='ascending')
    investpy.get_historical_data(equity='enagás', start='30/10/2018', end='30/12/2018', as_json=False, order='ascending')
    investpy.get_equity_company_profile(equity='enagás', language='spanish')

    get_equity_names()

    investpy.get_funds()
    investpy.get_funds_list()
    investpy.get_funds_dict(columns=['id', 'tag'], as_json=False)
    investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp', as_json=False, order='ascending')
    investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', start='30/10/2018', end='30/12/2018', as_json=False, order='ascending')
    investpy.get_fund_information(fund='bbva multiactivo conservador pp')

    get_fund_names()

    investpy.get_etfs()
    investpy.get_etfs_list()
    investpy.get_etfs_dict(columns=['id', 'name'], as_json=False)
    investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50', as_json=False, order='ascending')
    investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50', start='30/10/2018', end='30/12/2018', as_json=False, order='ascending')

    get_etf_names()


if __name__ == '__main__':
    test_investing()