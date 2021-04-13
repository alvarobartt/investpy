Introduction
============

investpy is a Python package developed in order to retrieve all the available historical data from stocks/stocks,
funds and ETFs from Investing.com. As Investing.com does not have any API to retrieve historical data, the main goal
of this package is to allow users retrieve information from all the available financial products.

investpy came to life due to the need of covering the existing shortcomings in terms of real time data retrieval from
stocks of the companies that make up the Spanish Stock Market, until the date there was no other package that provided
a data extraction model for stocks from the Spanish Stock Market.

As time passed by, a decision was made on how investpy could be improved, and as the package was expected to have a high
scalability and thus cover all the data possibilities offered by Investing.com to the public, investpy is now trying to
expand the data it retrieves to make it more useful.

Along this document some relevant features of `investpy <https://pypi.org/project/investpy/>`_ are going to be
sorted out and its functions are going to be explained in order to clarify its use.

Getting Started
---------------

.. note::
    In order to get started using `investpy <https://pypi.org/project/investpy/>`_ you will need to have it installed, so
    if you do not have it already, check :ref:`installation-label`.

Once you have `investpy <https://pypi.org/project/investpy/>`_ installed, you can now proceed to use the package. The
first step is importing it at the top of your Python file as::

    import investpy

Currently the main functions of `investpy <https://pypi.org/project/investpy/>`_ support historical data retrieval
of stocks, funds and ETFs from all around the world (as indexed in Investing.com). Additionally to
historical data retrieval, investpy also offers additional data retrieval related to the indexed financial products.

In order to clarify this concepts, some investpy functions are going to be presented, even though all of them
are going to be properly explained and sorted out on their respective appendix in the documentation or in the API
Reference. For example, a block of code in order to get to test investpy usage is presented::

    import investpy


    # Retrieve all the available stocks as a Python list
    stocks = investpy.get_stocks_list()

    # Retrieve the recent historical data (past month) of a stock as a pandas.DataFrame on ascending date order
    df = investpy.get_stock_recent_data(stock='bbva', country='spain', as_json=False, order='ascending')

    # Retrieve the company profile of the introduced stock on english
    profile = investpy.get_stock_company_profile(stock='bbva', country='spain', language='english')


Data Source
-----------

`Investing.com <https://www.investing.com/>`_ is the main data source from which investpy retrieves the data. Investing.com is a
global financial portal and Internet brand owned by Fusion Media Ltd. which provides news, analysis, streaming quotes,
charts, technical data and financial tools about the global financial markets.

So as, the decision of choosing Investing.com as the data source is based on its reliability and also because it is one of
the few web pages that provide detailed data from spanish markets, as it was the main focus when determining to
develop the package as explained previously.