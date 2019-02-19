import pytest
import investpy


def test_investing():
    """
    This function checks that all the main functions of investpy work properly.
    """

    investpy.get_recent_data(equity='siemens gamesa')
    investpy.get_historical_data(equity='bbva', start='30/10/2018', end='30/12/2018')