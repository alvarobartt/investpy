import pytest
import investing_scrapper


def test_investing():
    investing_scrapper.get_recent_data(equity='bbva')
    investing_scrapper.get_historical_data(equity='bbva', start='10/10/2018', end='10/12/2018')