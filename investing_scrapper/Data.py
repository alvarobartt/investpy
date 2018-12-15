#!/usr/bin/env python


class Data(object):
    def __init__(self, date_, close_, open_):
        self.date = date_
        self.close = close_
        self.open = open_

    def to_dict(self):
        return {
            'Date': self.date,
            'Close': self.close,
            'Open': self.open,
        }
