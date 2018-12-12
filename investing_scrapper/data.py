class Data(object):
    def __init__(self, date, close, open):
        self.date = date
        self.close = close
        self.open = open

    def to_dict(self):
        return {
            'Date': self.date,
            'Close': self.close,
            'Open': self.open,
        }
