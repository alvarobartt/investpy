#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"


# TODO: all lower case in objects to access it via dot operator (.)
#  look for a proper justification of it

class Data(object):
    """
    A class used to store the historical data of an equity, fund or etf

    Attributes
    ----------
    date_: str
        a string that stores the date in dd/mm/yyyy format
    open_, high_, low_, close_: float
        all the price values of an equity, fund or etf on the selected date
    volume_: long
        all the stocks sold on the selected date

    Methods
    -------
    equity_to_dict()
        converts the equity object into a dictionary
    equity_as_json()
        converts the equity object into a JSON object
    fund_to_dict()
        converts the fund object into a dictionary
    fund_as_json()
        converts the fund object into a JSON object
    etf_to_dict()
        converts the etf object into a dictionary
    etf_as_json()
        converts the etf object into a JSON object
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
        return {self.date.strftime('%Y/%m/%d'): {
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
        }}

    def fund_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
        }

    def fund_as_json(self):
        return {self.date.strftime('%d/%m/%Y'): {
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
        }}

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
