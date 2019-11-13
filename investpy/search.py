#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import requests

import re

from investpy.utils.search_obj import SearchObj
from investpy.utils.user_agent import get_random


def search_text(query):
    """
    This function ...
    """

    params = {
        'search_text': query,
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
        raise ValueError("ERR#0000: no results found on Investing for the introduced query.")

    search_results = list()
    
    for quote in data['quotes']:
        country = quote['flag'].lower()
        country = country if country not in ['usa', 'uk'] else 'united states' if country == 'usa' else 'united kingdom'

        tag = re.sub('\/(.*?)\/', '', quote['link'])

        search_results.append(SearchObj(id_=quote['pairId'], name=quote['name'], symbol=quote['symbol'],
                                        country=country, tag=tag, pair_type=quote['pair_type'], exchange=quote['exchange']))

    return search_results