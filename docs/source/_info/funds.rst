Funds
=====

A fund is a pool of money that is allocated for a specific purpose. A fund can be established for any purpose
whatsoever, whether it is a city government setting aside money to build a new civic center, a college setting
aside money to award a scholarship, or an insurance company setting aside money to pay its customers’ claims.

A fund is a pool of money set aside for a specific purpose, those pools can are often invested and professionally
managed and some common types of funds include pension funds, insurance funds, foundations, and endowments.

Individuals, businesses, and governments all use funds to set aside money. Individuals might establish an emergency
fund or rainy-day fund to pay for unforeseen expenses or a trust fund to set aside money for a specific person.

Source: *Investopedia*

Getting Started
---------------

To get started using `investpy <https://pypi.org/project/investpy/>`_ you first need to install it as described on
:ref:`installation-label`. Once you have it installed you can proceed to use it in order to retrieve data from
funds, after importing the package as it follows:

.. code-block:: python

    import investpy

Listing
^^^^^^^

`investpy <https://pypi.org/project/investpy/>`_ offers some listing functions that allow the user to get the general
information of the indexed funds on `Investing.com <https://www.investing.com/funds/>`_ as that information is already
stored on CSV files generated automatically on the package installation.

The user can either retrieve the whole :obj:`pandas.DataFrame` containing all the information stored on the CSV file, a
:obj:`list` containing just the names of the funds, which are the input parameters for the data retrieval functions; or
as a :obj:`dict` with all the available fields of information from the funds.

Also there is a param called ``country`` which by default is None, which means that the fund listing to be retrieved
will include all the available countries (indexed in Investing.com); on the contrary, if the param ``country`` is an
available country, the returned fund information will be filtered by country.

.. tip::

    To get a listing of all the available countries you can use the function ``investpy.get_fund_countries()`` which
    will return a :obj:`list` containing all the available country names which have funds as indexed on Investing.com.


.. code-block:: python

    # Retrieve all available funds information as a pandas.DataFrame
    funds_df = investpy.get_funds(country=None)
    # Retrieve a listing of all the available fund names
    funds_list = investpy.get_funds_list(country=None)
    # Retrieve a dictionary with all the funds and all of their information fields
    funds_dict = investpy.get_funds_dict(country=None)


.. note::

    The funds :obj:`pandas.DataFrame` contains internal package information that is useless for users, but it is provided
    anyways.

Since the data retrieval functions need both the fund name and the country from where that fund is, there is a function
to do so in order to let the user know which are the available countries and, so on, the available funds in those
countries. The functions presented below: `investpy.get_funds`, `investpy.get_funds_list` and `investpy.get_funds_dict`
have one optional parameter which is the country name so to retrieve just the :obj:`pandas.DataFrame`, :obj:`list` or
:obj:`dict` from all the available funds from the introduced country, respectively.

Anyways, before applying that filter, the use of the function `investpy.get_fund_countries` is proposed in order to
retrieve all the available countries which have funds.

.. code-block:: python

    countries = investpy.get_fund_countries()

    # Check if a country is either or not in the list & then get all the available funds from that country
    if 'spain' in countries:
        funds = investpy.get_funds_list(country='spain')

So on, every country listed on the previous listing can be used for filtering funds. Note that the country param is
needed in data retrieval functions since more than one fund can share the same name but not in the same country.

Fund Search
^^^^^^^^^^^

Before proceeding with the data retrieval functions an additional function is presented, since sometimes the user does
not have all the information for the fund to retrieve information from, so on, there is a function which allows the user
to search for funds with the specified value for the specified column/field. This function will return a `pandas.DataFrame`
with all the results found if they were found, if not, a `RuntimeError` will be raised.

Since the returned object is a `pandas.DataFrame` in the following example both the function usage and further data
handling is presented in order to let the user know hos to use the results of the search on the data retrieval functions
in order to make it more easy to use. Note that you can either select the value you are searching from the

.. code-block:: python

    search_result = investpy.search_funds(by='name', value='bbva')

    # Get both name and country via pandas.DataFrame index
    index = 0
    name = search_result.loc[index, 'name']
    country = search_result.loc[index, 'country']

    # Get both name and country via unique field such as isin
    isin = 'ES0113211835'
    name = search_result.loc[(search_result['isin'].str == isin).idxmax(), 'name']
    country = search_result.loc[(search_result['isin'].str == isin).idxmax(), 'country']

    # Or get it manually via printing the resulting pandas.DataFrame
    print(search_results)


Recent & Historical Data
^^^^^^^^^^^^^^^^^^^^^^^^

The main functions of `investpy <https://pypi.org/project/investpy/>`_ are focused on historical data extraction, and in
this concrete case, fund historical data retrieval functions will be explained and sorted out. As the main functionality
of the package is to retrieve data from Investing.com and format it so to access it via Python functions, some functions
have been developed in order to retrieve both recent and historical data.

As to explain its usage an example is proposed to explain how does historical data retrieval functions work::

    # Retrieves last month's data of 'Bankia Cauto Pp', which is a fund from 'Spain', as a pandas.DataFrame
    df = investpy.get_fund_recent_data(fund='Bankia Cauto Pp', country='spain')

    # Retrieves historical data of 'Bankia Cauto Pp', which is a fund from 'Spain', on the specified date range as a pandas.DataFrame
    df = investpy.get_fund_historical_data(fund='Bankia Cauto Pp', country='spain', from_date='01/01/2018', to_date='01/01/2019')

Both functions need some parameters, even though some of them are *optional*, which means that the function
does not need the user to specify them as they already have a default value.

Both parameters ``fund`` and ``country`` are mandatory, since they are the ones that specify which information should be
retrieved from Investing.com. Take into consideration that both parameters should match, which means that the name of
the fund should be a fund from the specified country, so if the introduced fund is not found on the specified country,
an error will be raised.

When retrieving recent data from a fund, we can additionally specify if we want the output as a json object or not, by
setting the parameter ``as_json`` as either True or False, respectively. We can also set the ``order`` we want the
returned object to have based on dates, where ascending goes from the very first date retrieved until now, and
descending goes the other way.

Furthermore, when it comes to historical data retrieval, we also need to specify both ``from_date`` and ``to_date``
values, as they are mandatory. Both date values are :obj:`str` formatted as *dd/mm/yyyy*.

.. tip::

    If you are not familiar with funds you can either retrieve a :obj:`list` of the ones available as provided by
    investpy or check the listing in `Investing.com Funds <https://www.investing.com/funds>`_.

Fund Information
^^^^^^^^^^^^^^^^

As an extra feature, via `investpy <https://pypi.org/project/investpy/>`_ you can retrieve information insights for the
specified fund on the specified country. This information is the one related to the introduced fund as indexed by
Investing.com which will give the user a wider sight on that concrete fund since values such as risk, rating or category
are provided by Investing.com and, so on, by investpy.

Its usage is pretty simple since just the `fund` and the `country` are mandatory parameters, but there is also an
additional parameter which is `as_json` that can be either True or False whether the information wants to be returned as
a :obj:`pandas.DataFrame` or a :obj:`json`.

.. code-block:: python

    # Retrieve information from the introduced fund in the specified country
    data = investpy.get_fund_information(fund='Bankia Cauto Pp', country='spain')

