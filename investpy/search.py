#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import requests

import re

from investpy.utils.search_obj import SearchObj
from investpy.utils.user_agent import get_random


def search_text(text):
    """
    This function will use the Investing search engine so to retrieve the search results of the
    introduced text. This function will create a :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj`
    class instances which will contain the search results so that they can be easily accessed and so
    to ease the data retrieval process since it can be done calling the methods `.retrieve_recent_data()`
    or `.retrieve_historical_data(from_date, to_date)` from the class instance, which will fill the `data`
    attribute of that instance.

    Args:
        text (:obj:`str`): text to search in Investing among all its indexed data.

    Returns:
        :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj`:
            The resulting :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj` will contained the retrieved
            financial products matching the introduced text as indexed in Investing, if found. Note that if no
            information was found this function will raise a `ValueError` exception.

    Raises:
        ValueError: raised if either the introduced text is not valid or if no results were found for that text.
        ConnectionError: raised whenever the connection to Investing.com errored (did not return a 200 OK code).

    """

    if not text:
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if not isinstance(text, str):
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    params = {
        'search_text': text,
        'tab': 'quotes',
        'isFilter': False
    }

    head = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/search/service/SearchInnerPage'

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    data = req.json()

    if data['total']['quotes'] == 0:
        raise ValueError("ERR#0000: no results found on Investing for the introduced text.")

    search_results = list()
    
    for quote in data['quotes']:
        country = quote['flag'].lower()
        country = country if country not in ['usa', 'uk'] else 'united states' if country == 'usa' else 'united kingdom'

        tag = re.sub('\/(.*?)\/', '', quote['link'])

        search_results.append(SearchObj(id_=quote['pairId'], name=quote['name'], symbol=quote['symbol'],
                                        country=country, tag=tag, pair_type=quote['pair_type'], exchange=quote['exchange']))

    return search_results
