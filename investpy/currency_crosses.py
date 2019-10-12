#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import json
import operator

import pandas as pd
import pkg_resources

import numpy as np

import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_currency_crosses(test_mode=False):
    """
    This function retrieves all the available `currency_crosses` indexed on Investing.com, so to retrieve data from
    them which will be used later for inner functions for data retrieval. Additionally, when currency crosses are
    retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame` and stored on a CSV file on a
    package folder containing all the available resources. Note that maybe some of the information contained in the
    resulting :obj:`pandas.DataFrame` is useless as it is just used for inner function purposes. All the currency
    crosses available can be found at: https://es.investing.com/currencies/ plus the name of the country

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - currency_crosses:
            The resulting :obj:`pandas.DataFrame` contains all the currency crosses meta-information if found, if not,
            an empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of currencies was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                name | full_name | tag | id | base | second | base_name | second_name
                -----|-----------|-----|----|------|--------|-----------|-------------
                xxxx | xxxxxxxxx | xxx | xx | xxxx | xxxxxx | xxxxxxxxx | xxxxxxxxxxx

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        FileNotFoundError: raised if `currency_crosses.csv` file does not exists or is empty.
        ConnectionError: raised if GET requests did not return 200 status code.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_cross_continents.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        continents = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0048: currency_cross_continents.csv file not found")

    results = list()

    for continent in continents['tag'].tolist():
        head = {
            "User-Agent": ua.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/currencies/" + continent

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']")

        if path_:
            for elements_ in path_:
                for element_ in elements_.xpath(".//tbody/tr"):
                    for values in element_.xpath('.//a'):
                        tag_ = values.get('href')

                        if str(tag_).__contains__('/currencies/'):
                            tag_ = tag_.replace('//www.investing.com/currencies/', '')

                            name = values.text.strip()

                            if name in list(map(operator.itemgetter('name'), results)):
                                continue

                            base = name.split('/')[0]
                            second = name.split('/')[1]

                            info = retrieve_currency_cross_info(tag_)

                            if info is None:
                                continue

                            if info['second_name'].__contains__("..."):
                                info['second_name'] = info['full_name'].replace(name, '').\
                                    replace(info['base_name'], '').replace(' -  ', '')

                            data = {
                                'name': name,
                                'full_name': info['full_name'],
                                'tag': tag_,
                                'id': info['id'],
                                'base': base,
                                'base_name': info['base_name'],
                                'second': second,
                                'second_name': info['second_name'],
                            }

                            results.append(data)

                    if test_mode is True:
                        break
                if test_mode is True:
                    break
        if test_mode is True:
            break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df


def retrieve_currency_cross_info(tag):
    """
    This function retrieves additional information that should be included in every currency cross details such as the
    base currency name or the full name of the currency cross. Additionally, this function is intended to retrieve the
    id which will later be used when retrieving historical data from currency crosses since the id is required in the
    request headers. As Investing.com currency crosses listing has some minor mistakes, if the request errors with a
    404 code, the information won't be retrieved and so on the currency cross won't be added to the currency_crosses.csv
    file.

    Args:
        tag (:obj:`str`):
            is the tag of the currency cross to retrieve the information from, as indexed in Investing.com.

    Returns:
        :obj:`dict` - info:
            The resulting :obj:`dict` contains the needed information for the currency crosses listing. And the id of
            the currency cross which is required to send the request to Investing.com when it comes to historical data
            retrieval.

    Raises:
        ConnectionError: raised if GET requests does not return 200 status code.
    """

    url = "https://www.investing.com/currencies/" + tag

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head)

    if req.status_code == 404:
        return None
    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    result = {
        'id': None,
        'base_name': None,
        'second_name': None,
        'full_name': None
    }

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//div[contains(@class, 'instrumentHead')]/div/div[contains(@class, 'headBtnWrapper')]")

    for element_ in path_:
        result['id'] = element_.get('data-pair-id')

    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for element_ in path_:
        if element_.xpath("span[not(@class)]")[0].text_content().__contains__('Base'):
            result['base_name'] = element_.xpath("span[@class='elp']")[0].text_content().rstrip()
        elif element_.xpath("span[not(@class)]")[0].text_content().__contains__('Second'):
            result['second_name'] = element_.xpath("span[@class='elp']")[0].text_content().rstrip()

    path_ = root_.xpath(".//section[@id='leftColumn']/div[@class='instrumentHead']/h1")

    for element_ in path_:
        result['full_name'] = element_.text_content().rstrip()

    return result


def retrieve_currency_cross_continents():
    """
    This function retrieves all the continents/regions with available currency crosses as indexed in Investing.com, so
    on, this continent or region listing will be retrieved via Web Scraping from https://www.investing.com/currencies/.
    This listing will be used to retrieve all the currency crosses, because the retrieved tag for every country will be
    used to generate the URL to retrieve the data from.

    Returns:
        :obj:`pandas.DataFrame` - currency_cross_continents:
            The resulting :obj:`pandas.DataFrame` contains all the available continents/regions with their
            corresponding tag, which will be used later by investpy.

    Raises:
        ValueError: raised if any of the introduced arguments is not valid.
        ConnectionError: raised if connection to Investing.com could not be established.
        RuntimeError: raised if no countries were retrieved from Investing.com equity listing.
    """

    headers = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/currencies/'

    req = requests.get(url, headers=headers)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root = fromstring(req.text)
    path = root.xpath(".//div[@class='worldCurSimpleList']/ul/li")

    countries = list()

    for element in path:
        obj = {
            'country': element.xpath(".//a")[0].text_content().strip(),
            'tag': element.xpath(".//a")[0].get("href").replace('/currencies/', ''),
        }

        countries.append(obj)

    if len(countries) < 1:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_cross_continents.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)
    df.to_csv(file_, index=False)

    return df


def available_currencies_as_list():
    """
    This function retrieves a listing with all the available currencies with indexed currency crosses in order to
    get to know which are the available currencies. The currencies listed in this function, so on, can be used to
    search currency crosses and used the retrieved data to get historical data of those currency crosses, so to
    determine which is the value of one base currency in the second currency.

    Returns:
        :obj:`list` - available_currencies:
            The resulting :obj:`list` contains all the available currencies with currency crosses being either the base
            or the second value of the cross, as listed in Investing.com.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                available_currencies = [
                    'AED', 'AFN', 'ALL', 'AMD', 'ANG', ...
                ]

    Raises:
        IndexError: raised if `currency_crosses.csv` file was unavailable or not found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currency_crosses = retrieve_currency_crosses(test_mode=False)

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")
    else:
        return np.unique(currency_crosses['base'].unique().tolist() + currency_crosses['second'].unique().tolist())


def currency_crosses_as_df(base=None, second=None):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`pandas.DataFrame`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file. Note that the filtering params are both base and second, which mean the base and the
    second currency of the currency cross, for example, in the currency cross `EUR/USD` the base currency is EUR and
    the second currency is USD. These are optional parameters, so specifying one of them means that all the currency
    crosses where the introduced currency is either base or second will be returned; if both are specified,
    just the introduced currency cross will be returned if it exists. All the available currency crosses can be found
    at: https://es.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.

    Returns:
        :obj:`pandas.DataFrame` - currency_crosses_df:
            The resulting :obj:`pandas.DataFrame` contains all the currency crosses basic information retrieved from
            Investing.com, some of which is not useful for the user, but for the inner package functions, such as the
            `tag` or `id` fields.

            In case the information was successfully retrieved, the resulting :obj:`pandas.DataFrame` will look like::

                name | full_name | tag | id | base | second | base_name | second_name
                -----|-----------|-----|----|------|--------|-----------|-------------
                xxxx | xxxxxxxxx | xxx | xx | xxxx | xxxxxx | xxxxxxxxx | xxxxxxxxxxx

            Just like `investpy.currency_crosses.retrieve_currencies()`, the output of this function is a
            :obj:`pandas.DataFrame` containing all the currency crosses as indexed in Investing.com, but instead of
            scraping the web in order to retrieve them and then generating the CSV file, this function just reads it
            and loads it into a :obj:`pandas.DataFrame`.

    Raises:
        IOError: raised if currency_crosses retrieval failed, both for missing file or empty file.
    """

    if base is not None and not isinstance(base, str):
        raise ValueError("ERR#0049: specified base currency value is not valid.")

    if second is not None and not isinstance(second, str):
        raise ValueError("ERR#0051: specified second currency value is not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currency_crosses = retrieve_currency_crosses()

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    available_currencies = available_currencies_as_list()

    if base is None and second is None:
        currency_crosses.reset_index(drop=True, inplace=True)

        return currency_crosses
    elif base is not None:
        if unidecode.unidecode(base.upper()) in available_currencies:
            if second is not None:
                if unidecode.unidecode(second.upper()) in available_currencies:
                    currency_crosses = currency_crosses[
                        (currency_crosses['base'] == unidecode.unidecode(base.upper())) &
                        (currency_crosses['second'] == unidecode.unidecode(second.upper()))
                    ]
                    currency_crosses.reset_index(drop=True, inplace=True)

                    if len(currency_crosses) > 0:
                        return currency_crosses
                    else:
                        raise ValueError("ERR#0054: the introduced currency cross " + str(base) + "/" +
                                         str(second) + " does not exists.")
                else:
                    raise ValueError("ERR#0053: the introduced currency " + str(second) + " does not exists.")
            else:
                currency_crosses = currency_crosses[currency_crosses['base'] == unidecode.unidecode(base.upper())]
                currency_crosses.reset_index(drop=True, inplace=True)

                return currency_crosses
        else:
            raise ValueError("ERR#0053: the introduced currency " + str(base) + " does not exists.")
    elif second is not None:
        if unidecode.unidecode(second.upper()) in available_currencies:
            currency_crosses = currency_crosses[currency_crosses['second'] == unidecode.unidecode(second.upper())]
            currency_crosses.reset_index(drop=True, inplace=True)

            return currency_crosses
        else:
            raise ValueError("ERR#0053: the introduced currency " + str(second) + " does not exists.")


def currency_crosses_as_list(base=None, second=None):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`dict`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file is columns is None, otherwise, just the specified column values will be returned. Note
    that the filtering params are both base and second, which mean the base and the second currency of the currency
    cross, for example, in the currency cross `EUR/USD` the base currency is EUR and the second currency is USD. These
    are optional parameters, so specifying one of them means that all the currency crosses where the introduced
    currency is either base or second will be returned; if both are specified, just the introduced currency cross will
    be returned if it exists. All the available currency crosses can be found at: https://es.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.

    Returns:
        :obj:`list` - currency_crosses_list:
            The resulting :obj:`list` contains the retrieved data from the `currency_crosses.csv` file, which is
            a listing of the names of the currency crosses listed in Investing.com, which is the input for data
            retrieval functions as the name of the currency cross to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                currency_crosses_list = [
                    'USD/BRLT', 'CAD/CHF', 'CHF/CAD', 'CAD/PLN', 'PLN/CAD', ...
                ]

    Raises:
        IOError: raised if currency_crosses retrieval failed, both for missing file or empty file.
    """

    if base is not None and not isinstance(base, str):
        raise ValueError("ERR#0049: specified base currency value is not valid.")

    if second is not None and not isinstance(second, str):
        raise ValueError("ERR#0051: specified second currency value is not valid.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currency_crosses = retrieve_currency_crosses()

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    available_currencies = available_currencies_as_list()

    if base is None and second is None:
        currency_crosses.reset_index(drop=True, inplace=True)

        return currency_crosses['name'].tolist()
    elif base is not None:
        if unidecode.unidecode(base.upper()) in available_currencies:
            if second is not None:
                if unidecode.unidecode(second.upper()) in available_currencies:
                    currency_crosses = currency_crosses[
                        (currency_crosses['base'] == unidecode.unidecode(base.upper())) &
                        (currency_crosses['second'] == unidecode.unidecode(second.upper()))
                    ]
                    currency_crosses.reset_index(drop=True, inplace=True)

                    if len(currency_crosses) > 0:
                        return currency_crosses['name'].tolist()
                    else:
                        raise ValueError("ERR#0054: the introduced currency cross " + str(base) + "/" +
                                         str(second) + " does not exists.")
                else:
                    raise ValueError("ERR#0053: the introduced currency " + str(second) + " does not exists.")
            else:
                currency_crosses = currency_crosses[currency_crosses['base'] == unidecode.unidecode(base.upper())]
                currency_crosses.reset_index(drop=True, inplace=True)

                return currency_crosses['name'].tolist()
        else:
            raise ValueError("ERR#0053: the introduced currency " + str(base) + " does not exists.")
    elif second is not None:
        if unidecode.unidecode(second.upper()) in available_currencies:
            currency_crosses = currency_crosses[currency_crosses['second'] == unidecode.unidecode(second.upper())]
            currency_crosses.reset_index(drop=True, inplace=True)

            return currency_crosses['name'].tolist()
        else:
            raise ValueError("ERR#0053: the introduced currency " + str(second) + " does not exists.")


def currency_crosses_as_dict(base=None, second=None, columns=None, as_json=False):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`dict`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file is columns is None, otherwise, just the specified column values will be returned. Note
    that the filtering params are both base and second, which mean the base and the second currency of the currency
    cross, for example, in the currency cross `EUR/USD` the base currency is EUR and the second currency is USD. These
    are optional parameters, so specifying one of them means that all the currency crosses where the introduced
    currency is either base or second will be returned; if both are specified, just the introduced currency cross will
    be returned if it exists. All the available currency crosses can be found at: https://es.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.
        columns (:obj:`list`, optional):
            names of the columns of the equity data to retrieve <name, full_name, tag, id, base, base_name,
            second, second_name>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

    Returns:
        :obj:`dict` or :obj:`json` - currency_crosses_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'name': name,
                    'full_name': full_name,
                    'tag': tag,
                    'id': id,
                    'base': base,
                    'base_name': base_name,
                    'second': second,
                    'second_name': second_name
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
       IOError: raised if currency_crosses retrieval failed, both for missing file or empty file.
    """

    if base is not None and not isinstance(base, str):
        raise ValueError("ERR#0049: specified base currency value is not valid.")

    if second is not None and not isinstance(second, str):
        raise ValueError("ERR#0051: specified second currency value is not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        currency_crosses = retrieve_currency_crosses()

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    available_currencies = available_currencies_as_list()

    if columns is None:
        columns = currency_crosses.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in currency_crosses.columns.tolist() for column in columns):
        raise ValueError("ERR#0021: specified columns does not exist, available columns are "
                         "<name, full_name, tag, id, base, base_name, second, second_name>")

    if base is None and second is None:
        currency_crosses.reset_index(drop=True, inplace=True)

        if as_json:
            return json.dumps(currency_crosses[columns].to_dict(orient='records'))
        else:
            return currency_crosses[columns].to_dict(orient='records')
    elif base is not None:
        if unidecode.unidecode(base.upper()) in available_currencies:
            if second is not None:
                if unidecode.unidecode(second.upper()) in available_currencies:
                    currency_crosses = currency_crosses[
                        (currency_crosses['base'] == unidecode.unidecode(base.upper())) &
                        (currency_crosses['second'] == unidecode.unidecode(second.upper()))
                    ]
                    currency_crosses.reset_index(drop=True, inplace=True)

                    if len(currency_crosses) > 0:
                        if as_json:
                            return json.dumps(currency_crosses[columns].to_dict(orient='records'))
                        else:
                            return currency_crosses[columns].to_dict(orient='records')
                    else:
                        raise ValueError("ERR#0054: the introduced currency cross " + str(base) + "/" +
                                         str(second) + " does not exists.")
                else:
                    raise ValueError("ERR#0053: the introduced currency " + str(second) + " does not exists.")
            else:
                currency_crosses = currency_crosses[currency_crosses['base'] == unidecode.unidecode(base.upper())]
                currency_crosses.reset_index(drop=True, inplace=True)

                if as_json:
                    return json.dumps(currency_crosses[columns].to_dict(orient='records'))
                else:
                    return currency_crosses[columns].to_dict(orient='records')
        else:
            raise ValueError("ERR#0053: the introduced currency " + str(base) + " does not exists.")
    elif second is not None:
        if unidecode.unidecode(second.upper()) in available_currencies:
            currency_crosses = currency_crosses[currency_crosses['second'] == unidecode.unidecode(second.upper())]
            currency_crosses.reset_index(drop=True, inplace=True)

            if as_json:
                return json.dumps(currency_crosses[columns].to_dict(orient='records'))
            else:
                return currency_crosses[columns].to_dict(orient='records')
        else:
            raise ValueError("ERR#0053: the introduced currency " + str(second) + " does not exists.")
