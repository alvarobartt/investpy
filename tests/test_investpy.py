#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
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

    params = [
        {
            'stock': 'bbva',
            'country': 'spain',
            'as_json': False
        },
        {
            'stock': 'bbva',
            'country': 'spain',
            'as_json': True
        },
        {
            'stock': 'HSBK',
            'country': 'kazakhstan',
            'as_json': False
        }
    ]

    for param in params:
        investpy.get_stock_information(stock=param['stock'], country=param['country'], as_json=param['as_json'])

    params = [
        {
            'country': 'spain',
            'as_json': True,
            'n_results': 50
        },
        {
            'country': 'united states',
            'as_json': False,
            'n_results': 50
        },
        {
            'country': 'bosnia',
            'as_json': False,
            'n_results': 50
        },
        {
            'country': 'palestine',
            'as_json': False,
            'n_results': 50
        },
        {
            'country': 'dubai',
            'as_json': False,
            'n_results': 50
        },
        {
            'country': 'ivory coast',
            'as_json': False,
            'n_results': 50
        }
    ]

    for param in params:
        investpy.get_stocks_overview(country=param['country'], as_json=param['as_json'], n_results=param['n_results'])

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
            'columns': ['name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['name'],
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

    params = [
        {
            'country': 'andorra',
            'as_json': True,
            'n_results': 2
        },
        {
            'country': 'andorra',
            'as_json': False,
            'n_results': 2
        },
        {
            'country': 'united states',
            'as_json': False,
            'n_results': 2
        },
        {
            'country': 'united kingdom',
            'as_json': False,
            'n_results': 2
        }
    ]

    for param in params:
        investpy.get_funds_overview(country=param['country'], as_json=param['as_json'], n_results=param['n_results'])

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
            'columns': ['name'],
            'as_json': True
        },
        {
            'country': None,
            'columns': ['name'],
            'as_json': False
        },
        {
            'country': 'spain',
            'columns': ['name'],
            'as_json': True
        },
        {
            'country': 'spain',
            'columns': ['name'],
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
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': False
        },
        {
            'etf': 'bbva accion dj eurostoxx 50',
            'country': 'spain',
            'as_json': True
        }
    ]

    for param in params:
        investpy.get_etf_information(etf=param['etf'], country=param['country'], as_json=param['as_json'])

    params = [
        {
            'country': 'united states',
            'as_json': True,
            'n_results': 2
        },
        {
            'country': 'united kingdom',
            'as_json': False,
            'n_results': 2
        },
    ]

    for param in params:
        investpy.get_etfs_overview(country=param['country'], as_json=param['as_json'], n_results=param['n_results'])

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

    params = [
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': False
        },
        {
            'index': 'ibex 35',
            'country': 'spain',
            'as_json': True
        }
    ]

    for param in params:
        investpy.get_index_information(index=param['index'], country=param['country'], as_json=param['as_json'])
    
    params = [
        {
            'country': 'united states', 
            'as_json': False,
            'n_results': 10
        },
        {
            'country': 'united kingdom', 
            'as_json': True,
            'n_results': 10
        }
    ]

    for param in params:
        investpy.get_indices_overview(country=param['country'], as_json=param['as_json'], n_results=param['n_results'])

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
            'from_date': '01/01/1990',
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

    params = [
        {
            'currency_cross': 'EUR/USD',
            'as_json': False
        },
        {
            'currency_cross': 'EUR/USD',
            'as_json': True
        }
    ]

    for param in params:
        investpy.get_currency_cross_information(currency_cross=param['currency_cross'], as_json=param['as_json'])
    
    params = [
        {
            'currency': 'try',
            'as_json': False,
            'n_results': 100
        },
        {
            'currency': 'amd',
            'as_json': True,
            'n_results': 100
        }
    ]
    
    for param in params:
        investpy.get_currency_crosses_overview(currency=param['currency'], as_json=param['as_json'], n_results=param['n_results'])

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
                                      as_json=param['as_json'],
                                      order=param['order'],
                                      interval='Daily')

        investpy.get_bond_historical_data(bond='Spain 30Y',
                                          from_date='01/01/1990',
                                          to_date='01/01/2019',
                                          as_json=param['as_json'],
                                          order=param['order'],
                                          interval='Daily')

    params = [
        {
            'bond': 'spain 30y',
            'as_json': False
        },
        {
            'bond': 'argentina 3y',
            'as_json': True
        },
        {
            'bond': 'germany 3m',
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_bond_information(bond=param['bond'], as_json=param['as_json'])
    
    params = [
        {
            'country': 'united states',
            'as_json': True,
        },
        {
            'country': 'united kingdom',
            'as_json': False,
        }
    ]

    for param in params:
        investpy.get_bonds_overview(country=param['country'], as_json=param['as_json'])

    investpy.search_bonds(by='name', value='Spain')


def test_investpy_commodities():
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
            'country': None,
            'as_json': True,
            'order': 'ascending',
        },
        {
            'country': 'united states',
            'as_json': False,
            'order': 'ascending',
        },
        {
            'country': 'united states',
            'as_json': True,
            'order': 'descending',
        },
        {
            'country': 'united states',
            'as_json': False,
            'order': 'descending',
        },
    ]

    for param in params:
        investpy.get_commodity_recent_data(commodity='copper',
                                           country=param['country'],
                                           as_json=param['as_json'],
                                           order=param['order'],
                                           interval='Daily')

        investpy.get_commodity_historical_data(commodity='copper',
                                               from_date='01/01/1990',
                                               to_date='01/01/2019',
                                               country=param['country'],
                                               as_json=param['as_json'],
                                               order=param['order'],
                                               interval='Daily')

    params = [
        {
            'commodity': 'copper',
            'country': None,
            'as_json': False
        },
        {
            'commodity': 'copper',
            'country': 'united states',
            'as_json': True
        }
    ]

    for param in params:
        investpy.get_commodity_information(commodity=param['commodity'], country=param['country'], as_json=param['as_json'])
    
    params = [
        {
            'group': 'metals',
            'as_json': True,
            'n_results': 100
        },
        {
            'group': 'metals',
            'as_json': False,
            'n_results': 100
        }
    ]

    for param in params:
        investpy.get_commodities_overview(group=param['group'], as_json=param['as_json'], n_results=param['n_results'])

    investpy.search_commodities(by='name', value='gold')


def test_investpy_cryptos():
    """
    This function checks that crypto currencies data retrieval functions listed in investpy work properly.
    """
    
    investpy.get_cryptos()
    investpy.get_cryptos_list()

    params = [
        {
            'columns': None,
            'as_json': False
        },
        {
            'columns': ['name', 'symbol', 'currency'],
            'as_json': False
        },
        {
            'columns': None,
            'as_json': True
        },    
    ]

    for param in params:
        investpy.get_cryptos_dict(columns=param['columns'],
                                  as_json=param['as_json'])

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
        investpy.get_crypto_recent_data(crypto='bitcoin',
                                        as_json=param['as_json'],
                                        order=param['order'],
                                        interval='Daily')

        investpy.get_crypto_historical_data(crypto='bitcoin',
                                            from_date='01/01/1990',
                                            to_date='01/01/2019',
                                            as_json=param['as_json'],
                                            order=param['order'],
                                            interval='Daily')

    params = [
        {
            'crypto': 'bitcoin',
            'as_json': False
        },
        {
            'crypto': 'bitcoin',
            'as_json': True
        }
    ]

    for param in params:
        investpy.get_crypto_information(crypto=param['crypto'], as_json=param['as_json'])
    
    params = [
        {
            'as_json': False,
            'n_results': 10
        },
        {
            'as_json': True,
            'n_results': 10
        },
        {
            'as_json': False,
            'n_results': 110
        },
        {
            'as_json': True,
            'n_results': 110
        },
        {
            'as_json': False,
            'n_results': None
        },
        {
            'as_json': True,
            'n_results': None
        },
    ]

    for param in params:
        investpy.get_cryptos_overview(as_json=param['as_json'], n_results=param['n_results'])

    investpy.search_cryptos(by='name', value='bitcoin')


def test_investpy_certificates():
    """
    This function checks that certificate data retrieval functions listed in investpy work properly.
    """

    params = [
        {
            'country': 'france',
        },
        {
            'country': None,
        },
    ]

    for param in params:
        investpy.get_certificates(country=param['country'])
        investpy.get_certificates_list(country=param['country'])

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
            'country': 'france',
            'columns': ['full_name', 'name'],
            'as_json': True
        },
        {
            'country': 'france',
            'columns': ['full_name', 'name'],
            'as_json': False
        },
        {
            'country': 'france',
            'columns': None,
            'as_json': False
        },
    ]

    for param in params:
        investpy.get_certificates_dict(country=param['country'],
                                       columns=param['columns'],
                                       as_json=param['as_json'])

    investpy.get_certificate_countries()

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
        investpy.get_certificate_recent_data(certificate='COMMERZBANK SG 31Dec99',
                                             country='france',
                                             as_json=param['as_json'],
                                             order=param['order'],
                                             interval='Daily')

        investpy.get_certificate_historical_data(certificate='COMMERZBANK SG 31Dec99',
                                                 country='france',
                                                 from_date='01/01/1990',
                                                 to_date='01/01/2019',
                                                 as_json=param['as_json'],
                                                 order=param['order'],
                                                 interval='Daily')

    params = [
        {
            'certificate': 'COMMERZBANK SG 31Dec99',
            'country': 'france',
            'as_json': False
        },
        {
            'certificate': 'COMMERZBANK SG 31Dec99',
            'country': 'france',
            'as_json': True
        }
    ]

    for param in params:
        investpy.get_certificate_information(certificate=param['certificate'],
                                             country=param['country'],
                                             as_json=param['as_json'])
    
    params = [
        {
            'country': 'france',
            'as_json': True,
            'n_results': 10
        },
        {
            'country': 'france',
            'as_json': False,
            'n_results': 10
        }
    ]

    for param in params:
        investpy.get_certificates_overview(country=param['country'],
                                           as_json=param['as_json'],
                                           n_results=param['n_results'])

    investpy.search_certificates(by='name', value='COMMERZBANK')


def test_investpy_search():
    """
    This function checks that investpy search function works properly.
    """

    params = [
        {
            'text': 'bbva',
            'n_results': 5,
            'filters': None
        },
        {
            'text': 'spain 3y',
            'n_results': 5,
            'filters': None
        },
        {
            'text': 'ibex 35',
            'n_results': 5,
            'filters': None
        },
        {
            'text': 'bnp daxplus',
            'n_results': 5,
            'filters': None
        },
        {
            'text': 'apple',
            'n_results': None,
            'filters': ['stocks']
        },
        {
            'text': 'apple',
            'n_results': 10,
            'filters': ['stocks']
        }
    ]

    for param in params:
        results = investpy.search(text=param['text'],
                                  n_results=param['n_results'],
                                  filters=param['filters'])

        dates = [
            {
                'from_date': '01/01/2018',
                'to_date': '01/01/2019'
            },
            {
                'from_date': '01/01/1990',
                'to_date': '01/01/2019'
            },
        ]

        for result in results:
            print(result)
            result.retrieve_recent_data()
            for date in dates:
                result.retrieve_historical_data(from_date=date['from_date'], to_date=date['to_date'])


if __name__ == '__main__':
    test_investpy()
    test_investpy_stocks()
    test_investpy_funds()
    test_investpy_etfs()
    test_investpy_indices()
    test_investpy_currency_crosses()
    test_investpy_bonds()
    test_investpy_commodities()
    test_investpy_cryptos()
    test_investpy_certificates()
    test_investpy_search()
