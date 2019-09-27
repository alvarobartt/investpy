#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

import json
import time

import pandas as pd
import pkg_resources

import requests
import unidecode
from lxml.html import fromstring

from investpy import user_agent as ua


def retrieve_currency_crosses(test_mode=False):
    # """
    # This function retrieves all the available `currency_crosses` indexed on Investing.com, so to
    # retrieve data from them which will be used later for inner functions for data retrieval.
    # Additionally, when currency crosses are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    # and stored on a CSV file on a package folder containing all the available resources.
    # Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    # just used for inner function purposes. All the currency crosses available can be found at:
    # https://es.investing.com/currencies/ plus the name of the country
    #
    # Args:
    #     test_mode (:obj:`bool`):
    #         variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
    #         coverage.
    #
    # Returns:
    #     :obj:`pandas.DataFrame` - currencies:
    #         The resulting :obj:`pandas.DataFrame` contains all the currencies meta-information if found, if not, an
    #         empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.
    #
    #         In the case that the retrieval process of currencies was successfully completed, the resulting
    #         :obj:`pandas.DataFrame` will look like::
    #
    #             name | full_name | tag | id
    #             -----|-----------|-----|----
    #             xxxx | xxxxxxxxx | xxx | xx
    #
    # Raises:
    #     ValueError: raised if any of the introduced arguments is not valid.
    #     FileNotFoundError: raised if `currency_crosses.csv` file does not exists or is empty.
    #     ConnectionError: raised if GET requests did not return 200 status code.
    #     IndexError: raised if currencies information was unavailable or not found.
    # """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_cross_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0048: currency_cross_countries.csv file not found")

    results = list()

    for index, row in countries.iterrows():
        head = {
            "User-Agent": ua.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/currencies/" + row['tag']

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

                            base = None
                            second = None

                            if name.__contains__('/'):
                                base = name.split('/')[0]
                                second = name.split('/')[1]

                            try:
                                time.sleep(1.5)
                                info = retrieve_currency_cross_info(tag_)

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

                                print(data)

                                results.append(data)
                            except:
                                data = {
                                    'name': name,
                                    'full_name': None,
                                    'tag': tag_,
                                    'id': None,
                                    'base': '',
                                    'base_name': None,
                                    'second': '',
                                    'second_name': None,
                                }

                                print(data)

                                results.append(data)

                    if test_mode is True:
                        break
                if test_mode is True:
                    break
        if test_mode is True:
            break

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file, index=False)

    return df


def retrieve_currency_cross_info(tag):
    # """
    # This function retrieves both the ISIN code, the currency and the symbol of an equity indexed in Investing.com, so
    # to include additional information in `equities.csv` file. The ISIN code will later be used in order to retrieve more
    # information from the specified equity, as the ISIN code is an unique identifier of each equity; the currency
    # will be required in order to know which currency is the value in, and the symbol will be used for processing the
    # request to HistoricalDataAjax to retrieve historical data from Investing.com.
    #
    # Args:
    #     tag (:obj:`str`): is the tag of the equity to retrieve the information from as indexed by Investing.com.
    #
    # Returns:
    #     :obj:`dict` - info:
    #         The resulting :obj:`dict` contains the needed information for the equities listing, so on, the ISIN
    #          code of the introduced equity, the currency of its values and the symbol of the equity.
    #
    # Raises:
    #     ConnectionError: raised if GET requests does not return 200 status code.
    #     IndexError: raised if either the isin code or the currency were unable to retrieve.
    # """

    url = "https://www.investing.com/currencies/" + tag

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head)

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


def retrieve_currency_cross_countries():
    # """
    # This function retrieves all the country names indexed in Investing.com with available equities to retrieve data
    # from, via Web Scraping https://www.investing.com/equities/ where the available countries are listed, and from their
    # names the specific equity website of every country is retrieved in order to get the ID which will later be used
    # when retrieving all the information from the available equities in every country.
    #
    # Returns:
    #     :obj:`pandas.DataFrame` - equity_countries:
    #         The resulting :obj:`pandas.DataFrame` contains all the available countries with their corresponding ID,
    #         which will be used later by investpy.
    #
    # Raises:
    #     ValueError: raised if any of the introduced arguments is not valid.
    #     ConnectionError: raised if connection to Investing.com could not be established.
    #     RuntimeError: raised if no countries were retrieved from Investing.com equity listing.
    # """

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

        print(obj)

        countries.append(obj)

    if len(countries) < 1:
        raise RuntimeError('ERR#0035: no countries could be retrieved!')

    resource_package = __name__
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_cross_countries.csv'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)
    df.to_csv(file, index=False)

    return df


# def available_currencies():
#     return None
#
#
# def currency_crosses_as_df(currency=None):
#     """
#     This function retrieves all the available `currency_crosses` from Investing.com and returns them as a
#     :obj:`pandas.DataFrame`, which contains not just the currency crosses names, but all the fields contained on
#     the currency_crosses file. All the available currency crosses can be found at: https://es.investing.com/currencies/
#
#     Returns:
#         :obj:`pandas.DataFrame` - currency_crosses_df:
#             The resulting :obj:`pandas.DataFrame` contains all the currency crosses basic information retrieved from
#             Investing.com, some of which is not useful for the user, but for the inner package functions, such as the
#             `tag` or `id` fields.
#
#             In case the information was successfully retrieved, the resulting :obj:`pandas.DataFrame` will look like::
#
#                 name | full_name | base | second | tag | id
#                 -----|-----------|------|--------|-----|----
#                 xxxx | xxxxxxxxx | xxxx | xxxxxx | xxx | xx
#
#             Just like `investpy.currency_crosses.retrieve_currencies()`, the output of this function is a
#             :obj:`pandas.DataFrame` containing all the currency crosses as indexed in Investing.com, but instead of
#             scraping the web in order to retrieve them and then generating the CSV file, this function just reads it
#             and loads it into a :obj:`pandas.DataFrame`.
#
#     Raises:
#         IOError: raised if the currency_crosses file from `investpy` is missing or errored.
#     """
#
#     if currency is not None and not isinstance(currency, str):
#         raise ValueError("ERR#00xx: specified currency value not valid.")
#
#     resource_package = __name__
#     resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
#     if pkg_resources.resource_exists(resource_package, resource_path):
#         currency_crosses = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
#     else:
#         currency_crosses = retrieve_currency_crosses()
#
#     if currency_crosses is None:
#         raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")
#
#     if currency is None:
#         currency_crosses.reset_index(drop=True, inplace=True)
#
#         return currency_crosses
#     elif unidecode.unidecode(currency.lower()) in available_currencies():
#         currency_crosses = currency_crosses[currency_crosses['base'] == unidecode.unidecode(currency.lower()) or
#                                             currency_crosses['second'] == unidecode.unidecode(currency.lower())]
#         currency_crosses.reset_index(drop=True, inplace=True)
#
#         return currency_crosses
#
#
# def currency_crosses_as_list(currency=None):
#     """
#     This function retrieves all the available MAJOR currencies and returns a list of each one of them.
#     All the available currencies can be found at: https://es.investing.com/currencies/streaming-forex-rates-majors
#
#     Returns:
#         :obj:`list` - currencies_list:
#             The resulting :obj:`list` contains the retrieved data, which corresponds to the currency_crosses names of
#             every MAJOR currency_cross listed on Investing.com.
#
#             In case the information was successfully retrieved from the CSV file, the :obj:`list` will look like::
#
#                 currencies = [...]
#
#     Raises:
#         ValueError: raised when the introduced arguments are not correct.
#         IOError: raised if the currency_crosses file from `investpy` is missing or errored.
#     """
#
#     resource_package = __name__
#     resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
#     if pkg_resources.resource_exists(resource_package, resource_path):
#         currencies = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
#     else:
#         currencies = retrieve_currency_crosses()
#
#     if currencies is None:
#         raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")
#
#     return currencies['name'].tolist()
#
#
# def currency_crosses_as_dict(currency=None, columns=None, as_json=False):
#     """
#     This function retrieves all the available currencies on Investing.com and returns them as a :obj:`dict` containing the
#     `country`, `name`, `full_name`, `symbol`, `tag` and `currency`. All the available currencies can be found at:
#     https://es.investing.com/currencies/streaming-forex-rates-majors
#
#     Args:
#         columns (:obj:`list` of :obj:`str`, optional): description
#             a :obj:`list` containing the column names from which the data is going to be retrieved.
#         as_json (:obj:`bool`, optional): description
#             value to determine the format of the output data (:obj:`dict` or :obj:`json`).
#
#     Returns:
#         :obj:`dict` or :obj:`json` - currencies_dict:
#             The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
#             fields are filled with `None` values.
#
#             In case the information was successfully retrieved, the :obj:`dict` will look like::
#
#                 {
#                     'name': name,
#                     'full_name': full_name,
#                     'tag': tag,
#                     'id': id,
#                 }
#
#     Raises:
#         ValueError: raised when the introduced arguments are not correct.
#         IOError: raised if the currencies file from `investpy` is missing or errored.
#     """
#
#     if not isinstance(as_json, bool):
#         raise ValueError("ERR#0052: as_json argument can just be True or False, bool type.")
#
#     resource_package = __name__
#     resource_path = '/'.join(('resources', 'currency_crosses', 'currency_crosses.csv'))
#     if pkg_resources.resource_exists(resource_package, resource_path):
#         currencies = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
#     else:
#         currencies = retrieve_currency_crosses()
#
#     if currencies is None:
#         raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")
#
#     if columns is None:
#         columns = currencies.columns.tolist()
#     else:
#         if not isinstance(columns, list):
#             raise ValueError("ERR#0054: specified columns argument is not a list, it can just be list type.")
#
#     if not all(column in currencies.columns.tolist() for column in columns):
#         raise ValueError("ERR#0055: specified columns does not exist, available columns are "
#                          "<name, full_name, tag, id>")
#
#     if as_json:
#         return json.dumps(currencies[columns].to_dict(orient='records'))
#     else:
#         return currencies[columns].to_dict(orient='records')


# if __name__ == '__main__':
#     retrieve_currency_crosses()

