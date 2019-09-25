#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources

import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_currency_crosses(test_mode=False):
    """
    This function retrieves all the available `currency crosses` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the currency crosses available can be found at: https://es.investing.com/currencies/. Additionally,
    when currency crosses are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - currencies:
            The resulting :obj:`pandas.DataFrame` contains all the currencies meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of currencies was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                country | name | full_name | tag | id
                --------|------|-----------|-----|----
                xxxxxxx | xxxx | xxxxxxxxx | xxx | xx

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        FileNotFoundError: raised if `index_countries.csv` file does not exists or is empty.
        ConnectionError: raised if GET requests did not return 200 status code.
        IndexError: raised if currencies information was unavailable or not found.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    results = list()

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    # url = "https://www.investing.com/currencies/single-currency-crosses"
    url = "https://www.investing.com/currencies/streaming-forex-rates-majors"

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='cr1']/tbody/tr")

    if path_:
        for elements_ in path_:
            id_ = elements_.get('id').replace('pair_', '')

            for element_ in elements_.xpath('.//a'):
                tag_ = element_.get('href')

                if str(tag_).__contains__('/currencies/'):
                    tag_ = tag_.replace('/currencies/', '')
                    full_name_ = element_.get('title').replace(' (CFD)', '').strip()
                    name = element_.text.strip()

                    data = {
                        'name': name,
                        'full_name': full_name_,
                        'tag': tag_,
                        'id': id_,
                    }

                    results.append(data)

            if test_mode is True:
                break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def currency_crosses_as_df():
    """
    This function retrieves all the available `currencies` from Investing.com and returns them as a :obj:`pandas.DataFrame`,
    which contains not just the index names, but all the fields contained on the currencies file.
    All the available currencies can be found at: https://es.investing.com/currencies/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available currencies from.

    Returns:
        :obj:`pandas.DataFrame` - currencies_df:
            The resulting :obj:`pandas.DataFrame` contains all the currencies basic information retrieved from Investing.com,
            some of which is not useful for the user, but for the inner package functions, such as the `tag` field,
            for example.

            In case the information was successfully retrieved, the :obj:`pandas.DataFrame` will look like::

                country | name | full_name | tag | id
                --------|------|-----------|-----|----
                xxxxxxx | xxxx | xxxxxxxxx | xxx | xx

            Just like `investpy.currencies.retrieve_currencies()`, the output of this function is a :obj:`pandas.DataFrame`,
            but instead of generating the CSV file, this function just reads it and loads it into a
            :obj:`pandas.DataFrame` object.

    Raises:
        IOError: raised if the currencies file from `investpy` is missing or errored.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currencies = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currencies = retrieve_currency_crosses()

    if currencies is None:
        raise IOError("ERR#0037: currencies not found or unable to retrieve.")

    return currencies


def currency_crosses_as_list():
    """
    This function retrieves all the available currencies and returns a list of each one of them.
    All the available currencies can be found at: https://es.investing.com/currencies/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available currencies from.

    Returns:
        :obj:`list` - currencies_list:
            The resulting :obj:`list` contains the retrieved data, which corresponds to the index names of
            every index listed on Investing.com.

            In case the information was successfully retrieved from the CSV file, the :obj:`list` will look like::

                currencies = [...]

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: raised if the currencies file from `investpy` is missing or errored.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currencies = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currencies = retrieve_currency_crosses()

    if currencies is None:
        raise IOError("ERR#0037: currencies not found or unable to retrieve.")

    return currencies['name'].tolist()


def currency_crosses_as_dict(columns=None, as_json=False):
    """
    This function retrieves all the available currencies on Investing.com and returns them as a :obj:`dict` containing the
    `country`, `name`, `full_name`, `symbol`, `tag` and `currency`. All the available currencies can be found at:
    https://es.investing.com/currencies/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available currencies from.
        columns (:obj:`list` of :obj:`str`, optional): description
            a :obj:`list` containing the column names from which the data is going to be retrieved.
        as_json (:obj:`bool`, optional): description
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - currencies_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'symbol': symbol,
                    'tag': tag
                }

    Raises:
        ValueError: raised when the introduced arguments are not correct.
        IOError: raised if the currencies file from `investpy` is missing or errored.
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currencies = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currencies = retrieve_currency_crosses()

    if currencies is None:
        raise IOError("ERR#0037: currencies not found or unable to retrieve.")

    if columns is None:
        columns = currencies.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in currencies.columns.tolist() for column in columns):
        raise ValueError("ERR#0023: specified columns does not exist, available columns are "
                         "<country, name, full_name, symbol, tag, currency>")

    if as_json:
        return json.dumps(currencies[columns].to_dict(orient='records'))
    else:
        return currencies[columns].to_dict(orient='records')
