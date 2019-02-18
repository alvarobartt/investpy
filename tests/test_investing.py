import pytest
import investpy


def test_investing():
    investpy.get_recent_data(equity='bbva')
    investpy.get_historical_data(equity='bbva', start='30/10/2018', end='30/12/2018')
    """
    investpy.get_fund_recent_data(fund='Bankia Soy Asi Cauto FI')
    investpy.get_fund_historical_data(fund='Bankia Soy Asi Cauto FI', start='30/10/2018', end='30/12/2018')
    """