<a>
  <img src="https://raw.githubusercontent.com/alvarob96/investpy/master/docs/investpy_logo.png" align="right">
</a>

# investpy — a Python package for financial historical data extraction from Investing

investpy is a Python package to retrieve real-time historical data from [Investing](https://www.investing.com/). 
It provides historical data retrieval from up to **28.120 equities, 81.024 funds, 11.366 etfs, 1.889 currency crosses 
and 7.797 indices**. Basically, investpy allows you to download historical data from all the indexed equities, funds, 
currency crosses and etfs in Investing.com. All the data that can be retrieved includes data from all over the world, 
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

``$ pip install investpy==0.9.6``

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

df = investpy.get_historical_data(equity='bbva',
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

#### Fund Data Retrieval

```python
import investpy

df = investpy.get_fund_recent_data(fund='bbva plan multiactivo moderado pp',
                                   country='spain')
print(df.head())
```
```{r, engine='python', count_lines}
             Open   High    Low  Close Currency
Date                                           
2019-08-13  1.110  1.110  1.110  1.110      EUR
2019-08-16  1.109  1.109  1.109  1.109      EUR
2019-08-19  1.114  1.114  1.114  1.114      EUR
2019-08-20  1.112  1.112  1.112  1.112      EUR
2019-08-21  1.115  1.115  1.115  1.115      EUR

```

```python
import investpy

df = investpy.get_fund_historical_data(fund='bbva plan multiactivo moderado pp',
                                       country='spain',
                                       from_date='01/01/2010',
                                       to_date='01/01/2019')
print(df.head())
```
```{r, engine='python', count_lines}
             Open   High    Low  Close Currency
Date                                           
2018-02-15  1.105  1.105  1.105  1.105      EUR
2018-02-16  1.113  1.113  1.113  1.113      EUR
2018-02-17  1.113  1.113  1.113  1.113      EUR
2018-02-18  1.113  1.113  1.113  1.113      EUR
2018-02-19  1.111  1.111  1.111  1.111      EUR

```

#### ETF Data Retrieval

```python
import investpy

df = investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50',
                                  country='spain')
print(df.head())
```
```{r, engine='python', count_lines}
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
```
```{r, engine='python', count_lines}
             Open   High    Low  Close Currency
Date                                           
2011-12-07  23.70  23.70  23.70  23.62      EUR
2011-12-08  23.53  23.60  23.15  23.04      EUR
2011-12-09  23.36  23.60  23.36  23.62      EUR
2011-12-12  23.15  23.26  23.00  22.88      EUR
2011-12-13  22.88  22.88  22.88  22.80      EUR

```

#### Index Data Retrieval

```python
import investpy

df = investpy.get_index_recent_data(index='ibex 35',
                                    country='spain')
print(df.head())
```
```{r, engine='python', count_lines}
               Open     High      Low    Close   Volume Currency
Date
2019-08-26  12604.7  12646.3  12510.4  12621.3  4770000      EUR
2019-08-27  12618.3  12723.3  12593.6  12683.8  8230000      EUR
2019-08-28  12657.2  12697.2  12585.1  12642.5  7300000      EUR
2019-08-29  12637.2  12806.6  12633.8  12806.6  5650000      EUR
2019-08-30  12767.6  12905.9  12756.9  12821.6  6040000      EUR

```

```python
import investpy

df = investpy.get_index_historical_data(index='ibex 35',
                                        country='spain',
                                        from_date='01/01/2018',
                                        to_date='01/01/2019')
print(df.head())
```
```{r, engine='python', count_lines}
               Open     High      Low    Close    Volume Currency
Date
2018-01-02  15128.2  15136.7  14996.6  15096.8  10340000      EUR
2018-01-03  15145.0  15186.9  15091.9  15106.9  12800000      EUR
2018-01-04  15105.5  15368.7  15103.7  15368.7  17070000      EUR
2018-01-05  15353.9  15407.5  15348.6  15398.9  11180000      EUR
2018-01-08  15437.1  15448.7  15344.0  15373.3  12890000      EUR

```
#### Currency Crosses Data Retrieval

```python
import investpy

df = investpy.get_currency_cross_recent_data(currency_cross='EUR/USD')
print(df.head())
```
```{r, engine='python', count_lines}
              Open    High     Low   Close  Volume Currency
Date
2019-08-27  1.1101  1.1116  1.1084  1.1091       0      USD
2019-08-28  1.1090  1.1099  1.1072  1.1078       0      USD
2019-08-29  1.1078  1.1093  1.1042  1.1057       0      USD
2019-08-30  1.1058  1.1062  1.0963  1.0991       0      USD
2019-09-02  1.0990  1.1000  1.0958  1.0968       0      USD

```

```python
import investpy

df = investpy.get_currency_cross_historical_data(currency_cross='EUR/USD',
                                                 from_date='01/01/2018',
                                                 to_date='01/01/2019')
print(df.head())
```
```{r, engine='python', count_lines}
              Open    High     Low   Close  Volume Currency
Date
2018-01-01  1.2003  1.2014  1.1995  1.2010       0      USD
2018-01-02  1.2013  1.2084  1.2003  1.2059       0      USD
2018-01-03  1.2058  1.2070  1.2001  1.2014       0      USD
2018-01-04  1.2015  1.2090  1.2004  1.2068       0      USD
2018-01-05  1.2068  1.2085  1.2021  1.2030       0      USD

```

### Search Data

As financial data is really complex and sometimes both the product name and the country are unknown for the user, in 
terms of what does investpy expect, every financial product listed in investpy (which currently includes equities,
funds, etfs, indices and currency crosses) has its own search function. Search functions allow the user to search among
all the available equities for example, whenever just one field is known (even though it is not the exact match). So on,
the usage of this functions is presented below with some samples:

#### The user just knows the ISIN code of an Equity

````python
import investpy

search_results = investpy.search_equities(by='isin', value='ES0113211835')

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

#### The user just knows the Symbol of an Index

````python
import investpy

search_results = investpy.search_indices(by='name', value='IBEX')

print(search_results.head())
````
```{r, engine='python', count_lines}
  country             name        full_name  symbol currency         market
0   spain          IBEX 35          IBEX 35    IBEX      EUR  world_indices
1   spain     FTSE Latibex     FTSE Latibex   IBEXL      EUR  world_indices
2   spain  IBEX Medium Cap  IBEX Medium Cap   IBEXC      EUR  world_indices
3   spain   IBEX Small Cap   IBEX Small Cap   IBEXS      EUR  world_indices
4   spain    IBEX 35 Banks    IBEX 35 Banks  IBEXIB      EUR  world_indices
```

#### The user just knows a keyword contained in the name of an ETF

````python
import investpy

search_results = investpy.search_etfs(by='name', value='bbva')

print(search_results.head())
````
```{r, engine='python', count_lines}
  country                                       name     symbol currency
0  mexico  BBVA-BMV Mexico Consumo Frecuente RT TRAC  CONSUMO10      MXN
1  mexico             BBVA-BMV Mexico Enlace RT TRAC   ENLACE10      MXN
2   spain                BBVA Accion DJ Eurostoxx 50      BBVAE      EUR
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
```
```{r, engine='python', count_lines}
"Banco Bilbao Vizcaya Argentaria, S.A. (BBVA) is a diversified financial company engaged in retail banking ..."
```

#### Fund Additional Information Retrieval

```python
import investpy

fund_information = investpy.get_fund_information(fund='bbva plan multiactivo moderado pp',
                                                 country='spain',
                                                 as_json=True)
print(fund_information)
```
```{r, engine='python', count_lines}
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
```

And much more! All the functions usage can be found in the [Documentation](https://investpy.readthedocs.io/)!

## Contribute - [![Open Source Helpers](https://www.codetriage.com/alvarob96/investpy/badges/users.svg)](https://www.codetriage.com/alvarob96/investpy)

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, 
enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarob96/investpy/issues) where anyone can contribute opening 
new issues if needed or navigate through them in order to solve them or contribute to its solving. Remember that issues
are not threads to describe multiple issues, this does not mean that issues can't be discussed, but if new issues are 
reported, a new issue should be open so to keep a structured project management. Note that issues should be formatted as 
the description specified in [ISSUE_TEMPLATE](https://github.com/alvarob96/investpy/tree/master/.github/ISSUE_TEMPLATE),
which is automatically launched whenever you want to open an issue, but if you prefer you can open a custom issue, trying
to give all the information to identify the issue and solve it if possible.

Additionally, you can triage issues on [investpy CodeTriage](https://www.codetriage.com/alvarob96/investpy) so you can 
provide issues so the package can grow and improve as the issues solves bugs, problems or needs, and maybe provide new 
ideas to improve package functionality and efficiency.

## Disclaimer

This Python package has been made for research purposes in order to fit the needs that Investing.com does not cover, so 
this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. 
Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement 
specified by Investing in order to develop this package was "*mention the source where data is retrieved from*".
