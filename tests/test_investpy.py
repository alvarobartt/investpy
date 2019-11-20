#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pytest

import investpy


def test_investpy():
    """
    This function checks that both the investpy's author and version are the correct ones.
    """

    print(investpy.__author__)
    print(investpy.__version__)


def test_investpy_stocks():
    """
    This function checks that stock data retrieval functions listed in investpy work properly.
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
        investpy.get_stocks(country=param['country'])
        investpy.get_stocks_list(country=param['country'])

    params = [
        {
            'country': None,
            'columns': ['full_name', 'name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['full_name', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['full_name', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['full_name', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_stocks_dict(country=param['country'],
                                 columns=param['columns'],
                                 as_json=param['as_json'])

    investpy.get_stock_countries()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
        },
        {
            'as_json': False,
            'order': 'ascending',
        },
        {
            'as_json': True,
            'order': 'descending',
        },
        {
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_stock_recent_data(stock='BBVA',
                                       country='spain',
                                       as_json=param['as_json'],
                                       order=param['order'],
                                       interval='Daily')

        investpy.get_stock_historical_data(stock='BBVA',
                                           country='spain',
                                           from_date='01/01/1990',
                                           to_date='01/01/2019',
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           interval='Daily')

    for value in ['spanish', 'english']:
        investpy.get_stock_company_profile(stock='BBVA',
                                           country='spain',
                                           language=value)

    investpy.get_stock_dividends(stock='BBVA', country='spain')

    investpy.search_stocks(by='name', value='BBVA')


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
        },
        {
            'as_json': False,
            'order': 'ascending',
        },
        {
            'as_json': True,
            'order': 'descending',
        },
        {
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp',
                                      country='spain',
                                      as_json=param['as_json'],
                                      order=param['order'],
                                      interval='Daily')

        investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp',
                                          country='spain',
                                          from_date='01/01/2010',
                                          to_date='01/01/2019',
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          interval='Daily')

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
        },
        {
            'as_json': False,
            'order': 'ascending',
        },
        {
            'as_json': True,
            'order': 'descending',
        },
        {
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                     country='spain',
                                     as_json=param['as_json'],
                                     order=param['order'],
                                     interval='Daily')

        investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50',
                                         country='spain',
                                         from_date='01/01/2010',
                                         to_date='01/01/2019',
                                         as_json=param['as_json'],
                                         order=param['order'],
                                         interval='Daily')

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
        },
        {
            'as_json': False,
            'order': 'ascending',
        },
        {
            'as_json': True,
            'order': 'descending',
        },
        {
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_index_recent_data(index='ibex 35',
                                       country='spain',
                                       as_json=param['as_json'],
                                       order=param['order'],
                                       interval='Daily')

        investpy.get_index_historical_data(index='ibex 35',
                                           country='spain',
                                           from_date='01/01/2018',
                                           to_date='01/01/2019',
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           interval='Daily')

    investpy.search_indices(by='name', value='ibex')


def test_investpy_currency_crosses():
    """
    This function checks that currency cross data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'base': None,
            'second': None,
        },
        {
            'base': 'EUR',
            'second': None,
        },
        {
            'base': None,
            'second': 'EUR',
        },
        {
            'base': 'EUR',
            'second': 'USD',
        },
    ]

    for param in params:
        investpy.get_currency_crosses(base=param['base'], second=param['second'])
        investpy.get_currency_crosses_list(base=param['base'], second=param['second'])

    params = [
        {
            'base': None,
            'second': None,
            'columns': None,
            'as_json': True
        },
        {
            'base': None,
            'second': None,
            'columns': None,
            'as_json': False
        },
        {
            'base': 'EUR',
            'second': None,
            'columns': None,
            'as_json': True
        },
        {
            'base': 'EUR',
            'second': None,
            'columns': None,
            'as_json': False
        },
        {
            'base': None,
            'second': 'USD',
            'columns': None,
            'as_json': True
        },
        {
            'base': None,
            'second': 'USD',
            'columns': None,
            'as_json': False
        },
        {
            'base': 'EUR',
            'second': 'USD',
            'columns': None,
            'as_json': True
        },
        {
            'base': 'EUR',
            'second': 'USD',
            'columns': None,
            'as_json': False
        },
        {
            'base': 'EUR',
            'second': 'USD',
            'columns': ['name', 'full_name'],
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_currency_crosses_dict(base=param['base'],
                                           second=param['second'],
                                           columns=param['columns'],
                                           as_json=param['as_json'])

    investpy.get_available_currencies()

    params = [
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': True,
            'order': 'ascending',
        },
        {
            'currency_cross': 'EUR/USD',
            'from_date': '01/01/2018',
            'to_date': '01/01/2019',
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_currency_cross_recent_data(currency_cross=param['currency_cross'],
                                                as_json=param['as_json'],
                                                order=param['order'],
                                                interval='Daily')

        investpy.get_currency_cross_historical_data(currency_cross=param['currency_cross'],
                                                    from_date=param['from_date'],
                                                    to_date=param['to_date'],
                                                    as_json=param['as_json'],
                                                    order=param['order'],
                                                    interval='Daily')

    investpy.search_currency_crosses(by='base', value='EUR')


def test_investpy_bonds():
    """
    This function checks that bond data retrieval functions listed in investpy work properly.
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
        investpy.get_bonds(country=param['country'])
        investpy.get_bonds_list(country=param['country'])

    params = [
        {
            'country': None,
            'columns': ['full_name', 'name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['full_name', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['full_name', 'name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['full_name', 'name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_bonds_dict(country=param['country'],
                                columns=param['columns'],
                                as_json=param['as_json'])

    investpy.get_bond_countries()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
        },
        {
            'as_json': False,
            'order': 'ascending',
        },
        {
            'as_json': True,
            'order': 'descending',
        },
        {
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_bond_recent_data(bond='Spain 30Y',
                                      country='spain',
                                      as_json=param['as_json'],
                                      order=param['order'],
                                      interval='Daily')

        investpy.get_bond_historical_data(bond='Spain 30Y',
                                          country='spain',
                                          from_date='01/01/1990',
                                          to_date='01/01/2019',
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          interval='Daily')

    investpy.search_bonds(by='name', value='Spain')


def test_commodities():
    """
    This function checks that commodity data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'group': 'metals',
        },
        {
            'group': None,
        },
    ]

    for param in params:
        investpy.get_commodities(group=param['group'])
        investpy.get_commodities_list(group=param['group'])

    params = [
        {
            'group': None,
            'columns': ['title', 'full_name', 'name'],
            'as_json': True
        },
        {
            'group': None,
            'columns': ['title', 'full_name', 'name'],
            'as_json': False
        },
        {
            'group': 'metals',
            'columns': ['title', 'full_name', 'name'],
            'as_json': True
        },
        {
            'group': 'metals',
            'columns': ['title', 'full_name', 'name'],
            'as_json': False
        },
        {
            'group': 'metals',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_commodities_dict(group=param['group'],
                                      columns=param['columns'],
                                      as_json=param['as_json'])

    investpy.get_commodity_groups()

    params = [
        {
            'as_json': True,
            'order': 'ascending',
        },
        {
            'as_json': False,
            'order': 'ascending',
        },
        {
            'as_json': True,
            'order': 'descending',
        },
        {
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_commodity_recent_data(commodity='gold',
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           interval='Daily')

        investpy.get_commodity_historical_data(commodity='gold',
                                               from_date='01/01/1990',
                                               to_date='01/01/2019',
                                               as_json=param['as_json'],
                                               order=param['order'],
                                               interval='Daily')

    investpy.search_commodities(by='name', value='gold')


def test_search():
    """
    This function checks that investpy search function works properly.
    """

    params = [
        {
            'text': 'bbva',
        },
        {
            'text': 'endesa'
        }
    ]

    for param in params:
        investpy.search_text(text=param['text'])


if __name__ == '__main__':
    test_investpy()
    test_investpy_stocks()
    test_investpy_funds()
    test_investpy_etfs()
    test_investpy_indices()
    test_investpy_currency_crosses()
    test_investpy_bonds()
    test_search()
