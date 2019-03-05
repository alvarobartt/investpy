# Investing Scraper of historical data from continuous spanish stock market

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://travis-ci.org/alvarob96/investpy.svg?branch=master)](https://pypi.org/project/investpy/)

## Introduction

Since [**Investing**](https://es.investing.com/) does not have an API, I decided to develop this Python scraper in order to retrieve historical data from the companies that integrate the **Continuous Spanish Stock Market**. The scraper is a Python package everyone can use through PyPi (Python Package Installer) via [investpy](https://pypi.org/project/investpy/).

The main purpose of developing this package was to use it as the **Data Extraction** tool for its namesake section, for my Final Degree Project at the University of Salamanca titled "**Machine Learning for stock investment recommendation systems**". The package end up being so consistent, reliable and usable that it is going to be used as the main Data Extraction tool by another students in their Final Degree Projects named "*Recommender system of banking products*" and "*Robo-Advisor Application*".

To conclude this section, I am in the need to specify that this is not the final version of the package, this is just a beta version of it that will keep going while I develop a consistent Python package for financial data extraction.

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) from PyPi via Terminal typing:

``pip install investpy``

All the dependencies are already listed on the setup file of the package, but to sum them up, you will need the following requirements:

* [**pandas 0.23.4**](https://pypi.org/project/pandas/)
* [**requests 2.20.0**](https://pypi.org/project/requests/)
* [**pytest 4.0.2**](https://pypi.org/project/pytest/)
* [**beautifulsoup4 4.6.3**](https://pypi.org/project/beautifulsoup4/)
* [**lxml 4.3.2**](https://pypi.org/project/lxml/)

## Use

Currently you just have two possible options to retrieve data with this scraper:

* **Retrieve the recent data of an equity/fund**: it retrieves the historical data of an equity/fund from the last month. The function also checks if the introduced equity/fund name is correct and then retrieves the data.
The function has some optional parameters like: 
    * *as_json* by default is **False** but if True the output of the function is a JSON object, not a pandas.DataFrame.
    * *order* by default is **'ascending'** ordering the historical data in the pandas.DataFrame from the older to the newest, **'descending'** should be used for the contrary testing. 
 
    ```
    import investpy
    
    equities_df_ = investpy.get_recent_data('bbva', as_json=False, order='ascending')
    funds_df_ = innvestpy.get_fund_recent_data('bbva multiactivo conservador pp', as_json=False, order='ascending')
    ```

* **Retrieve the historical data of an equity/fund from a specific range of time**: it retrieves the historical data from an equity/fund from a range of time between the start and the end date, specified in dd/mm/YY format. This function also checks is the introduced equity/fund name is correct and then retrieves the data.
The function has some optional parameters like: 
    * *as_json* by default is **False** but if True the output of the function is a JSON object, not a pandas.DataFrame.
    * *order* by default is **'ascending'** ordering the historical data in the pandas.DataFrame from the older to the newest, **'descending'** should be used for the contrary testing. 

    ```
    import investpy
    
    equities_df_ = investpy.get_historical_data('bbva', '10/10/2018', '10/12/2018', as_json=False, order='ascending')
    funds_df_ = investpy.get_fund_historical_data('bbva multiactivo conservador pp', '10/10/2018', '10/12/2018', as_json=False, order='ascending')
    ```

You can check all the available equities/funds you can retrieve data from in Investing:
* Equities from the **Spanish Stock Market** -> https://es.investing.com/equities/spain
* Funds from the **Spanish Stock Market** -> https://es.investing.com/funds/spain-funds

(**NOTE**: you will need an active Internet connection in order to get the scraper working.)

## Performance Analysis and Case Study

Detailed in Jupyter Notebook

## Future Work

* Spanish ETFs
* Latest Spanish Stock News
* Allow multiple date formats
* Add more function parameters if needed

## Additional Information

The package is currently in a development version, so please, if needed open an [issues](https://github.com/alvarob96/investpy/issues) to solve all the possible problems the package may be causing
so I fix them as fast as I can. Also, any new ideas or proposals are welcome, and I will gladly implement them in the package if the are positive and useful.

For further information or any question feel free to contact me via email at alvarob96@usal.es

## Disclaimer

This Python Package has been made for research purposes in order to fit a needs that Investing.com does not cover, so this package works like an API for Investing.com developed in an altruistic way. Conclude that I am not related at all with Investing.com or any similar company, so I contacted Investing.com via mail and they gave me permission to develop this scraper with the condition of mentioning the source where I retrieve the data from.
