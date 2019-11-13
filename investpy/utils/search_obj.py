#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import requests
from lxml.html import fromstring

import json
from random import randint

from investpy.utils.data import Data
from investpy.utils.user_agent import get_random


class SearchObj(object):
    """
    This class ...
    """

    def __init__(self, id_, name, symbol, tag, country, pair_type, exchange):
        self.id_ = id_
        self.name = name
        self.symbol = symbol
        self.country = country
        self.tag = tag
        self.pair_type = pair_type
        self.exchange = exchange

    def __str__(self):
        return json.dumps(self.__dict__)


    def retrieve_recent_data(self):
        """
        This method ...
        """

        if self.pair_type in ['equities', 'fund', 'etf', 'currency']:
            header = self.symbol + ' Historical Data'
            head, params = self._prepare_request(header, from_date, to_date)
            if self.pair_type == 'equities':
                self.data = None # Stock Retrieval Function
            elif self.pair_type == 'fund':
                self.data = None # Fund Retrieval Function
            elif self.pair_type == 'etf':
                self.data = None # ETF Retrieval Function
            elif self.pair_type == 'currency':
                self.data = None # Currency Retrieval Function
        elif self.pair_type in ['bond']:
            header = self.name + ' Bond Yield Historical Data'
            head, params = self._prepare_request(header, from_date, to_date)
            self.data = None # Bond Retrieval Function
        elif self.pair_type in ['indice']:
            header = self.name + ' Historical Data'
            head, params = self._prepare_request(header, from_date, to_date)
            self.data = None # Index Retrieval Function
        elif self.pair_type in ['certificate', 'commodity', 'crypto', 'fxfuture']:
            return None
            self.data = None

    def retrieve_historical_data(self, from_date, to_date):
        """
        This method ...
        """

        if self.pair_type in ['equities', 'fund', 'etf', 'currency']:
            header = self.symbol + ' Historical Data'
            head, params = self._prepare_historical_request(header, from_date, to_date)
            if self.pair_type == 'equities':
                self.data = None # Stock Retrieval Function
            elif self.pair_type == 'fund':
                self.data = None # Fund Retrieval Function
            elif self.pair_type == 'etf':
                self.data = None # ETF Retrieval Function
            elif self.pair_type == 'currency':
                self.data = None # Currency Retrieval Function
        elif self.pair_type in ['bond']:
            header = self.name + ' Bond Yield Historical Data'
            head, params = self._prepare_historical_request(header, from_date, to_date)
            self.data = None # Bond Retrieval Function
        elif self.pair_type in ['indice']:
            header = self.name + ' Historical Data'
            head, params = self._prepare_historical_request(header, from_date, to_date)
            self.data = None # Index Retrieval Function
        elif self.pair_type in ['certificate', 'commodity', 'crypto', 'fxfuture']:
            return None
            self.data = None

    def _prepare_request(self, header):
        """
        This method ...
        """

        head = {
            "User-Agent": get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        params = {
            "curr_id": self.id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        return head, params

    def _prepare_historical_request(self, header, from_date, to_date):
        """
        This method ...
        """

        head = {
            "User-Agent": get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        params = {
            "curr_id": self.id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": from_date,
            "end_date": to_date,
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        return head, params