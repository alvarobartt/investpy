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

``pip install investpy==0.8``

All the dependencies are already listed on the setup file of the package, but to sum them up, you will need the following requirements:

* [**pandas 0.23.4**](https://pypi.org/project/pandas/)
* [**requests 2.20.0**](https://pypi.org/project/requests/)
* [**pytest 4.0.2**](https://pypi.org/project/pytest/)
* [**beautifulsoup4 4.6.3**](https://pypi.org/project/beautifulsoup4/)
* [**lxml 4.3.2**](https://pypi.org/project/lxml/)

## Use

As this package is in a Beta Version, every use or application of the package that is not implemented can b developed for future releases, so do not hesitate on asking for them. So on, currently using investpy you can:

* **Retrieve the Recent Data of an Equity/Fund/ETF**: it retrieves the historical data of an equity/fund/etf from the last month. The function also checks if the introduced equity/fund/etf name is correct and then retrieves the data.
The function has some optional parameters like: 
    * *as_json*, by default is **False** but if **True** the output of the function is a JSON object, not a pandas.DataFrame.
    * *order*, by default is **'ascending'** ordering the historical data in the pandas.DataFrame from the older to the newest, **'descending'** should be used for the contrary testing. 
 
    ```python
    import investpy
    
    equities_df = investpy.get_recent_data(equity='bbva', as_json=False, order='ascending')
    funds_df = investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp', as_json=False, order='ascending')
    etfs_df = investpy.get_etf_recent_data(etf='bbva-accion-dj-eurostoxx-50', as_json=False, order='ascending')
    ```

* **Retrieve the Historical Data of an Equity/Fund/ETF from a Specific Range of Time**: it retrieves the historical data from an equity/fund/etf from a range of time between the start and the end date, specified in dd/mm/YY format. This function also checks is the introduced equity/fund/etf name is correct and then retrieves the data.
The function has some optional parameters like:
    * *as_json*, by default is **False** but if **True** the output of the function is a JSON object, not a pandas.DataFrame.
    * *order*, by default is **'ascending'** ordering the historical data in the pandas.DataFrame from the older to the newest, **'descending'** should be used for the contrary testing. 

    ```python
    import investpy
    
    equities_df = investpy.get_historical_data(equity='bbva', start='10/10/2018', end='10/12/2018', as_json=False, order='ascending')
    funds_df = investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', start='10/10/2018', end='10/12/2018', as_json=False, order='ascending')
    etfs_df = investpy.get_etf_historical_data(etf='bbva-accion-dj-eurostoxx-50', start='10/10/2018', end='10/12/2018', as_json=False, order='ascending')
    ```
    
* **Retrieve the Company Profile of an Equity**: you can retrieve the company profile of an equity in spanish or english, so you need to specify a valid equity name and a valid source. 
The language of the Company Profile depends on the specified value for the following optional parameter:
    * **source**, Investing for English Profile or Bolsa de Madrid for Spanish Profile, but default value is Investing, so the Company Profile that this function is going to retrieve is going to be in English.

    ```python
    import investpy
    
    equity_profile = investpy.get_equity_company_profile(equity='bbva', source='Investing')
    ```
    
* **Retrieve Information Available of a Fund**: it consists on retrieving all the additional information indexed in Investing.com from a specified fund. The function checks that the fund is valid and it retrieves the information from it.
This function has an optional parameter:
    * **as_json**, if True instead of returning a pandas.DataFrame with the information it returns a JSON document, by default it is False.

    ```python
    import investpy
    
    fund_information = investpy.get_fund_information(fund='bbva multiactivo conservador pp', as_json=False)
    ```
    
* **Get a List of Available Equities/Funds/ETFs Names**: this function returns a list containing all the available equities/funds/etfs from where you can retrieve information from.

    ```python
    import investpy
    
    equities_list = investpy.get_equities_list()
    funds_list = investpy.get_funds_list()
    etfs_list = investpy.get_etfs_list()
    ```

    Or you can manually check all the available equities/funds/etfs indexed in Investing.com:
    * Equities from the **Spanish Stock Market** -> https://es.investing.com/equities/spain
    * Funds from the **Spanish Stock Market** -> https://es.investing.com/funds/spain-funds
    * ETFs from the **Spanish Stock Market** -> https://es.investing.com/etfs/spain-etfs

(**NOTE**: you will need an active Internet connection in order to get the scraper working.)

## Release Notes 0.8

* Company Profile Retrieval for All Equities
* Fund Historical Data Date Error Fixed
* Fund Overview Information Retrieval
* Functions for Listing Equities, Funds and ETFs

## Additional Information

The package is currently in a development version, so please, if needed open an [issues](https://github.com/alvarob96/investpy/issues) to solve all the possible problems the package may be causing
so I fix them as fast as I can. Also, any new ideas or proposals are welcome, and I will gladly implement them in the package if the are positive and useful.

For further information or any question feel free to contact me via email at alvarob96@usal.es

You can also check my [Medium Publication](https://medium.com/research-studies-by-alvaro-bartolome/investpy-a-python-library-for-historical-data-extraction-from-the-spanish-stock-market-ad4d564dbfc5), where I upload weekly posts related to Data Science and some of them explain investpy functions and development in a deeper way.

## Disclaimer

This Python Package has been made for research purposes in order to fit a needs that Investing.com does not cover, so this package works like an API for Investing.com developed in an altruistic way. Conclude that I am not related at all with Investing.com or any similar company, so I contacted Investing.com via mail and they gave me permission to develop this scraper with the condition of mentioning the source where I retrieve the data from.

To clear any doubt if this is legal or not, I will tell you literally what *Enrique from Investing.com Support* answered me when I asked them for permission to develop this scraper: "[...] *thank you for contacting and choosing us (as the reliable source to get the data from)* [...] *you can use and retrieve all the data that Investing.com offers to the users as far as you specify which is the source you get the data from* [...]".
