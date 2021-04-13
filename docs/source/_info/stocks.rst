Stocks/Equities
===============

A **stock** (also known as "shares" or "equities") is a type of security that signifies proportionate ownership in the
issuing corporation. This entitles the stockholder to that proportion of the corporation's assets and earnings.

Stocks are bought and sold predominantly on stock exchanges, though there can be private sales as well, and are the
foundation of nearly every portfolio. These transactions have to conform to government regulations which are meant to
protect investors from fraudulent practices. Historically, they have outperformed most other investments over the long
run. These investments can be purchased from most online stock brokers.

Source: *Investopedia*

Getting Started
---------------

To get started using `investpy <https://pypi.org/project/investpy/>`_ you first need to install it as described on
:ref:`installation-label`. Once you have it installed you can proceed to use it in order to retrieve data from
stocks, after importing the package as it follows:

.. code-block:: python

    import investpy

Listing
^^^^^^^

`investpy <https://pypi.org/project/investpy/>`_ offers some listing functions that allow the user to get the general
information of the indexed stocks on `Investing.com <https://www.investing.com/>`_ as that information is already
stored on CSV files generated automatically on the package installation.

We can either retrieve the whole :obj:`pandas.DataFrame` containing all the information stored on the CSV file or a
:obj:`list` containing just the symbols of the stocks, which are the input parameters for the data retrieval functions.

Also there is a param called ``country`` which by default is None, which means that the stock listing to be retrieved
will include all the available countries (indexed in Investing.com); on the contrary, if the param ``country`` is an
available country, the returned stock information will be filtered by country.

.. tip::

    To get a listing of all the available countries you can use the function ``investpy.get_stock_countries()`` which
    will return a :obj:`list` containing all the available country names which have stocks as indexed on Investing.com.


.. code-block:: python

    # Retrieve all available stocks information as a pandas.DataFrame
    stocks_df = investpy.get_stocks(country=None)
    # Retrieve a listing of all the available stock symbols
    stocks_list = investpy.get_stocks_list(country=None)

Recent & Historical Data
^^^^^^^^^^^^^^^^^^^^^^^^

The main functions of `investpy <https://pypi.org/project/investpy/>`_ are focused on historical data extraction,
stocks in this case. As the main functionality of the package is to retrieve data from Investing.com, so on,
some functions have been developed in order to retrieve both recent and historical data.

As to explain its usage an example is proposed to present historical data retrieval functions::

    # Retrieves the recent data of BBVA (last month) a spanish stock, as a pandas.DataFrame on ascending order
    df = investpy.get_stock_recent_data(stock='bbva', country='spain', as_json=False, order='ascending')

    # Retrieves the historical data of BBVA, a spanish stock, on the specified date range as a pandas.DataFrame on ascending order
    df = investpy.get_stock_historical_data(stock='bbva', country='spain', from_date='01/01/2018', to_date='01/01/2019', as_json=False, order='ascending')

As we already saw, both functions take some parameters, but some of them are *optional*, which means that the function
does not need the user to specify them as they already have a default value.

Both parameters ``stock`` and ``country`` are mandatory, since they are the ones that specify which information should be
retrieved from Investing.com. Consider that both parameters should match, which means that the symbols of the stock should
be an stock from the specified country, if the stock is not found on the specified country, an error will be raised.

When retrieving recent data from an stock, we can additionally specify if we want the output as a json object or not, by
setting the parameter ``as_json`` as either True or False, respectively. We can also set the ``order`` we want the
returned object to have based on dates, where ascending goes from the very first date retrieved until now, and
descending goes the other way.

Furthermore, when it comes to historical data retrieval, we also need to specify both ``from_date`` and ``to_date``
values, as they are mandatory. Both date values are :obj:`str` formatted as *dd/mm/yyyy*.

.. tip::

    If you are not familiar with stocks you can either retrieve a listing of the ones
    available or check the one presented in `Investing.com Equities <https://www.investing.com/equities>`_.

Company Profile
^^^^^^^^^^^^^^^

As an extra feature, via `investpy <https://pypi.org/project/investpy/>`_ you can retrieve the company profile from a
company in order to either classify or analyse them based on the information these companies publicly provide, as it
is a self-made description of the company.

.. code-block:: python

    investpy.get_stock_company_profile(stock='bbva', country='spain', language='english')

As explained before, when it comes to data retrieval, both ``stock`` and ``country`` parameters are mandatory, and
should match; as the default value for the ``language`` of the retrieved company profile is *english* (as `Investing.com <https://www.investing.com/>`_
provides company profiles written in english), but besides that, the function
also retrieves the company profile on *spanish* from `Bolsa de Madrid <http://www.bolsamadrid.es/esp/aspx/Portada/Portada.aspx>`_,
which is the additional resource used along this package.

.. warning::

    This function is just available for spanish stocks, since `investpy <https://pypi.org/project/investpy/>`_ was
    first created just for Spanish Stocks, Funds and ETFs retrieval. Future coverage for world stocks company
    profiles is intended, but currently just the spanish ones are available.

Samples
-------

As the generated dataset has been uploaded to `Kaggle <https://www.kaggle.com/alvarob96/spanish-stocks-historical-data>`_
some kernels with samples on retrieved data usage have been created by the community.