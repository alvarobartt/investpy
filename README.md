# investpy — Python package for stock historical data extraction from Investing

[![Python Version](https://img.shields.io/pypi/pyversions/investpy.svg)](https://pypi.org/project/investpy/)
[![PyPi Version](https://img.shields.io/pypi/v/investpy.svg)](https://pypi.org/project/investpy/)
[![Anaconda Cloud Version](https://anaconda.org/alvarob96/investpy/badges/version.svg)](https://pypi.org/project/investpy/)
[![Package Status](https://img.shields.io/pypi/status/investpy.svg)](https://pypi.org/project/investpy/)
[![Build Status](https://travis-ci.org/alvarob96/investpy.svg?branch=master)](https://pypi.org/project/investpy/)
[![Documentation Status](https://readthedocs.org/projects/investpy/badge/?version=latest)](https://investpy.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/alvarob96/investpy/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarob96/investpy)
[![Downloads](https://img.shields.io/pypi/dm/investpy.svg?style=flat)](https://pypi.python.org/pypi/investpy)

## Introduction

Since [**Investing**](https://es.investing.com/) does not have an API, I decided to develop this Python scraper in order to retrieve historical data from the companies that integrate the **Continuous Spanish Stock Market**. The scraper is a Python package everyone can use through PyPi (Python Package Installer) via [investpy](https://pypi.org/project/investpy/).

The main purpose of developing this package was to use it as the **Data Extraction** tool for its namesake section, for my Final Degree Project at the University of Salamanca titled "**Machine Learning for stock investment recommendation systems**". The package end up being so consistent, reliable and usable that it is going to be used as the main Data Extraction tool by another students in their Final Degree Projects named "*Recommender system of banking products*" and "*Robo-Advisor Application*".

To conclude this section, I am in the need to specify that this is not the final version of the package, this is just a beta version of it that will keep going while I develop a consistent Python package for financial data extraction.

## Installation

In order to get this package working you will need to install [**investpy**](https://pypi.org/project/investpy/) from PyPi via Terminal typing:

``pip install investpy==0.8.5``

All the dependencies are already listed on the setup file of the package, but to sum them up, you will need the following requirements:

* [**pandas 0.24.2**](https://pypi.org/project/pandas/)
* [**requests 2.22.0**](https://pypi.org/project/requests/)
* [**lxml 4.3.3**](https://pypi.org/project/lxml/)
* [**unidecode 1.0.23**](https://pypi.org/project/unidecode/)

## Documentation

[investpy - Read the Docs](https://investpy.readthedocs.io/en/latest/)

## Contribute to investpy - [![Open Source Helpers](https://www.codetriage.com/alvarob96/investpy/badges/users.svg)](https://www.codetriage.com/alvarob96/investpy)

As this is an open source project it is open to contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas.

Also there is an open tab of [issues](https://github.com/alvarob96/investpy/issues) where anyone can contribute opening new issues if needed or navigate through them in order to solve them or contribute to its solving.

Additionally, you can triage issues on [investpy CodeTriage](https://www.codetriage.com/alvarob96/investpy) so you can provide issues so the package can grow and improve as the issues solves bugs, problems or needs, and maybe provide new ideas to improve package functionality and efficiency.

Feel free to contact package administrator via [email](alvarob96@usal.es)!

## License

[MIT License](https://github.com/alvarob96/investpy/blob/master/LICENSE)

## Additional Information

The package is currently in a development version, so please, if needed open an [issue](https://github.com/alvarob96/investpy/issues) to solve all the possible problems the package may be causing
so I fix them as fast as I can. Also, any new ideas or proposals are welcome, and I will gladly implement them in the package if the are positive and useful.

For further information or any question feel free to contact me via email at alvarob96@usal.es

You can also check my [Medium Publication](https://medium.com/research-studies-by-alvaro-bartolome/investpy-a-python-library-for-historical-data-extraction-from-the-spanish-stock-market-ad4d564dbfc5), where I upload weekly posts related to Data Science and some of them explain investpy functions and development in a deeper way.

## Disclaimer

This Python Package has been made for research purposes in order to fit a needs that Investing.com does not cover, so this package works like an Application Programming Interface (API) of Investing.com developed in an altruistic way. Conclude that this package is not related in any way with Investing.com or any dependant company, the only requirement for developing this package was to mention the source where data is retrieved.