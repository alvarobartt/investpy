#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import pytest
import investpy


def test_investing():
    """
    This function checks that main functions of investpy work properly.
    """

    investpy.get_recent_data(equity='enagás',
                             as_json=True,
                             order='ascending')

    investpy.get_historical_data(equity='enagás',
                                 start='30/10/2018',
                                 end='30/12/2018',
                                 as_json=False,
                                 order='ascending')

    investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp',
                                  as_json=False,
                                  order='ascending')

    investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp',
                                      start='30/10/2018',
                                      end='30/12/2018',
                                      as_json=False,
                                      order='ascending')

    investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                 as_json=False,
                                 order='ascending')

    investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50',
                                     start='30/10/2018',
                                     end='30/12/2018',
                                     as_json=False,
                                     order='ascending')
