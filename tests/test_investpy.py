# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
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
        },
        {
            'country': 'indonesia',
            'as_json': False,
            'n_results': 362
        }
    ]

    for param in params:
        investpy.get_stocks_overview(country=param['country'], as_json=param['as_json'], n_results=param['n_results'])

    params = [
        {
            'stock': 'bbva',
            'country': 'spain'
        },
        {
            'stock': 'entel',
            'country': 'chile'
        }
    ]

    for param in params:
        investpy.get_stock_dividends(stock=param['stock'], country=param['country'])

    params = [
        {
            'stock': 'bbva',
            'country': 'spain',
            'summary_type': 'balance_sheet',
            'period': 'annual'
        },
        {
            'stock': 'aapl',
            'country': 'united states',
            'summary_type': 'income_statement',
            'period': 'quarterly'
        },
        {
            'stock': 'barc',
            'country': 'united kingdom',
            'summary_type': 'cash_flow_statement',
            'period': 'annual'
        }
    ]

    for param in params:
        investpy.get_stock_financial_summary(stock=param['stock'],
                                             country=param['country'], 
                                             summary_type=param['summary_type'],
                                             period=param['period'])

    investpy.search_stocks(by='name', value='BBVA')


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
        {
            'currency_cross': 'XAG/USD',
            'from_date': '01/01/2010',
            'to_date': '01/01/2015',
            'as_json': False,
            'order': 'descending',
        },
        {
            'currency_cross': 'XAU/USD',
            'from_date': '01/01/2010',
            'to_date': '01/01/2015',
            'as_json': False,
            'order': 'descending',
        }
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
        },
        {
            'currency_cross': 'XAU/USD',
            'as_json': True
        },
        {
            'currency_cross': 'XAG/USD',
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


def test_investpy_search():
    """
    This function checks that investpy search function works properly.
    """

    params = [
        {
            'text': 'bbva',
            'products': None,
            'countries': None,
            'n_results': 5
        },
        {
            'text': 'spain 3y',
            'products': None,
            'countries': None,
            'n_results': 5
        },
        {
            'text': 'ibex 35',
            'products': None,
            'countries': None,
            'n_results': 5
        },
        {
            'text': 'bnp daxplus',
            'products': None,
            'countries': None,
            'n_results': None
        },
        {
            'text': 'apple',
            'products': ['stocks'],
            'countries': ['united states'],
            'n_results': 1
        }
    ]

    for param in params:
        results = investpy.search_quotes(text=param['text'],
                                         products=param['products'],
                                         countries=param['countries'],
                                         n_results=param['n_results'])

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
            break


def test_investpy_news():
    """
    This function checks that investpy news retrieval functionality works as expected.
    """

    params = [
        {
            'time_zone': None,
            'time_filter': 'time_only',
            'countries': ['spain', 'france'],
            'importances': ['high', 'low'],
            'categories': ['credit', 'employment'],
            'from_date': None,
            'to_date': None
        },
        {
            'time_zone': 'GMT -3:00',
            'time_filter': 'time_only',
            'countries': None,
            'importances': None,
            'categories': None,
            'from_date': '01/01/2020',
            'to_date': '01/02/2020'
        }
    ]

    for param in params:
        investpy.economic_calendar(time_zone=param['time_zone'],
                                   time_filter=param['time_filter'],
                                   countries=param['countries'],
                                   importances=param['importances'],
                                   categories=param['categories'],
                                   from_date=param['from_date'],
                                   to_date=param['to_date'])


def test_investpy_technical():
    """
    This function checks that investpy news retrieval functionality works as expected.
    """

    params = list()

    for interval in list(investpy.utils.constant.INTERVAL_FILTERS.keys()):
        params.append({
            'name': 'bbva',
            'country': 'spain',
            'product_type': 'stock',
            'interval': interval
        })

    for param in params:
        investpy.technical_indicators(name=param['name'],
                                      country=param['country'],
                                      product_type=param['product_type'],
                                      interval=param['interval'])

        investpy.moving_averages(name=param['name'],
                                 country=param['country'],
                                 product_type=param['product_type'],
                                 interval=param['interval'])

        investpy.pivot_points(name=param['name'],
                              country=param['country'],
                              product_type=param['product_type'],
                              interval=param['interval'])


if __name__ == '__main__':
    test_investpy()
    test_investpy_stocks()
    test_investpy_currency_crosses()
    test_investpy_search()
    test_investpy_news()
    test_investpy_technical()
