import pytest
import investpy as invest


def test_investing():
    """
    This function checks that all the main functions of investpy work properly.
    """

    invest.get_recent_data(equity='bbva', as_json=True, order='ascending')
    # invest.get_historical_data(equity='bbva', start='30/10/2018', end='30/12/2018', as_json=False, order='ascending')
    # invest.get_fund_recent_data(fund='BBVA Multiactivo Conservador PP', as_json=False, order='ascending')
    # invest.get_fund_historical_data(fund='BBVA Multiactivo Conservador PP', start='30/10/2018', end='30/12/2018', as_json=False, order='ascending')
