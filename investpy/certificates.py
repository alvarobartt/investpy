#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from datetime import datetime, date
import json
import re
from random import randint

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy.utils.user_agent import get_random
from investpy.utils.data import Data

from investpy.data.certificates_data import certificates_as_df, certificates_as_list, certificates_as_dict
from investpy.data.certificates_data import certificate_countries_as_list


def get_certificates(country=None):
    """
    This function retrieves all the data stored in `certificates.csv` file, which previously was retrieved from 
    Investing.com. Since the resulting object is a matrix of data, the certificate's data is properly structured 
    in rows and columns, where columns are the certificate data attribute names. Additionally, country
    filtering can be specified, which will make this function return not all the stored certificates, but just
    the data of the certificates from the introduced country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available certificates from.

    Returns:
        :obj:`pandas.DataFrame` - certificates_df:
            The resulting :obj:`pandas.DataFrame` contains all the certificate's data from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | full_name | symbol | issuer | isin | asset_class | underlying
                --------|------|-----------|--------|--------|------|-------------|------------
                xxxxxxx | xxxx | xxxxxxxxx | xxxxxx | xxxxxx | xxxx | xxxxxxxxxxx | xxxxxxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if certificates file was not found.
        IOError: raised when certificates file is missing or empty.

    """

    return certificates_as_df(country)


def get_certificates_list(country=None):
    """
    This function retrieves all the available etfs indexed on Investing.com, already stored on `etfs.csv`.
    This function also allows the users to specify which country do they want to retrieve data from or if they
    want to retrieve it from every listed country; so on, a listing of etfs will be returned. This function
    helps the user to get to know which etfs are available on Investing.com.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`list` - certificates_list:
            The resulting :obj:`list` contains the retrieved data from the `etfs.csv` file, which is
            a listing of the names of the etfs listed on Investing.com, which is the input for data
            retrieval functions as the name of the etf to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                certificates_list = ['SOCIETE GENERALE CAC 40 X10 31DEC99', 'COMMERZBANK SG 31Dec99', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if certificates file was not found.
        IOError: raised when certificates file is missing or empty.
    
    """

    return certificates_as_list(country)


def get_certificates_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available certificates indexed on Investing.com, stored on `certificates.csv`.
    This function also allows the user to specify which country do they want to retrieve data from, or from every 
    listed country; the columns which the user wants to be included on the resulting :obj:`dict`; and the output 
    of the function will either be a :obj:`dict` or a :obj:`json`.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available certificates from.
        columns (:obj:`list`, optional):
            names of the columns of the etf data to retrieve <country, name, full_name, symbol, issuer, isin, asset_class, underlying>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

    Returns:
        :obj:`dict` or :obj:`json` - etfs_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding fields are
            filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    "country": "france",
                    "name": "SOCIETE GENERALE CAC 40 X10 31DEC99",
                    "full_name": "SOCIETE GENERALE EFFEKTEN GMBH ZT CAC 40 X10 LEVERAGE 31DEC99",
                    "symbol": "FR0011214527",
                    "issuer": "Societe Generale Effekten GMBH",
                    "isin": "FR0011214527",
                    "asset_class": "index",
                    "underlying": "CAC 40 Leverage x10 NR"
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if certificates file was not found.
        IOError: raised when certificates file is missing or empty.
    
    """

    return certificates_as_dict(country=country, columns=columns, as_json=as_json)


def get_certificate_countries():
    """
    This function retrieves all the available countries to retrieve certificates from, as the listed countries 
    are the ones indexed on Investing.com. The purpose of this function is to list the countries which 
    have available certificates according to Investing.com data, since the country parameter is needed when
    retrieving data from any certificate available.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the countries listed on Investing.com with available certificates
            to retrieve data from.

            In the case that the file reading of `certificate_countries.csv` which contains the names of the available
            countries with certificates was successfully completed, the resulting :obj:`list` will look like::

                countries = ['france', 'germany', 'italy', 'netherlands', 'sweden']

    Raises:
        FileNotFoundError: raised when certificate countries file was not found.
    
    """

    return certificate_countries_as_list()
