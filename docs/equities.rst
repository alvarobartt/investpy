Stocks/Equities
===============

A stock (also known as "shares" or "equity) is a type of security that signifies proportionate ownership in the issuing
corporation. This entitles the stockholder to that proportion of the corporation's assets and earnings.

Stocks are bought and sold predominantly on stock exchanges, though there can be private sales as well, and are the
foundation of nearly every portfolio. These transactions have to conform to government regulations which are meant to
protect investors from fraudulent practices. Historically, they have outperformed most other investments over the long
run. These investments can be purchased from most online stock brokers.


Getting Started
---------------

To get started using `investpy <https://pypi.org/project/investpy/>`_ you first need to install it as described on
:ref:`installation-label`. Once you have it installed you can proceed to use it and retrieve data from stocks/equities,
after importing the package as it follows::

    $ import investpy

Listing
^^^^^^^

investpy offers some listing functions that allow the user to get the general information of the indexed stocks/equities
on `Investing <https://es.investing.com/>`_ as that information is already stored on CSV files generated automatically
on the package installation.

We can either retrieve the whole `pandas.DataFrame` containing all the information stored on the CSV file or a `list`
containing just the names of the stocks/equities, which are the input parameters to the data retrieval functions and so
on, the ones that are needed as input on the data retrieval functions.

.. code-block:: python

    # Retrieve all available stocks/equities information as a pandas.DataFrame
    equities_df = investpy.get_equities()
    # Retrieve a listing of all the available stock/equity names
    equities_list = investpy.get_equities_list()

.. note::

    The `pandas.DataFrame` contains internal package information that is probably useless for users, but it is provided
    anyways. On a future release stocks/equities listing functions will be improved in order to provide just useful data.

Recent & Historical Data
^^^^^^^^^^^^^^^^^^^^^^^^

The main functions of `investpy <https://pypi.org/project/investpy/>`_ refer to historical data extraction of
stocks/equities in this case. As the main functionality of the package is to retrieve historical data, some functions
have been developed in order to retrieve both recent and historical data between a date range.

So on an example is proposed in order to clarify the use of investpy for historical data retrieval::

    # Retrieves the recent data of BBVA (last month) as a pandas.DataFrame on ascending order
    df = investpy.get_recent_data(equity='bbva', as_json=False, order='ascending', debug=False)

    # Retrieves the historical data of BBVA on the specified date range as a pandas.DataFrame on ascending order
    df = investpy.get_historical_data(equity='bbva', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)

As we already saw, both functions take a lot of parameters, but some of them are *optional* which means that the function
does not need the user to specify them.

When retrieving recent data from an equity, we can additionally specify if we want the output as a json object or not, via
setting the parameter `as_json` on either *True* or *False*, respectively. We can also set the `order` we want the
returned object to have based on dates, where *ascending* goes from the very first date retrieved until now, and
*descending* goes the other way.

Furthermore when it comes to historical data retrieval we also need to specify both `start` and `end` dates, mandatory.
Where both date values are `str` objects as *dd/mm/yyyy* format, as it is the Spanish format to specify dates.

.. tip::

    If you are not familiar with stocks/equities remember that you can either retrieve a listing of the ones
    available or check the listing on `Investing Equities <https://es.investing.com/equities>`_.

Company Profile
^^^^^^^^^^^^^^^

As an extra feature, via `investpy <https://pypi.org/project/investpy/>`_ you can retrieve the company profile from a
company in order to either classify or analyse them based on the information these companies publicly provide, as it
is a self-made description of the company.

.. code-block:: python

    investpy.get_equity_company_profile(equity='bbva', country='spain', language='english')

Just the `equity` parameter is mandatory, as the default value for the `language` of the retrieved company profile is
*english* (due to `Investing <https://es.investing.com/>`_, as it just provides company profiles on english), but the
function also retrieves the company profile on *spanish* from
`Bolsa de Madrid <http://www.bolsamadrid.es/esp/aspx/Portada/Portada.aspx>`_, the additional resource used along this
package.

.. warning::

    This function is just available for spanish equities, since investpy was first created just for spanish equities,
    funds and ETFs retrieval. Future coverage for world equities company profiles is intended, but currently just the
    spanish ones are available.

Samples
-------

As the generated dataset has been uploaded to `Kaggle <https://www.kaggle.com/alvarob96/spanish-stocks-historical-data>`_
some kernels with samples on retrieved data usage have been created for the community.