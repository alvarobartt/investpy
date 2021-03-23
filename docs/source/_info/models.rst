Models
======

Data Model
----------

As the retrieved historical data is common to every financial product that investpy extracts data from, only a model
class has been created in order to store the day-a-day historical data.

So in we define a model in where every value corresponds to each value of the OHLC (Open-High-Low-Close) nomenclature
(except on stocks, that it also includes the volume) and it looks like::

    def __init__(self, date_, open_, high_, low_, close_, volume_, currency_):
        self.date = date_
        self.open = open_
        self.high = high_
        self.low = low_
        self.close = close_
        self.volume = volume_
        self.currency_ = currency_


As their names indicate, OHLC values refer to opening, highest, lowest and closing values of the market on a trading
day, respectively. And the volume value refers to the number of shares traded in a security day.


.. note::

    The Data model is not usable as it is just a class used for the inner package, transparent to the user. It is used
    in order to categorize each retrieved value from Investing.com and then to define its structure and, so on, the
    structure that either the resulting pandas.DataFrame or JSON file will be based on.

Search Model
------------

TODO