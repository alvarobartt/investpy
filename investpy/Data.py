#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.


class Data(object):
    """
    This class is used to store the historical data of an equity, fund or ETF; and so on to store it
    as a JSON or as a Python :obj:`dict`.

    Args:
        date_ (:obj:`str`): date in dd/mm/yyyy format
        open_ (:obj:`float`): open value of the market on the introduced date
        high_ (:obj:`float`): highest value of the market on the introduced date
        low_ (:obj:`float`): lowest value of the market on the introduced date
        close_ (:obj:`float`): close value of the market on the introduced date
        volume_ (:obj:`long`): number of shares traded on the introduced date

    Attributes:
        date_ (:obj:`str`): date in dd/mm/yyyy format
        open_ (:obj:`float`): open value of the market on the introduced date
        high_ (:obj:`float`): highest value of the market on the introduced date
        low_ (:obj:`float`): lowest value of the market on the introduced date
        close_ (:obj:`float`): close value of the market on the introduced date
        volume_ (:obj:`long`): number of shares traded on the introduced date
    """

    def __init__(self, date_, open_, high_, low_, close_, volume_):
        self.date = date_
        self.open = open_
        self.high = high_
        self.low = low_
        self.close = close_
        self.volume = volume_

    def equity_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
        }

    def equity_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
        }

    def fund_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
        }

    def fund_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }

    def etf_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
        }

    def etf_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }
