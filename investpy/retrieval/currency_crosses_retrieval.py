#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import operator

import pandas as pd
import pkg_resources

import requests
from lxml.html import fromstring

from investpy.utils import user_agent as ua


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

    resource_package = 'investpy'
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

    resource_package = 'investpy'
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

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'currency_crosses', 'currency_cross_continents.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(countries)
    df.to_csv(file_, index=False)

    return df
