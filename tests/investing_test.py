#!/usr/bin/env python

import pytest

import investing_scrapper

investing_scrapper.get_recent_data(ticker='bbva')
investing_scrapper.get_historical_data(ticker='bbva', start='10/10/2018', end='10/12/2018')