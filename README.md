<p align="center">
  <img src="https://raw.githubusercontent.com/alvarob96/investpy/master/docs/investpy_logo.png" hspace="20">
</p>

# Financial Historical Data Extraction with Python

investpy is a Python package to retrieve historical data from [Investing](https://www.investing.com/). 
It provides historical data retrieval from up to **29.628 stocks, 81.024 funds, 11.403 etfs, 1.889 currency crosses, 
7.797 indices and 688 bonds**. Basically, investpy allows you to download historical data from almost 
all the financial products indexed in Investing.com. All the data that can be retrieved includes data from all over the world, 
from countries such as: **United States, France, India, Spain, Russia or Germany, amongst many others**. Therefore, 
investpy is intended to wrap up all the available data from Investing.com, so that it can be retrieved via Python for 
its further usage and/or analysis.

investpy seeks to be one of the most complete Python packages when it comes to historical data extraction of financial
products in order to stop relying on public/private APIs, as investpy is **FREE** and has **NO LIMITATIONS**. These
are some of the features that currently lead investpy to be one of the most consistent packages of financial data retrieval.

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Package Status](https://img.shields.io/pypi/status/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://dev.azure.com/alvarob96/alvarob96/_apis/build/status/alvarob96.investpy?branchName=master)](https://dev.azure.com/alvarob96/alvarob96/_build?definitionId=1&_a=summary)
[![Build Status](https://img.shields.io/travis/alvarob96/investpy/master.svg?label=Travis%20CI&logo=travis&logoColor=white)](https://travis-ci.org/alvarob96/investpy)
[![Documentation Status](https://readthedocs.org/projects/investpy/badge/?version=latest)](https://investpy.readthedocs.io/)
[![codecov](https://codecov.io/gh/alvarob96/investpy/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarob96/investpy)
[![Downloads](https://img.shields.io/pypi/dm/investpy.svg?maxAge=2592000&label=installs&color=%2327B1FF)](https://pypistats.org/packages/investpy)

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) using 
pip on the terminal by typing:

``$ pip install investpy==0.9.9``

Every package used is listed in [requirements.txt](https://github.com/alvarob96/investpy/blob/master/requirements.txt)
file, which can also be installed via pip:

``$ pip install -r requirements.txt``

## Usage

Even though some investpy usage examples are shown on the [docs](https://investpy.readthedocs.io/usage.html), 
some basic functionality will be sorted out with sample Python code blocks.

### Recent/Historical Data Retrieval

As the main functionality is based on historical data retrieval, the usage of stock data retrieval functions 
will be explained so to ease the use of investpy, which is mainly intended for historical data extraction, which 
means that every other function is additional.

```python
import investpy

df = investpy.get_stock_recent_data(stock='BBVA',
                                    country='spain')
print(df.head())
```
```{r, engine='python', count_lines}
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

df = investpy.get_stock_historical_data(stock='BBVA',
                                        country='spain',
                                        from_date='01/01/2010',
                                        to_date='01/01/2019')
print(df.head())
```
```{r, engine='python', count_lines}
             Open   High    Low  Close  Volume Currency
Date                                                   
2010-01-04  12.73  12.96  12.73  12.96       0      EUR
2010-01-05  13.00  13.11  12.97  13.09       0      EUR
2010-01-06  13.03  13.17  13.02  13.12       0      EUR
2010-01-07  13.02  13.11  12.93  13.05       0      EUR
2010-01-08  13.12  13.22  13.04  13.18       0      EUR
```

### Search Data

As financial data is really complex and sometimes both the product name/symbol and the country are unknown for the user, in 
terms of what does investpy expect, every financial product listed in investpy (which currently includes stocks,
funds, etfs, indices and currency crosses) has its own search function. Search functions allow the user to search among
all the available stocks for example, whenever just one field is known (even though it is not the exact match). So on, a
basic example on stock search by the ISIN code is presented below:

````python
import investpy

search_results = investpy.search_stocks(by='isin', value='ES0113211835')

print(search_results.head())
````
```{r, engine='python', count_lines}
          country  name                             full_name          isin  currency symbol  
0          mexico  BBVA    Banco Bilbao Vizcaya Argentaria SA  ES0113211835       MXN   BBVA  
1          mexico  BBVA  Banco Bilbao Vizcaya Argentaria S.A.  ES0113211835       MXN   BBVA  
2         belgium  BBVA    Banco Bilbao Vizcaya Argentaria SA  ES0113211835       EUR   BBVA  
3           spain  BBVA  Banco Bilbao Vizcaya Argentaria S.A.  ES0113211835       EUR   BBVA  
4  united kingdom  BBVA    Banco Bilbao Vizcaya Argentaria Sa  ES0113211835       EUR   BVAB
```

### Additional Data

As Investing.com provides more data besides the historical one, some of that additional data can be fetched via investpy. 
Currently, as the package is under-development, some additional functions have been created in order to retrieve more data
as indexed in Investing.com. 

### and much more!

All the functions definitions and usage can be found in the [Documentation](https://investpy.readthedocs.io/)!

## Utilities

Since investpy is intended to retrieve data from different financial products as indexed in Investing.com, the development 
of some support modules, which implement an additional functionallity based on investpy data, is presented. Note that anyone 
can contribute to this section by creating any package, module or utility which uses this package. So on, the ones already 
created are going to be presented, since they are intended to be used combined with investpy:

- [investpy_portfolio](https://github.com/alvarob96/investpy_portfolio/): is a Python package to generate stock portfolios.
- [trendet](https://github.com/alvarob96/trendet/): is a Python package for trend detection on stock time series data.

## Contribute - [![Open Source Helpers](https://www.codetriage.com/alvarob96/investpy/badges/users.svg)](https://www.codetriage.com/alvarob96/investpy)

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, 
enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarob96/investpy/issues) where anyone can contribute opening 
new issues if needed or navigate through them in order to solve them or contribute to its solving. Remember that issues
are not threads to describe multiple issues, this does not mean that issues can't be discussed, but if new issues are 
reported, a new issue should be open so to keep a structured project management.

Additionally, you can triage issues on [investpy CodeTriage](https://www.codetriage.com/alvarob96/investpy) so you can 
provide issues so the package can grow and improve as the issues solves bugs, problems or needs, and maybe provide new 
ideas to improve package functionality and efficiency.

## Disclaimer

This Python package has been made for research purposes in order to fit the needs that Investing.com does not cover, so 
this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. 
Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement 
specified by Investing in order to develop this package was "*mention the source where data is retrieved from*".
