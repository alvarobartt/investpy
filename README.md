# Investing Scrapper of continuous Spanish stock market

[![Python Version](https://img.shields.io/pypi/pyversions/investing-scrapper.svg)](https://pypi.org/project/investing-scrapper/)
[![PyPi Version](https://img.shields.io/pypi/v/investing-scrapper.svg)](https://pypi.org/project/investing-scrapper/)
[![Build Status](https://travis-ci.org/alvarob96/investing-scrapper.svg?branch=master)](https://pypi.org/project/investing-scrapper/)

## Introduction

Since [**Investing**](https://es.investing.com/) does not have an API to retrieve historical data of the **Continuous Spanish Stock Market**, I decided to develop a scrapper to retrieve that information.

I developed this scrapper in order to get the data from Investing for my Final Degree Project at the University of Salamanca titled "**Machine Learning for stock investment recommendation systems**".

To sum up this is not the final version of this scrapper since this is just the pre-alpha version of it. So I will continue scrapping information indexed in investing so you can be able to retrieve more data, as soon as I can.

## Installation

In order to get this package working you will need to install [**investing-scrapper**](https://pypi.org/project/investing-scrapper/) from PyPi via Terminal: 

``pip install investing-scrapper``

All the dependencies are already listed on the setup file of the package, but to sum it up, you will need this requirements:

* [**pandas 0.23.4**](https://pypi.org/project/pandas/)
* [**requests 2.20.0**](https://pypi.org/project/requests/)
* [**pytest 4.0.2**](https://pypi.org/project/pytest/)
* [**beautifulsoup4 4.6.3**](https://pypi.org/project/beautifulsoup4/)

## Use

Currently you just have two possible options to retrieve data with this scrapper:

* **Retrieve the recent data of a stock**: it retrieves the historical data from a stock from the last month. The function also checks if the introduced equity name is correct and then retrieves the data.
```
import investing_scrapper as ivs

df = ivs.get_recent_data('bbva')
```

* **Retrieve the historical data of a stock from a specific range of time**: it retrieves the historical data from a stock from a range of time between the start date and the end date, specified in dd/mm/YY format. This function also checks is the introduced equity name is correct and then retrieves the data.
```
import investing_scrapper as ivs

df = ivs.get_historical_data('bbva', '10/10/2018', '10/12/2018')
```

You can check all the available equities for the **Spanish Stock Market** in this list from investing: https://es.investing.com/equities/spain

(**NOTE**: you will need an active HTTP connection in order to get the scrapper working. As a temporary solution, you can just store the retrieved pandas.DataFrame in a CSV so you can work with that data offline.)

## Future Work Ideas

* Spanish ETFs -> https://es.investing.com/etfs/spain-etfs
* Spanish Funds -> https://es.investing.com/funds/spain-funds **(In progress)**
* Latest Spanish Stock News -> https://es.investing.com/search/?q=ticker&tab=news
* Allow multiple date formats

## Information

For further information or any question feel free to contact me via email at alvarob96@usal.es

**Disclaimer:** this is just for personal use, I am not related at all with Investing or any similar company. This is just a tool for the research project I am working on. I get no profit or economic benefit from this scrapper.
