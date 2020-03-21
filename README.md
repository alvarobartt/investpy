<p align="center">
  <img src="https://raw.githubusercontent.com/alvarobartt/investpy/master/docs/investpy_logo.png" hspace="20">
</p>

<h2 align="center">Financial Data Extraction from Investing.com with Python</h2>

investpy is a Python package to retrieve data from [Investing](https://www.investing.com/), which 
provides data retrieval from up to **39952 stocks, 82221 funds, 11403 etfs, 2029 currency crosses, 
7797 indices, 688 bonds, 66 commodities, 250 certificates and 2812 cryptocurrencies**. investpy allows you
to download historical data from all the financial products indexed in Investing.com. All the data that can be 
retrieved includes data from all over the world, from countries such as: **United States, France, India, Spain, Russia or 
Germany, amongst many others**. Therefore, investpy is intended to wrap up all the available data from Investing.com, 
so that it can be easily retrieved with Python for its further usage and/or analysis.

investpy seeks to be one of the most complete Python packages when it comes to financial data extraction
in order to stop relying on public/private APIs, since investpy is **FREE** and has **NO LIMITATIONS**. These
are some of the features that currently lead investpy to be one of the most consistent packages when it comes to financial 
data retrieval.

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Package Status](https://img.shields.io/pypi/status/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://dev.azure.com/alvarobartt/alvarobartt/_apis/build/status/investpy?branchName=master)](https://dev.azure.com/alvarobartt/alvarobartt/_build/latest?definitionId=3&branchName=master)
[![Build Status](https://img.shields.io/travis/alvarobartt/investpy/master.svg?label=Travis%20CI&logo=travis&logoColor=white)](https://travis-ci.org/alvarobartt/investpy)
[![Documentation Status](https://readthedocs.org/projects/investpy/badge/?version=latest)](https://investpy.readthedocs.io/)
[![codecov](https://codecov.io/gh/alvarobartt/investpy/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarobartt/investpy)

**Join gitter chat to ease developer-user communication and also contribute with other investpy users.**

[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/investpy/community?source=orgpage)

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) using 
pip on the terminal by typing:

``$ pip install investpy``

## Usage

Even though some investpy usage examples are shown on the [docs](https://investpy.readthedocs.io/usage.html), 
some basic functionality will be sorted out with sample Python code blocks.

### Recent/Historical Data Retrieval

As the main functionality is based on historical data retrieval, the usage of stock data retrieval functions 
will be explained so to ease the use of investpy, which is mainly intended for historical data extraction, which 
means that every other function is additional.

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

Investing.com search engine is completely integrated with investpy so that any available financial product (quote) 
can be easily found since the search function provides the user some parameters in order to adjust the search to their
needs, where both product types and countries from where the products are from can be specified. All the search functionality
can be easily achieved just using the following piece of code:

```python
import investpy

search_results = investpy.search(text='apple',
                                 products=['stocks'],
                                 countries=['united_states'],
                                 n_results=10)
```

Retrieved search results will be a `list` of `investpy.utils.search_obj.SearchObj` class instances. In order to get to 
know which are the available functions and attributes of the returned search results, please visit: 
[investpy Search Engine](https://investpy.readthedocs.io/search_api.html). So, those objects can be used to retrieve
retrieved product's historical data, its information, etc., as presented in this piece of code:

```python
 for search_result in search_results[:1]:
   print(search_result)
   search_result.retrieve_historical_data(from_date='01/01/2019', to_date='01/01/2020')
   print(search_result.data.head())
```
```{r, engine='python', count_lines}
{"id_": 6408, "name": "Apple Inc", "symbol": "AAPL", "country": "united states", "tag": "apple-computer-inc", "pair_type": "equities", "exchange": "NASDAQ"}

              Open    High     Low   Close    Volume
Date                                                
2019-01-02  154.89  158.85  154.23  157.92  37039736
2019-01-03  143.98  145.72  142.00  142.19  91312192
2019-01-04  144.53  148.55  143.80  148.26  58607072
2019-01-07  148.70  148.83  145.90  147.93  54777764
2019-01-08  149.56  151.82  148.52  150.75  41025312

```

### Crypto Currencies Data Retrieval

It has recently been included crypto currency data retrieval functions. All the crypto currencies that are
available in Investing for data retrieval are, so on, available in investpy.

So to ease investpy's usage, a sample will be presented below of how to retrieve the past 5 years of 
data from Bitcoin (BTC):

````python
import investpy

data = investpy.get_crypto_historical_data(crypto='bitcoin', from_date='01/01/2014', to_date='01/01/2019')

print(data.head())
````
```{r, engine='python', count_lines}
             Open    High    Low   Close  Volume Currency
Date                                                     
2014-01-01  805.9   829.9  771.0   815.9   10757      USD
2014-01-02  815.9   886.2  810.5   856.9   12812      USD
2014-01-03  856.9   888.2  839.4   884.3    9709      USD
2014-01-04  884.3   932.2  848.3   924.7   14239      USD
2014-01-05  924.7  1029.9  911.4  1014.7   21374      USD
```

Yes, retrieving historical data from any available crypto currency is really that easy!

## Utilities

Since investpy is intended to retrieve data from different financial products as indexed in Investing.com, the development 
of some support modules, which implement an additional functionallity based on investpy data, is presented. Note that anyone 
can contribute to this section by creating any package, module or utility which uses this package. So on, the ones already 
created are going to be presented, since they are intended to be used combined with investpy:

- [pyrtfolio](https://github.com/alvarobartt/pyrtfolio/): is a Python package to generate stock portfolios.
- [trendet](https://github.com/alvarobartt/trendet/): is a Python package for trend detection on stock time series data.

## Contribute - [![Open Source Helpers](https://www.codetriage.com/alvarobartt/investpy/badges/users.svg)](https://www.codetriage.com/alvarobartt/investpy)

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, 
enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarobartt/investpy/issues) where anyone can contribute opening 
new issues if needed or navigate through them in order to solve them or contribute to its solving. Remember that issues
are not threads to describe multiple issues, this does not mean that issues can't be discussed, but if new issues are 
reported, a new issue should be open so to keep a structured project management.

Additionally, you can triage issues on [investpy CodeTriage](https://www.codetriage.com/alvarobartt/investpy) so you can 
provide issues so the package can grow and improve as the issues solves bugs, problems or needs, and maybe provide new 
ideas to improve package functionality and efficiency.

## Reference

`investpy - a Python package for Financial Data Extraction from Investing.com developed by Álvaro Bartolomé del Canto @ alvarobartt at GitHub`

## Disclaimer

This Python package has been made for research purposes in order to fit the needs that Investing.com does not cover, so 
this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. 
Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement 
specified by Investing in order to develop this package was "*mention the source where data is retrieved from*".
