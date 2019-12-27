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


def get_certificate_recent_data():
    return None


def get_certificate_historical_data():
    return None


def get_certificate_information():
    return None


def get_certificates_overview():
    return None


def search_certificates(by, value):
    """
    This function searches certificates by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced one for the specified field which is the
    `certificates.csv` column name to search in. Available fields to search certificates are `country`, `name`, 
    `full_name`, `symbol`, `issuer`, `isin`, `asset_class`, `underlying`.

    Args:
        by (:obj:`str`):
            name of the field to search for, which is the column name which can be: country, name, full_name, symbol,
            issuer, isin, asset_class or underlying.
        value (:obj:`str`): value of the field to search for, which is the value that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting :obj:`pandas.DataFrame` contains the search results from the given query, which is
            any match of the specified value in the specified field. If there are no results for the given query,
            an error will be raised, but otherwise the resulting :obj:`pandas.DataFrame` will contain all the
            available certificates that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised if no results were found for the introduced value in the introduced field.

    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'certificates', 'certificates.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        certificates = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0096: certificates file not found or errored.")

    if certificates is None:
        raise IOError("ERR#0097: certificates not found or unable to retrieve.")

    certificates.drop(columns=['tag', 'id'], inplace=True)

    available_search_fields = certificates.columns.tolist()

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    certificates['matches'] = certificates[by].str.contains(value, case=False)

    search_result = certificates.loc[certificates['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
