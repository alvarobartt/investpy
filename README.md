# investpy - Spanish Stock Historical Data Scraper

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://travis-ci.org/alvarob96/investpy.svg?branch=master)](https://pypi.org/project/investpy/)

## Introduction

Since [**Investing**](https://es.investing.com/) does not have an API, I decided to develop this Python scraper in order to retrieve historical data from the companies that integrate the **Continuous Spanish Stock Market**. The scraper is a Python package everyone can use through PyPi (Python Package Installer) via [investpy](https://pypi.org/project/investpy/).

The main purpose of developing this package was to use it as the **Data Extraction** tool for its namesake section, for my Final Degree Project at the University of Salamanca titled "**Machine Learning for stock investment recommendation systems**". The package end up being so consistent, reliable and usable that it is going to be used as the main Data Extraction tool by another students in their Final Degree Projects named "*Recommender system of banking products*" and "*Robo-Advisor Application*".

To conclude this section, I am in the need to specify that this is not the final version of the package, this is just a beta version of it that will keep going while I develop a consistent Python package for financial data extraction.

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) from PyPi via Terminal typing:

``pip install investpy==0.8.4.5``

All the dependencies are already listed on the setup file of the package, but to sum them up, you will need the following requirements:

* [**pandas 0.24.2**](https://pypi.org/project/pandas/)
* [**requests 2.21.0**](https://pypi.org/project/requests/)
* [**lxml 4.3.3**](https://pypi.org/project/lxml/)
* [**unidecode 1.0.23**](https://pypi.org/project/unidecode/)
* [**pytest 4.1.1**](https://pypi.org/project/pytest/)

## GitHub Gists on investpy use

In order to explain the use of [**investpy**](https://pypi.org/project/investpy/), some self-explanatory gists have been created and they can be found at [my GitHub Gist Page](https://gist.github.com/alvarob96). As the package is updated with new functionality, gists will be updated so they can be easily tested and provide useful information for investpy use.

* Equity Data Retrieval: https://gist.github.com/alvarob96/461dce00d9196dd3140f37993f8808f8

If needed you can open an [issue](https://github.com/alvarob96/investpy/issues) or [email me](alvarob96@usal.es) to request any other Gist or further explanation on how the package works.


## Release Notes 0.8.4.x

* Several fixes on minor bugs/errors
* Added support for Python 3.5
* Updated window size when data retrieval interval is above 20 years
* JSON structured to work better when plotting it
* docstring updated and "Use" section removed from package documentation
* Setup of some changes for future releases
* Handled errors such as input error return values or input dates format
* Full company name for equities add
* Company Profile retrieval returned value is a dict with the source and the description
* Internal fixes to improve its ease of adaptability
* Temporarily removed Python 2.7 support due to its warning of deprecation in January 1st of 2020
* Updated docstrings as reStructuredText (via PyCharm)
* Modified JSON output to fit current standard for historical data
* Added function to retrieve information from listed ETFs (id, name, symbol and tag)
* 

## Additional Information

The package is currently in a development version, so please, if needed open an [issues](https://github.com/alvarob96/investpy/issues) to solve all the possible problems the package may be causing
so I fix them as fast as I can. Also, any new ideas or proposals are welcome, and I will gladly implement them in the package if the are positive and useful.

For further information or any question feel free to contact me via email at alvarob96@usal.es

You can also check my [Medium Publication](https://medium.com/research-studies-by-alvaro-bartolome/investpy-a-python-library-for-historical-data-extraction-from-the-spanish-stock-market-ad4d564dbfc5), where I upload weekly posts related to Data Science and some of them explain investpy functions and development in a deeper way.

## Disclaimer

This Python Package has been made for research purposes in order to fit a needs that Investing.com does not cover, so this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement for developing this package was to mention the source where data is retrieved.