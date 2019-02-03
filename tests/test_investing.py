import pytest
import investing_scrapper


def test_investing():
    investing_scrapper.get_recent_data(equity='BBVA')
    investing_scrapper.get_historical_data(equity='BBVA', start='30/10/2018', end='30/12/2018')
    investing_scrapper.get_fund_recent_data(fund='Bankia Soy Asi Cauto FI')
    investing_scrapper.get_fund_historical_data(fund='Bankia Soy Asi Cauto FI', start='30/10/2018', end='30/12/2018')