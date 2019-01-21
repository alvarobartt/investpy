#!/usr/bin/env python


class Data(object):
    def __init__(self, date_, close_, open_, max_, min_, volume_):
        self.date = date_
        self.close = close_
        self.open = open_
        self.max = max_
        self.min = min_
        self.volume = volume_

    def to_dict(self):
        return {
            'Date': self.date,
            'Close': self.close,
            'Open': self.open,
            'Max': self.max,
            'Min': self.min,
            'Volume': self.volume,
        }
