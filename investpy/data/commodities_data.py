#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import unidecode
import json

import pandas as pd
import pkg_resources


def commodities_as_df(group=None):
    """
    """
    
    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0076: specified commodity group value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities.drop(columns=['tag', 'id'], inplace=True)

    if group is None:
        commodities.reset_index(drop=True, inplace=True)
        return commodities
    else:
        if unidecode.unidecode(group.lower()) in commodity_groups_list():
            commodities = commodities[commodities['group'] == unidecode.unidecode(group.lower())]
            commodities.reset_index(drop=True, inplace=True)
            return commodities
        else:
            raise ValueError("ERR#0077: introduced group does not exists or is not a valid one.")


def commodities_as_list(group=None):
    """
    """

    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0076: specified commodity group value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities.drop(columns=['tag', 'id'], inplace=True)

    if group is None:
        return commodities['symbol'].tolist()
    else:
        if unidecode.unidecode(group.lower()) in commodity_groups_list():
            return commodities[commodities['group'] == unidecode.unidecode(group.lower())]['symbol'].tolist()
        else:
            raise ValueError("ERR#0077: introduced group does not exists or is not a valid one.")


def commodities_as_dict(group=None, columns=None, as_json=False):
    """
    """

    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0076: specified commodity group value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities.drop(columns=['tag', 'id'], inplace=True)

    if columns is None:
        columns = commodities.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in commodities.columns.tolist() for column in columns):
        raise ValueError("ERR#0021: specified columns does not exist, available columns are "
                         "<title, country, id, name, full_name, tag, currency, group>")

    if group is None:
        if as_json:
            return json.dumps(commodities[columns].to_dict(orient='records'))
        else:
            return commodities[columns].to_dict(orient='records')
    else:
        if group in commodity_groups_list():
            if as_json:
                return json.dumps(commodities[commodities['group'] == unidecode.unidecode(group.lower())][columns].to_dict(orient='records'))
            else:
                return commodities[commodities['group'] == unidecode.unidecode(group.lower())][columns].to_dict(orient='records')
        else:
            raise ValueError("ERR#0077: introduced group does not exists or is not a valid one.")


def commodity_groups_list():
    """
    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'commodities', 'commodities.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")
    else:
        return commodities['group'].unique().tolist()
