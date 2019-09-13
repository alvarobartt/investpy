# investpy — a Python package for financial historical data extraction from Investing

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Anaconda Cloud Version](https://anaconda.org/alvarob96/investpy/badges/version.svg)](https://anaconda.org/alvarob96/investpy)
[![Package Status](https://img.shields.io/pypi/status/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://dev.azure.com/alvarob96/alvarob96/_apis/build/status/alvarob96.investpy?branchName=master)](https://dev.azure.com/alvarob96/alvarob96/_build?definitionId=1&_a=summary)
[![Build Status](https://img.shields.io/travis/alvarob96/investpy/master.svg?label=Travis%20CI&logo=travis&logoColor=white)](https://travis-ci.org/alvarob96/investpy)
[![Documentation Status](https://readthedocs.org/projects/investpy/badge/?version=latest)](https://investpy.readthedocs.io/)
[![codecov](https://codecov.io/gh/alvarob96/investpy/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarob96/investpy)
[![Downloads](https://img.shields.io/pypi/dm/investpy.svg?maxAge=2592000&label=installs&color=%2327B1FF)](https://pypistats.org/packages/investpy)

## Introduction


investpy is a Python package to retrieve real-time historical data from [Investing](https://www.investing.com/). 
It provides historical data retrieval from up to **28.121 equities, 4.120 funds and 8.755 etfs**. Basically, 
it allows you to download historical data from all the indexed equities, funds and etfs in Investing.com. Therefore,
investpy is intended to wrap up all the available data from Investing, so that it can be retrieved via Python for 
its further usage and/or analysis.

investpy seeks to be one of the most complete Python packages when it comes to historical data extraction of financial
products in order to stop relying on public/private APIs, as investpy is **FREE** and has **NO LIMITATIONS**. These
are some of the features that currently lead investpy to be one of the most consistent packages of financial data retrieval.

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) using 
pip on the terminal by typing:

``$ pip install investpy==0.9.1``

Every package used is listed in [requirements.txt](https://github.com/alvarob96/investpy/blob/master/requirements.txt) 
file, which can also be installed via pip:

``$ pip install -r requirements.txt``

## Usage

Even though some investpy usage examples are shown on the [docs](https://investpy.readthedocs.io/equities.html), 
some basic functionality will be sorted out with sample Python code blocks.

### Recent/Historical Data

As the main functionality is based on historical data retrieval, the usage of every function will be explained so to 
ease the user the use of investpy, which is mainly intended for historical data extraction, which means that every 
other function is additional.

#### Equity Data Retrieval

```python
import investpy

df = investpy.get_recent_data(equity='bbva',
                              country='spain')
print(df.head())

>>>
             Open   High    Low  Close    Volume Currency
Date                                                     
2019-08-13  4.263  4.395  4.230  4.353  27250000      EUR
2019-08-14  4.322  4.325  4.215  4.244  36890000      EUR
2019-08-15  4.281  4.298  4.187  4.234  21340000      EUR
2019-08-16  4.234  4.375  4.208  4.365  46080000      EUR
2019-08-19  4.396  4.425  4.269  4.269  18950000      EUR

```

```python
import investpy

df = investpy.get_historical_data(equity='bbva',
                                  country='spain',
                                  from_date='01/01/2010',
                                  to_date='01/01/2019')
print(df.head())

>>>
             Open   High    Low  Close  Volume Currency
Date                                                   
2010-01-04  12.73  12.96  12.73  12.96       0      EUR
2010-01-05  13.00  13.11  12.97  13.09       0      EUR
2010-01-06  13.03  13.17  13.02  13.12       0      EUR
2010-01-07  13.02  13.11  12.93  13.05       0      EUR
2010-01-08  13.12  13.22  13.04  13.18       0      EUR

```

#### Fund Data Retrieval

```python
import investpy

df = investpy.get_fund_recent_data(fund='bbva plan multiactivo moderado pp',
                                   country='spain')
print(df.head())

>>>
            Close   High    Low   Open
Date                                  
2019-07-12  1.128  1.128  1.128  1.128
2019-07-15  1.130  1.130  1.130  1.130
2019-07-16  1.130  1.130  1.130  1.130
2019-07-17  1.129  1.129  1.129  1.129
2019-07-18  1.126  1.126  1.126  1.126

```

```python
import investpy

df = investpy.get_fund_historical_data(fund='bbva plan multiactivo moderado pp',
                                       country='spain',
                                       from_date='01/01/2010',
                                       to_date='01/01/2019')
print(df.head())

>>>
            Close   High    Low   Open
Date                                  
2018-02-15  1.105  1.105  1.105  1.105
2018-02-16  1.113  1.113  1.113  1.113
2018-02-17  1.113  1.113  1.113  1.113
2018-02-18  1.113  1.113  1.113  1.113
2018-02-19  1.111  1.111  1.111  1.111

```

#### ETF Data Retrieval

```python
import investpy

df = investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                  country='spain')
print(df.head())

>>>
              Open    High     Low   Close Currency
Date                                               
2019-08-13  33.115  33.780  32.985  33.585      EUR
2019-08-14  33.335  33.335  32.880  32.905      EUR
2019-08-15  32.790  32.925  32.455  32.845      EUR
2019-08-16  33.115  33.200  33.115  33.305      EUR
2019-08-19  33.605  33.735  33.490  33.685      EUR

```

```python
import investpy

df = investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50',
                                      country='spain',
                                      from_date='01/01/2018',
                                      to_date='01/01/2019')
print(df.head())

>>>
             Open   High    Low  Close Currency
Date                                           
2011-12-07  23.70  23.70  23.70  23.62      EUR
2011-12-08  23.53  23.60  23.15  23.04      EUR
2011-12-09  23.36  23.60  23.36  23.62      EUR
2011-12-12  23.15  23.26  23.00  22.88      EUR
2011-12-13  22.88  22.88  22.88  22.80      EUR

```

### Additional Data

As Investing provides more data besides the historical one, some of that additional data can be fetched via investpy. 
Currently, as the package is under-development, some additional information such as company profiles or inner basic 
information is retrieved for both equities and funds, respectively as shown below.

#### Equity Company Profile Retrieval

```python
import investpy

company_profile = investpy.get_equity_company_profile(equity='bbva',
                                                      country='spain')
print(company_profile)

>>> "Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a diversified financial company engaged in retail banking ..."
```

#### Fund Additional Information Retrieval

```python
import investpy

fund_information = investpy.get_fund_information(fund='bbva plan multiactivo moderado pp',
                                                 country='spain',
                                                 as_json=True)
print(fund_information)

>>> {
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
```

## Contribute - [![Open Source Helpers](https://www.codetriage.com/alvarob96/investpy/badges/users.svg)](https://www.codetriage.com/alvarob96/investpy)

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, 
enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarob96/investpy/issues) where anyone can contribute opening 
new issues if needed or navigate through them in order to solve them or contribute to its solving.

Additionally, you can triage issues on [investpy CodeTriage](https://www.codetriage.com/alvarob96/investpy) so you can 
provide issues so the package can grow and improve as the issues solves bugs, problems or needs, and maybe provide new 
ideas to improve package functionality and efficiency.

## Disclaimer

This Python package has been made for research purposes in order to fit the needs that Investing.com does not cover, so 
this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. 
Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement 
specified by Investing in order to develop this package was "*mention the source where data is retrieved from*".
