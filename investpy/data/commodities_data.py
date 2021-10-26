# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode

from ..utils import constant as cst


def commodities_as_df(group=None):
    """
    This function retrieves all the commodities data stored in `commodities.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the commodities data is properly
    structured in rows and columns, where columns are the commodity data attribute names. Additionally, group
    filtering can be specified, so that the return commodities are from the specified group instead from every
    available group. Anyways, since it is an optional parameter it does not need to be specified, which means that
    if it is None or not specified, all the available commodities will be returned.

    Args:
        group (:obj:`str`, optional): name of the group to retrieve all the available commodities from.

    Returns:
        :obj:`pandas.DataFrame` - commodities_df:
            The resulting :obj:`pandas.DataFrame` contains all the commodities data from the introduced group if specified,
            or from all the commodity groups if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                title | country | name | full_name | currency | group
                ------|---------|------|-----------|----------|-------
                xxxxx | xxxxxxx | xxxx | xxxxxxxxx | xxxxxxxx | xxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `commodities.csv` file was not found.
        IOError: raised when `commodities.csv` file is missing or empty.

    """

    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0076: specified commodity group value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "commodities.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities.drop(columns=["tag", "id"], inplace=True)
    commodities = commodities.where(pd.notnull(commodities), None)

    if group is None:
        commodities.reset_index(drop=True, inplace=True)
        return commodities
    else:
        group = unidecode(group.strip().lower())

        if group not in commodity_groups_list():
            raise ValueError(
                "ERR#0077: introduced group does not exists or is not a valid one."
            )

        commodities = commodities[commodities["group"] == group]
        commodities.reset_index(drop=True, inplace=True)

        return commodities


def commodities_as_list(group=None):
    """
    This function retrieves all the commodity names as stored in `commodities.csv` file, which contains all the
    data from the commodities as previously retrieved from Investing.com. So on, this function will just return
    the commodity names from either all the available groups or from any group, which will later be used when it
    comes to both recent and historical data retrieval.

    Args:
        group (:obj:`str`, optional): name of the group to retrieve all the available commodities from.

    Returns:
        :obj:`list` - commodities_list:
            The resulting :obj:`list` contains the all the commodity names from the introduced group if specified,
            or from every group if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of commodity names will look like::

                commodities_list = ['Gold', 'Copper', 'Silver', 'Palladium', 'Platinum', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `commodities.csv` file was not found.
        IOError: raised when `commodities.csv` file is missing or empty.

    """

    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0076: specified commodity group value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "commodities.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities.drop(columns=["tag", "id"], inplace=True)
    commodities = commodities.where(pd.notnull(commodities), None)

    if group is None:
        return commodities["name"].tolist()
    else:
        group = unidecode(group.strip().lower())

        if group not in commodity_groups_list():
            raise ValueError(
                "ERR#0077: introduced group does not exists or is not a valid one."
            )

        return commodities[commodities["group"] == group]["name"].tolist()


def commodities_as_dict(group=None, columns=None, as_json=False):
    """
    This function retrieves all the commodities information stored in the `commodities.csv` file and formats it as a
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the
    JSON structure. Some optional paramaters can be specified such as the group, columns or as_json, which
    are the name of the commodity group to filter between all the available commodities so not to return all the
    commodities but just the ones from the introduced group, the column names that want to be retrieved in case
    of needing just some columns to avoid unnecessary information load, and whether the information wants to be
    returned as a JSON object or as a dictionary; respectively.

    Args:
        group (:obj:`str`, optional): name of the group to retrieve all the available commodities from.
        columns (:obj:`list`, optional):
            column names of the commodities data to retrieve, can be: <title, country, name, full_name, currency, group>
        as_json (:obj:`bool`, optional):
            if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - bonds_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every bond as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                commodities_dict = {
                    'title': title,
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'currency': currency,
                    'group': group,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `commodities.csv` file was not found.
        IOError: raised when `commodities.csv` file is missing or empty.

    """

    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0076: specified commodity group value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "commodities.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    commodities.drop(columns=["tag", "id"], inplace=True)
    commodities = commodities.where(pd.notnull(commodities), None)

    if columns is None:
        columns = commodities.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in commodities.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0021: specified columns does not exist, available columns are "
            "<title, country, name, full_name, currency, group>"
        )

    if group is None:
        if as_json:
            return json.dumps(commodities[columns].to_dict(orient="records"))
        else:
            return commodities[columns].to_dict(orient="records")
    else:
        group = unidecode(group.strip().lower())

        if group not in commodity_groups_list():
            raise ValueError(
                "ERR#0077: introduced group does not exists or is not a valid one."
            )

        if as_json:
            return json.dumps(
                commodities[commodities["group"] == group][columns].to_dict(
                    orient="records"
                )
            )
        else:
            return commodities[commodities["group"] == group][columns].to_dict(
                orient="records"
            )


def commodity_groups_list():
    """
    This function returns a listing with all the available commodity groupsson that a filtering can be applied when
    retrieving data from commodities. The current available commodity groups are metals, agriculture and energy,
    which include all the raw materials or commodities included in them.

    Returns:
        :obj:`list` - commodity_groups:
            The resulting :obj:`list` contains all the available commodity groups as indexed in Investing.com

    Raises:
        FileNotFoundError: raised when `commodities.csv` file was not found.
        IOError: raised when `commodities.csv` file is missing or empty.

    """

    resource_package = "investpy"
    resource_path = "/".join(("resources", "commodities.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        commodities = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0075: commodities file not found or errored.")

    if commodities is None:
        raise IOError("ERR#0076: commodities not found or unable to retrieve.")

    return commodities["group"].unique().tolist()
