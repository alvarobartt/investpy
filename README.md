# investpy — a Python package for financial historical data extraction from Investing

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Anaconda Cloud Version](https://anaconda.org/alvarob96/investpy/badges/version.svg)](https://anaconda.org/alvarob96/investpy)
[![Package Status](https://img.shields.io/pypi/status/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://travis-ci.org/alvarob96/investpy.svg?branch=master)](https://travis-ci.org/alvarob96/investpy)
[![Documentation Status](https://readthedocs.org/projects/investpy/badge/?version=latest)](https://investpy.readthedocs.io/)
[![codecov](https://codecov.io/gh/alvarob96/investpy/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarob96/investpy)
[![Downloads](https://img.shields.io/pypi/dm/investpy.svg?style=flat)](https://pypistats.org/packages/investpy)

## Introduction

investpy is a Python package to retrieve real-time historical data from [Investing](https://www.investing.com/) mainly
of spanish financial products, but it is intended to be scalable and so on, work with world financial products such as 
equities, funds, ETFs or currencies.

investpy seeks to be one of the most used Python packages when it comes to historical data extraction from financial products, so to stop depending on public/private APIs, as investpy is **free** and has **no limitations**, features that lead investpy to be one of the most strong and consistent packages of financial data retrieval.

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) using pip on the terminal by typing:

``$ pip install investpy==0.8.7``

Every package used is listed in [requirements.txt](https://github.com/alvarob96/investpy/blob/master/requirements.txt) file, which can also be installed via pip:

``$ pip install -r requirements.txt``

## Usage

Even though some investpy usage examples are shown on the [docs](https://investpy.readthedocs.io/equities.html), some basic functionality will be sorted out with sample Python code blocks.

### Recent/Historical Data

As the main functionality is based on historical data retrieval, the usage of every function will be explained so to ease the user the use of investpy, which is mainly intended for historical data extraction, which means that every other function is additional.

#### Equity Data Retrieval

```python
import investpy

df = investpy.get_recent_data(equity='bbva', as_json=False, order='ascending')
print(df.head())

>>>
            Close   High    Low   Open    Volume
Date                                            
2019-07-12  4.897  4.985  4.897  4.952  22930000
2019-07-15  4.926  4.941  4.873  4.915  14830000
2019-07-16  4.971  5.008  4.913  4.947  30730000
2019-07-17  4.905  4.965  4.900  4.952  22410000
2019-07-18  4.856  4.894  4.812  4.879  35820000

df = investpy.get_historical_data(equity='bbva', from_date='01/01/2018', to_date='12/08/2019', as_json=False, order='ascending')
print(df.head())

>>>
            Close   High    Low   Open    Volume
Date                                            
2018-01-02  7.082  7.169  7.050  7.139  15960000
2018-01-03  7.094  7.120  7.055  7.113  13320000
2018-01-04  7.221  7.274  7.104  7.113  20790000
2018-01-05  7.253  7.282  7.203  7.259  13580000
2018-01-08  7.235  7.293  7.220  7.274  13420000
```

#### Fund Data Retrieval

```python
import investpy

df = investpy.get_fund_recent_data(fund='bbva plan multiactivo moderado pp', as_json=False, order='ascending')
print(df.head())

>>>
            Close   High    Low   Open
Date                                  
2019-07-12  1.128  1.128  1.128  1.128
2019-07-15  1.130  1.130  1.130  1.130
2019-07-16  1.130  1.130  1.130  1.130
2019-07-17  1.129  1.129  1.129  1.129
2019-07-18  1.126  1.126  1.126  1.126

df = investpy.get_fund_historical_data(fund='bbva plan multiactivo moderado pp', from_date='01/01/2018', to_date='12/08/2019', as_json=False, order='ascending')
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

df = investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50', as_json=False, order='ascending')
print(df.head())

>>>
             Close    High     Low    Open
Date                                      
2019-07-12  35.795  35.870  35.825  35.825
2019-07-15  35.855  35.930  35.760  35.875
2019-07-16  36.040  36.085  35.835  35.845
2019-07-17  35.830  36.080  35.810  35.965
2019-07-18  35.640  35.785  35.515  35.515

df = investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50', from_date='01/01/2018', to_date='12/08/2019', as_json=False, order='ascending')
print(df.head())

>>>
             Close    High     Low    Open
Date                                      
2018-01-02  34.995  35.155  34.860  35.155
2018-01-03  35.210  35.305  35.020  35.105
2018-01-04  35.825  35.710  35.465  35.465
2018-01-05  36.185  36.180  35.900  35.900
2018-01-08  36.280  36.370  36.240  36.325
```

### Additional Data

As Investing provides more data apart from historical data, some of that data is fetched via investpy if it is considered to be useful. So on, some additional information is retrieved for both equities and funds such as company profiles or inner basic information for equities and funds, respectively as shown below.

#### Equity Company Profile Retrieval

```python
import investpy

company_profile = investpy.get_equity_company_profile(equity='bbva', language='en')
print(company_profile)

>>> "Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a diversified financial company engaged in retail banking ..."
```

#### Fund Additional Information Retrieval

```python
import investpy

fund_information = investpy.get_fund_information(fund='bbva plan multiactivo moderado pp', as_json=True)
print(fund_information)

>>> {'Fund Name': 'Bbva Plan Multiactivo Moderado Pp',
 'Rating': '4',
 '1-Year Change': '-1,19%',
 'Previous Close': '1.103',
 'Risk Rating': '1',
 'TTM Yield': '0%',
 'ROE': '14,02%',
 'Issuer': 'BBVA Pensiones EGFP',
 'Turnover': 'N/A',
 'ROA': '4,97%',
 'Inception Date': '2012-10-16 00:00:00',
 'Total Assets': '1670000000',
 'Expenses': 'N/A',
 'Min Investment': '30',
 'Market Cap': '34820000000',
 'Category': 'Mixtos Euros Moderados PP'}
```

## Contribute - [![Open Source Helpers](https://www.codetriage.com/alvarob96/investpy/badges/users.svg)](https://www.codetriage.com/alvarob96/investpy)

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarob96/investpy/issues) where anyone can contribute opening new issues if needed or navigate through them in order to solve them or contribute to its solving.

Additionally, you can triage issues on [investpy CodeTriage](https://www.codetriage.com/alvarob96/investpy) so you can provide issues so the package can grow and improve as the issues solves bugs, problems or needs, and maybe provide new ideas to improve package functionality and efficiency.

## Disclaimer

This Python package has been made for research purposes in order to fit the needs that Investing.com does not cover, so this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement specified by Investing in order to develop this package was "*mention the source where data is retrieved from*".
