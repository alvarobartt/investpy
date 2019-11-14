#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import requests
from lxml.html import fromstring
import pandas as pd

import json
from datetime import datetime, date
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
            head, params = self._prepare_request(header)
        elif self.pair_type in ['bond']:
            header = self.name + ' Bond Yield Historical Data'
            head, params = self._prepare_request(header)
        elif self.pair_type in ['indice']:
            header = self.name + ' Historical Data'
            head, params = self._prepare_request(header)
        elif self.pair_type in ['certificate', 'commodity', 'crypto', 'fxfuture']:
            self.data = None
            return None

        self.data = self._data_retrieval(product=self.pair_type, head=head, params=params)

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

    def _data_retrieval(self, product, head, params):
        """
        This method ...
        """

        if product in ['equities', 'indice', 'currency']:
            has_volume = True
        else:
            has_volume = False

        url = "https://www.investing.com/instruments/HistoricalDataAjax"

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()

        if path_:
            for elements_ in path_:
                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get('data-real-value'))

                if info[0] == 'No results found':
                    raise IndexError("ERR#0033: information unavailable or not found.")

                date_ = datetime.fromtimestamp(int(info[0]))
                date_ = date(date_.year, date_.month, date_.day)
                
                close_ = float(info[1])
                open_ = float(info[2])
                high_ = float(info[3])
                low_ = float(info[4])

                volume_ = None
                
                if has_volume is True:
                    if info[5].__contains__('K'):
                        volume_ = int(float(info[5].replace('K', '').replace(',', '')) * 1e3)
                    elif info[5].__contains__('M'):
                        volume_ = int(float(info[5].replace('M', '').replace(',', '')) * 1e6)
                    elif info[5].__contains__('B'):
                        volume_ = int(float(info[5].replace('B', '').replace(',', '')) * 1e9)

                result.insert(len(result),
                              Data(date_, open_, high_, low_, close_, volume_, None))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.unknown_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
