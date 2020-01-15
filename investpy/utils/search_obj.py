#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
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
    """Class which contains each search result when searching data in Investing.
    
    This class contains the search results of the Investing.com search made with the function
    call `investpy.search(text)` which returns a :obj:`list` of instances of this class
    with the formatted retrieved information. Additionally, data can either be retrieved or not
    including both recent and historical data, which will be included in the `SearchObj.data` 
    attribute when calling either `SearchObj.retrieve_recent_data()` or 
    `SearchObj.retrieve_historical_data(from_date, to_date)`, respectively.

    Attributes:
        id_ (:obj:`int`): ID value used by Investing to retrieve data.
        name (:obj:`str`): name of the retrieved financial product.
        symbol (:obj:`str`): symbol of the retrieved financial product.
        tag (:obj:`str`): tag (which is the Investing URL) of the retrieved financial product.
        country (:obj:`str`): name of the country from where the retrieved financial product is.
        pair_type (:obj:`str`): type of retrieved financial product (equities, fund, etf, etc.).
        exchange (:obj:`str`): name of the stock exchange of the retrieved financial product.
        data (:obj:`pandas.DataFrame`, optional): 
            recent or historical data to retrieve from the current financial product.

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
        """Class method used to retrieve the recent data from the class instance of any financial product.
        
        This method retrieves the recent data from Investing of the financial product of the current class
        instance, so it fills the `SearchObj.data` attribute with the retrieved :obj:`pandas.DataFrame`. This method
        uses the previously filled data from the `investpy.search(text)` function search results to build the
        request that it is going to be sent to Investing so to retrieve and parse the data.

        Returns:
            :obj:`pandas.DataFrame` - data:
                This method retrieves the recent data from the current class instance of a financial product
                from Investing.com. This method both stores retrieved data in self.data attribute of the class 
                instance and it also returns it as a normal function will do.

        Note:
            Some financial products may not be available since its retrieval has not been developed.

        """

        if self.pair_type in ['equities', 'fund', 'etf', 'currency', 'certificate']:
            header = self.symbol + ' Historical Data'
            head, params = self._prepare_request(header)
        elif self.pair_type in ['bond']:
            header = self.name + ' Bond Yield Historical Data'
            head, params = self._prepare_request(header)
        elif self.pair_type in ['indice', 'commodity', 'crypto', 'fxfuture']:
            header = self.name + ' Historical Data'
            head, params = self._prepare_request(header)

        try:
            self.data = self._data_retrieval(product=self.pair_type, head=head, params=params)
            return self.data
        except:
            self.data = None
            return self.data

    def retrieve_historical_data(self, from_date, to_date):
        """Class method used to retrieve the historical data from the class instance of any financial product.
        
        This method retrieves the historical data from Investing of the financial product of the current class
        instance on the specified date range, so it fills the `SearchObj.data` attribute with the retrieved 
        :obj:`pandas.DataFrame`. This method uses the previously filled data from the `investpy.search(text)` 
        function search results to build the request that it is going to be sent to Investing so to retrieve 
        and parse the data.

        Returns:
            :obj:`pandas.DataFrame` - data:
                This method retrieves the historical data from the current class instance of a financial product
                from Investing.com. This method both stores retrieved data in self.data attribute of the class 
                instance and it also returns it as a normal function will do.

        Note:
            Some financial products may not be available since its retrieval has not been developed.

        Args:
            from_date (:obj:`str`): date from which data will be retrieved, specified in dd/mm/yyyy format.
            to_date (:obj:`str`): date until data will be retrieved, specified in dd/mm/yyyy format.
        
        """

        try:
            datetime.strptime(from_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'.")

        try:
            datetime.strptime(to_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

        from_date = datetime.strptime(from_date, '%d/%m/%Y')
        to_date = datetime.strptime(to_date, '%d/%m/%Y')

        if from_date >= to_date:
            raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

        if self.pair_type in ['equities', 'fund', 'etf', 'currency', 'certificate']:
            header = self.symbol + ' Historical Data'
        elif self.pair_type in ['bond']:
            header = self.name + ' Bond Yield Historical Data'
        elif self.pair_type in ['indice', 'commodity', 'crypto', 'fxfuture']:
            header = self.name + ' Historical Data'

        if to_date.year - from_date.year > 20:
            intervals = self._calculate_intervals(from_date, to_date)

            result = list()

            for interval in intervals['intervals']:
                head, params = self._prepare_historical_request(header=header, from_date=interval['from'], to_date=interval['to'])
                try:
                    res = self._data_retrieval(product=self.pair_type, head=head, params=params)
                    result.append(res)
                except:
                    continue

            if len(result) < 1:
                self.data = None
            else:
                self.data = pd.concat(result)
        else:
            head, params = self._prepare_historical_request(header=header, from_date=from_date.strftime('%d/%m/%Y'), to_date=to_date.strftime('%d/%m/%Y'))
            try:
                self.data = self._data_retrieval(product=self.pair_type, head=head, params=params)
            except:
                self.data = None

        return self.data

    def _prepare_request(self, header):
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

    def _calculate_intervals(self, from_date, to_date):
        date_interval = {
            'intervals': [],
        }

        flag = True

        while flag is True:
            diff = to_date.year - from_date.year

            if diff > 19:
                obj = {
                    'from': from_date.strftime('%m/%d/%Y'),
                    'to': from_date.replace(year=from_date.year + 19).strftime('%m/%d/%Y'),
                }

                date_interval['intervals'].append(obj)

                from_date = from_date.replace(year=from_date.year + 19)
            else:
                obj = {
                    'from': from_date.strftime('%m/%d/%Y'),
                    'to': to_date.strftime('%m/%d/%Y'),
                }

                date_interval['intervals'].append(obj)

                flag = False
        
        return date_interval
    

    def _data_retrieval(self, product, head, params):
        if product in ['equities', 'indice', 'fxfuture']:
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
                    val = nested_.get('data-real-value')
                    if val is None and nested_.text_content() == 'No results found':
                        raise IndexError("ERR#0033: information unavailable or not found.")
                    info.append(val)

                date_ = datetime.strptime(str(datetime.fromtimestamp(int(info[0])).date()), '%Y-%m-%d')
                
                close_ = float(info[1].replace(',', ''))
                open_ = float(info[2].replace(',', ''))
                high_ = float(info[3].replace(',', ''))
                low_ = float(info[4].replace(',', ''))

                volume_ = None
                
                if has_volume is True:
                    volume_ = int(info[5])

                result.insert(len(result),
                              Data(date_, open_, high_, low_, close_, volume_, None))

            result = result[::-1]

            df = pd.DataFrame.from_records([value.unknown_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df
