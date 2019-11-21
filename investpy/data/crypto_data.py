#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import unidecode
import json

import pandas as pd
import pkg_resources


def cryptos_as_df():
    """
    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'cryptos', 'cryptos.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        cryptos = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0081: cryptos file not found or errored.")

    if cryptos is None:
        raise IOError("ERR#0082: cryptos not found or unable to retrieve.")

    cryptos = cryptos[cryptos['status'] == 'available']
    cryptos.drop(columns=['tag', 'id', 'status'], inplace=True)

    commodities.reset_index(drop=True, inplace=True)
    return commodities


def cryptos_as_list():
    """
    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'cryptos', 'cryptos.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        cryptos = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0081: cryptos file not found or errored.")

    if cryptos is None:
        raise IOError("ERR#0082: cryptos not found or unable to retrieve.")

    cryptos = cryptos[cryptos['status'] == 'available']
    cryptos.drop(columns=['tag', 'id', 'status'], inplace=True)

    return commodities['name'].tolist()


def cryptos_as_dict(columns=None, as_json=False):
    """
    """

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'cryptos', 'cryptos.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        cryptos = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0081: cryptos file not found or errored.")

    if cryptos is None:
        raise IOError("ERR#0082: cryptos not found or unable to retrieve.")

    cryptos = cryptos[cryptos['status'] == 'available']
    cryptos.drop(columns=['tag', 'id', 'status'], inplace=True)

    if columns is None:
        columns = cryptos.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in cryptos.columns.tolist() for column in columns):
        raise ValueError("ERR#0021: specified columns does not exist, available columns are "
                         "<name, symbol, currency>")

    if as_json:
        return json.dumps(cryptos[columns].to_dict(orient='records'))
    else:
        return cryptos[columns].to_dict(orient='records')
