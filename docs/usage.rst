Usage
=====

Along this document, the main `investpy <https://github.com/alvarobartt/investpy>`_ functions are going to be presented. So on, this is a tutorial 
on how to use **investpy** to retrieve data from the financial products available, such as: stocks, funds, ETFs, indices and currency crosses, 
retrieved from Investing.com.

Recent/Historical Data Retrieval
--------------------------------

The main functionallity of **investpy** is to retrieve historical data from the indexed financial products. So both recent and historical data
retrieval functions have been developed in order to retrieve data from the last month or from a concrete period of time, respectively.

Stock Data Retrieval
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    df = investpy.get_stock_recent_data(stock='bbva',
                                        country='spain')
    print(df.head())
    
                 Open   High    Low  Close    Volume Currency
    Date                                                     
    2019-08-13  4.263  4.395  4.230  4.353  27250000      EUR
    2019-08-14  4.322  4.325  4.215  4.244  36890000      EUR
    2019-08-15  4.281  4.298  4.187  4.234  21340000      EUR
    2019-08-16  4.234  4.375  4.208  4.365  46080000      EUR
    2019-08-19  4.396  4.425  4.269  4.269  18950000      EUR


.. code-block:: python

    import investpy

    df = investpy.get_stock_historical_data(stock='AAPL',
                                            country='United States',
                                            from_date='01/01/2010',
                                            to_date='01/01/2020')
    print(df.head())

                Open   High    Low  Close     Volume Currency
    Date                                                      
    2010-01-04  30.49  30.64  30.34  30.57  123432176      USD
    2010-01-05  30.66  30.80  30.46  30.63  150476160      USD
    2010-01-06  30.63  30.75  30.11  30.14  138039728      USD
    2010-01-07  30.25  30.29  29.86  30.08  119282440      USD
    2010-01-08  30.04  30.29  29.87  30.28  111969192      USD

Fund Data Retrieval
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    df = investpy.get_fund_recent_data(fund='bbva plan multiactivo moderado pp',
                                       country='spain')
    print(df.head())
    
                 Open   High    Low  Close Currency
    Date                                           
    2019-08-13  1.110  1.110  1.110  1.110      EUR
    2019-08-16  1.109  1.109  1.109  1.109      EUR
    2019-08-19  1.114  1.114  1.114  1.114      EUR
    2019-08-20  1.112  1.112  1.112  1.112      EUR
    2019-08-21  1.115  1.115  1.115  1.115      EUR

.. code-block:: python

    import investpy

    df = investpy.get_fund_historical_data(fund='bbva plan multiactivo moderado pp',
                                           country='spain',
                                           from_date='01/01/2010',
                                           to_date='01/01/2019')
    print(df.head())
    
                 Open   High    Low  Close Currency
    Date                                           
    2018-02-15  1.105  1.105  1.105  1.105      EUR
    2018-02-16  1.113  1.113  1.113  1.113      EUR
    2018-02-17  1.113  1.113  1.113  1.113      EUR
    2018-02-18  1.113  1.113  1.113  1.113      EUR
    2018-02-19  1.111  1.111  1.111  1.111      EUR

ETF Data Retrieval
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    df = investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                      country='spain')
    print(df.head())
    
                  Open    High     Low   Close Currency
    Date                                               
    2019-08-13  33.115  33.780  32.985  33.585      EUR
    2019-08-14  33.335  33.335  32.880  32.905      EUR
    2019-08-15  32.790  32.925  32.455  32.845      EUR
    2019-08-16  33.115  33.200  33.115  33.305      EUR
    2019-08-19  33.605  33.735  33.490  33.685      EUR

.. code-block:: python

    import investpy

    df = investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50',
                                          country='spain',
                                          from_date='01/01/2018',
                                          to_date='01/01/2019')
    print(df.head())
    
                 Open   High    Low  Close Currency
    Date                                           
    2011-12-07  23.70  23.70  23.70  23.62      EUR
    2011-12-08  23.53  23.60  23.15  23.04      EUR
    2011-12-09  23.36  23.60  23.36  23.62      EUR
    2011-12-12  23.15  23.26  23.00  22.88      EUR
    2011-12-13  22.88  22.88  22.88  22.80      EUR

Index Data Retrieval
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    df = investpy.get_index_recent_data(index='ibex 35',
                                        country='spain')
    print(df.head())
    
                   Open     High      Low    Close   Volume Currency
    Date
    2019-08-26  12604.7  12646.3  12510.4  12621.3  4770000      EUR
    2019-08-27  12618.3  12723.3  12593.6  12683.8  8230000      EUR
    2019-08-28  12657.2  12697.2  12585.1  12642.5  7300000      EUR
    2019-08-29  12637.2  12806.6  12633.8  12806.6  5650000      EUR
    2019-08-30  12767.6  12905.9  12756.9  12821.6  6040000      EUR

.. code-block:: python

    import investpy

    df = investpy.get_index_historical_data(index='ibex 35',
                                            country='spain',
                                            from_date='01/01/2018',
                                            to_date='01/01/2019')
    print(df.head())
    
                   Open     High      Low    Close    Volume Currency
    Date
    2018-01-02  15128.2  15136.7  14996.6  15096.8  10340000      EUR
    2018-01-03  15145.0  15186.9  15091.9  15106.9  12800000      EUR
    2018-01-04  15105.5  15368.7  15103.7  15368.7  17070000      EUR
    2018-01-05  15353.9  15407.5  15348.6  15398.9  11180000      EUR
    2018-01-08  15437.1  15448.7  15344.0  15373.3  12890000      EUR

Currency Crosses Data Retrieval
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    df = investpy.get_currency_cross_recent_data(currency_cross='EUR/USD')
    print(df.head())
    
                  Open    High     Low   Close  Volume Currency
    Date
    2019-08-27  1.1101  1.1116  1.1084  1.1091       0      USD
    2019-08-28  1.1090  1.1099  1.1072  1.1078       0      USD
    2019-08-29  1.1078  1.1093  1.1042  1.1057       0      USD
    2019-08-30  1.1058  1.1062  1.0963  1.0991       0      USD
    2019-09-02  1.0990  1.1000  1.0958  1.0968       0      USD

.. code-block:: python

    import investpy

    df = investpy.get_currency_cross_historical_data(currency_cross='EUR/USD',
                                                     from_date='01/01/2018',
                                                     to_date='01/01/2019')
    print(df.head())
    
                Open    High     Low   Close  Volume Currency
    Date
    2018-01-01  1.2003  1.2014  1.1995  1.2010       0      USD
    2018-01-02  1.2013  1.2084  1.2003  1.2059       0      USD
    2018-01-03  1.2058  1.2070  1.2001  1.2014       0      USD
    2018-01-04  1.2015  1.2090  1.2004  1.2068       0      USD
    2018-01-05  1.2068  1.2085  1.2021  1.2030       0      USD

Additional Data
---------------

As Investing.com provides more data besides the historical one, some of that additional data can be fetched via investpy. 
Currently, as the package is under-development, some additional functions have been created in order to retrieve more data
as indexed in Investing.com. 

Stock Company Profile Retrieval
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    company_profile = investpy.get_stock_company_profile(stock='bbva',
                                                         country='spain')
    print(company_profile)
     
    {
        "url": "https://www.investing.com/equities/bbva-company-profile",
        "description": "Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a diversified financial company engaged in retail banking ..."
    }

Fund Information Retrieval
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import investpy

    fund_information = investpy.get_fund_information(fund='bbva plan multiactivo moderado pp',
                                                     country='spain',
                                                     as_json=True)
    print(fund_information)
    
    {
        'Fund Name': 'Bbva Plan Multiactivo Moderado Pp',
        'Rating': 4,
        '1-Year Change': '-1,19%',
        'Previous Close': '1.103',
        'Risk Rating': 1,
        'TTM Yield': '0%',
        'ROE': '14,02%',
        'Issuer': 'BBVA Pensiones EGFP',
        'Turnover': None,
        'ROA': '4,97%',
        'Inception Date': '16/10/2012',
        'Total Assets': 1670000000,
        'Expenses': None,
        'Min Investment': 30,
        'Market Cap': 34820000000,
        'Category': 'Mixtos Euros Moderados PP'
    }