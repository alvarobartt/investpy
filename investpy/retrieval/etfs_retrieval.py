#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring

from investpy.utils import user_agent as ua


def retrieve_etfs(test_mode=False):
    """
    This function retrieves all the available `world etfs` indexed on Investing.com, so to
    retrieve data from them which will be used later for inner functions for data retrieval.
    All the etfs available can be found at: https://es.investing.com/etfs/world-etfs. Additionally,
    when etfs are retrieved all the meta-information is both returned as a :obj:`pandas.DataFrame`
    and stored on a CSV file on a package folder containing all the available resources.
    Note that maybe some of the information contained in the resulting :obj:`pandas.DataFrame` is useless as it is
    just used for inner function purposes.

    Args:
        test_mode (:obj:`bool`):
            variable to avoid time waste on travis-ci since it just needs to test the basics in order to improve code
            coverage.

    Returns:
        :obj:`pandas.DataFrame` - etfs:
            The resulting :obj:`pandas.DataFrame` contains all the world etfs meta-information if found, if not, an
            empty :obj:`pandas.DataFrame` will be returned and no CSV file will be stored.

            In the case that the retrieval process of world etfs was successfully completed, the resulting
            :obj:`pandas.DataFrame` will look like::

                country | name | symbol | tag | id | currency
                --------|------|--------|-----|----|----------
                xxxxxxx | xxxx | xxxxxx | xxx | xx | xxxxxxxx

    Raises:
        ValueError: if any of the introduced arguments is not valid.
        FileNotFoundError: raised when `etf_countries.csv` file is missing.
        ConnectionError: if GET requests does not return 200 status code.
    """

    if not isinstance(test_mode, bool):
        raise ValueError('ERR#0041: test_mode can just be either True or False')

    head = {
        "User-Agent": ua.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'etfs', 'etf_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0044: etf_countries file not found")

    results = list()

    if test_mode is False:
        country_list = countries['country'].tolist()
    else:
        country_list = ['spain', 'usa']

    for country in country_list:
        url = "https://www.investing.com/etfs/" + country.replace(" ", "-") + "-etfs?issuer_filter=0"

        req = requests.get(url, headers=head)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//select[@name='asset_filter']/option")

        assets = list()

        if path_:
            for elements_ in path_:
                assets.append(elements_.get("value"))

        for asset in assets:
            url = "https://www.investing.com/etfs/" + country.replace(' ', '-') + "-etfs?asset=" \
                  + str(asset) + "&issuer_filter=0"

            req = requests.get(url, headers=head)

            if req.status_code != 200:
                raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

            root_ = fromstring(req.text)
            path_ = root_.xpath(".//table[@id='etfs']"
                                "/tbody"
                                "/tr")

            if path_:
                if len(path_) == 1000:
                    if test_mode is True:
                        url = 'https://www.investing.com/etfs/usa-etfs?&asset=1&issuer_filter=0'
                        req = requests.get(url, headers=head)

                    root_ = fromstring(req.text)
                    path_ = root_.xpath(".//select[@name='etf_filter']/optgroup")

                    etf_filters = list()

                    if path_:
                        for elements_ in path_:
                            element_ = elements_.xpath(".//option")
                            for value_ in element_:
                                etf_filters.append(value_.get("value"))

                        for etf_filter in etf_filters:
                            url = "https://www.investing.com/etfs/" + country.replace(' ', '-') + "-etfs?asset=" \
                                  + str(asset) + "&filter=" + str(etf_filter) + "&issuer_filter=0"

                            req = requests.get(url, headers=head)

                            if req.status_code != 200:
                                raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

                            root_ = fromstring(req.text)
                            path_ = root_.xpath(".//table[@id='etfs']"
                                                "/tbody"
                                                "/tr")

                            if path_:
                                for elements_ in path_:
                                    id_ = elements_.get('id').replace('pair_', '')
                                    symbol = elements_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

                                    nested = elements_.xpath(".//a")[0]
                                    tag = nested.get('href').replace('/etfs/', '')
                                    full_name = nested.get('title').rstrip()

                                    if not any(result['tag'] == tag for result in results):
                                        info = None

                                        while info is None:
                                            try:
                                                info = retrieve_etf_info(tag)
                                            except:
                                                pass

                                        data = {
                                            "country": 'united kingdom' if country == 'uk' else 'united states' if country == 'usa' else country,
                                            "name": nested.text.strip(),
                                            "full_name": full_name,
                                            "symbol": symbol,
                                            "tag": tag,
                                            "id": id_,
                                            "isin": info['isin'],
                                            "asset_class": info['asset_class'],
                                            "currency": info['currency'],
                                        }

                                        results.append(data)

                                        if test_mode is True:
                                            break

                            if test_mode is True:
                                break
                else:
                    if path_:
                        for elements_ in path_:
                            id_ = elements_.get('id').replace('pair_', '')
                            symbol = elements_.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

                            nested = elements_.xpath(".//a")[0]
                            tag = nested.get('href').replace('/etfs/', '')
                            full_name = nested.get('title').rstrip()

                            if not any(result['tag'] == tag for result in results):
                                info = None

                                while info is None:
                                    try:
                                        info = retrieve_etf_info(tag)
                                    except:
                                        pass

                                data = {
                                    "country": 'united kingdom' if country == 'uk' else 'united states' if country == 'usa' else country,
                                    "name": nested.text.strip(),
                                    "full_name": full_name,
                                    "symbol": symbol,
                                    "tag": tag,
                                    "id": id_,
                                    "isin": info['isin'],
                                    "asset_class": info['asset_class'],
                                    "currency": info['currency'],
                                }

                                results.append(data)

                                if test_mode is True:
                                    break

            if test_mode is True:
                break

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    file_ = pkg_resources.resource_filename(resource_package, resource_path)

    df = pd.DataFrame(results)

    if test_mode is False:
        df.to_csv(file_, index=False)

    return df


def retrieve_etf_info(tag):
    """
    This function retrieves additional information from the specified etf as indexed in Investing.com, in order to add
    more information to `etfs.csv` which can later be useful. Currently just the currency value is retrieved, since it
    is needed so to determine in which currency the historical data values are.

    Args:
       tag (:obj:`str`): is the tag of the etf to retrieve the information from as indexed by Investing.com.

    Returns:
       :obj:`dict` - info:
           The resulting :obj:`dict` contains the needed information for the etfs listing.

    Raises:
       ConnectionError: raised if GET requests does not return 200 status code.
       IndexError: raised if the information from the etf was not found or unable to retrieve.
    """

    url = "https://www.investing.com/etfs/" + tag

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
        'isin': None,
        'asset_class': None,
        'currency': None
    }

    root_ = fromstring(req.text)

    path_ = root_.xpath(".//div[contains(@class, 'overViewBox')]"
                        "/div[@id='quotes_summary_current_data']"
                        "/div[@class='right']"
                        "/div")

    for p in path_:
        if p.xpath("span[not(@class)]")[0].text_content().__contains__('ISIN'):
            result['isin'] = p.xpath("span[@class='elp']")[0].get('title').rstrip()
            continue
        elif p.xpath("span[not(@class)]")[0].text_content().__contains__('Asset Class'):
            result['asset_class'] = p.xpath("span[@class='elp']")[0].get('title').rstrip().lower()
            continue

    path_ = root_.xpath(".//div[contains(@class, 'bottom')]"
                        "/span[@class='bold']")

    for element_ in path_:
        if element_.text_content():
            result['currency'] = element_.text_content()

    return result
