#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.


class Data(object):
    """
    This class is used to store the historical data of an equity, fund or etf either as a :obj:`json` or as a
    :obj:`dict`.

    Args:
        date_ (:obj:`str`): date in dd/mm/yyyy format.
        open_ (:obj:`float`): open value of the market on the introduced date.
        high_ (:obj:`float`): highest value of the market on the introduced date.
        low_ (:obj:`float`): lowest value of the market on the introduced date.
        close_ (:obj:`float`): close value of the market on the introduced date.
        volume_ (:obj:`long`): number of shares traded on the introduced date.
        currency_ (:obj:`str`): currency in which the data is displayed.

    Attributes:
        date_ (:obj:`str`): date in dd/mm/yyyy format.
        open_ (:obj:`float`): open value of the market on the introduced date.
        high_ (:obj:`float`): highest value of the market on the introduced date.
        low_ (:obj:`float`): lowest value of the market on the introduced date.
        close_ (:obj:`float`): close value of the market on the introduced date.
        volume_ (:obj:`long`): number of shares traded on the introduced date.
        currency_ (:obj:`str`): currency in which the data is displayed.
    """

    def __init__(self, date_, open_, high_, low_, close_, volume_, currency_=None):
        self.date = date_
        self.open = open_
        self.high = high_
        self.low = low_
        self.close = close_
        self.volume = volume_
        self.currency = currency_

    def equity_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
            'Currency': self.currency,
        }

    def equity_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'currency': self.currency,
        }

    def fund_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Currency': self.currency,
        }

    def fund_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'currency': self.currency,
        }

    def etf_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Currency': self.currency,
        }

    def etf_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'currency': self.currency,
        }

    def index_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
            'Currency': self.currency,
        }

    def index_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'currency': self.currency,
        }

    def currency_cross_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
        }

    def currency_cross_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
        }
