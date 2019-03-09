#!/usr/bin/env python


class Data(object):
    """
    A class used to store the historical data of an equity, fund or etf

    Attributes
    ----------
    date_: str
        a string that stores the date in dd/mm/yyyy format
    close_, open_, max_, min_: float
        all the prices of an equity, fund or etf from the selected date
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
    """

    def __init__(self, date_, close_, open_, max_, min_, volume_):
        self.date = date_
        self.close = close_
        self.open = open_
        self.max = max_
        self.min = min_
        self.volume = volume_

    def equity_to_dict(self):
        return {
            'Date': self.date,
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
            'Volume': self.volume,
        }

    def equity_as_json(self):
        return {self.date.strftime('%d/%m/%Y'): {
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
            'Volume': self.volume,
        }}

    def fund_to_dict(self):
        return {
            'Date': self.date,
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
        }

    def fund_as_json(self):
        return {self.date.strftime('%d/%m/%Y'): {
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
        }}

    def etf_to_dict(self):
        return {
            'Date': self.date,
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
        }

    def etf_as_json(self):
        return {self.date.strftime('%d/%m/%Y'): {
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
        }}
