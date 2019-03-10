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
 
    ```python
    import investpy
    
    equities_df_ = investpy.get_recent_data('bbva', as_json=False, order='ascending')
    funds_df_ = innvestpy.get_fund_recent_data('bbva multiactivo conservador pp', as_json=False, order='ascending')
    ```

* **Retrieve the historical data of an equity/fund from a specific range of time**: it retrieves the historical data from an equity/fund from a range of time between the start and the end date, specified in dd/mm/YY format. This function also checks is the introduced equity/fund name is correct and then retrieves the data.
The function has some optional parameters like: 
    * *as_json* by default is **False** but if True the output of the function is a JSON object, not a pandas.DataFrame.
    * *order* by default is **'ascending'** ordering the historical data in the pandas.DataFrame from the older to the newest, **'descending'** should be used for the contrary testing. 

    ```python
    import investpy
    
    equities_df_ = investpy.get_historical_data('bbva', '10/10/2018', '10/12/2018', as_json=False, order='ascending')
    funds_df_ = investpy.get_fund_historical_data('bbva multiactivo conservador pp', '10/10/2018', '10/12/2018', as_json=False, order='ascending')
    ```

You can check all the available equities/funds you can retrieve data from in Investing:
* Equities from the **Spanish Stock Market** -> https://es.investing.com/equities/spain
* Funds from the **Spanish Stock Market** -> https://es.investing.com/funds/spain-funds

(**NOTE**: you will need an active Internet connection in order to get the scraper working.)

## Performance Analysis

In this section I am going to explain the case study when developing the package and all the possible options when scraping in order to let you know which is the most efficient way to make a historical data scraper as far as I know based on my research over the past weeks.

Lets start with the first step before scraping a web, in this case [investing](https://es.investing.com/), the process of either downloading the web or sending a post request to a web. As we all know, there a two main tools used to get the HTML code from a website:
* [urllib3](https://pypi.org/project/urllib3/): urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too. urllib3 brings many critical features that are missing from the Python standard libraries.
* [requests](https://pypi.org/project/requests/): Requests allows you to send organic, grass-fed HTTP/1.1 requests, without the need for manual labor. There's no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to urllib3.

This unit tests are made with an stable Internet connection and done 500 times each, so we have a wide range of results in order to get to a better conclusion.
As we can see they are very related and similar, but with a significant efficiency difference when calculating the download time of a website's HTML code of a POST request, as shown in the graph:

![urllib3 vs requests](https://raw.githubusercontent.com/alvarob96/investpy/0.6/statistic%20plots/urllib3-requests.png)

If we analyse the graph, we can see that the mean time when sending a POST request is better when we use **requests** instead of **urllib3**, and it is also more stable and more consistent so on.

Once we have the HTML code resulting as the response to the POST request, we need to scrap the data from it and insert it into a pandas.DataFrame, so we are looking for a fast HTML parsing tool that allows us to retrieve huge loads of data really fast, so the user of the package does not wait too much.
The main Python packages used for HTML parsing are:
* [bs4](https://pypi.org/project/beautifulsoup4/): Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
* [lxml](https://pypi.org/project/lxml/): lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It provides safe and convenient access to these libraries using the ElementTree API. It extends the ElementTree API significantly to offer support for XPath, RelaxNG, XML Schema, XSLT, C14N and much more.

This unit tests are made with an stable Internet connection and done 500 times each, so we have a wide range of results in order to get to a better conclusion.
To determine which has a better time performance, we are going to parse a HTML that contains historical data from the last 10 years, to see which package works better for huge loads of data, as shown in the graph:

![bs4 vs lxml](https://raw.githubusercontent.com/alvarob96/investpy/0.6/statistic%20plots/bs4-lxml.png)

We can clearly see that **lxml** completely outperforms **bs4**, with a much more better time result when retrieving huge loads of data from a HTML file; and it is more stable, with less fluctuations being more consistent.

To sum up, we can clearly determine that the best combination in this use case is to use **requests** to download the HTML code and process the POST/GET requests, while when parsing the HTML (data extraction) we determine that **lxml** completely outperforms any other Python HTML parser.

If you have any other package you want to compare with the ones used in this case, feel free to send me a mail to alvarob96@usal.es and I will try my best to answer fast.

## Future Work

* Latest Spanish Stock News
* Allow multiple input equities/funds/etfs
* List equities, funds and etfs
* Remove bs4 for equity/fund/etf list retrieval

## Additional Information

The package is currently in a development version, so please, if needed open an [issues](https://github.com/alvarob96/investpy/issues) to solve all the possible problems the package may be causing
so I fix them as fast as I can. Also, any new ideas or proposals are welcome, and I will gladly implement them in the package if the are positive and useful.

For further information or any question feel free to contact me via email at alvarob96@usal.es

## Disclaimer

This Python Package has been made for research purposes in order to fit a needs that Investing.com does not cover, so this package works like an API for Investing.com developed in an altruistic way. Conclude that I am not related at all with Investing.com or any similar company, so I contacted Investing.com via mail and they gave me permission to develop this scraper with the condition of mentioning the source where I retrieve the data from.

To clear any doubt if this is legal or not, I will tell you literally what *Enrique from Investing.com Support* answered me when I asked them for permission to develop this scraper: "[...] *thank you for contacting and choosing us (as the reliable source to get the data from)* [...] *you can use and retrieve all the data that Investing.com offers to the users as far as you specify which is the source you get the data from* [...]".
