# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode

from ..utils import constant as cst


def bonds_as_df(country=None):
    """
    This function retrieves all the bonds data stored in `bonds.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the bonds data is properly
    structured in rows and columns, where columns are the bond data attribute names. Additionally, country
    filtering can be specified, which will make this function return not all the stored bond data, but just
    the data of the bonds from the introduced country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.

    Returns:
        :obj:`pandas.DataFrame` - bonds_df:
            The resulting :obj:`pandas.DataFrame` contains all the bond data from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | full name
                --------|------|-----------
                xxxxxxx | xxxx | xxxxxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `bonds.csv` file was not found.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "bonds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    bonds.drop(columns=["tag", "id"], inplace=True)
    bonds = bonds.where(pd.notnull(bonds), None)

    if country is None:
        bonds.reset_index(drop=True, inplace=True)
        return bonds
    else:
        country = unidecode(country.strip().lower())

        if country not in bond_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        bonds = bonds[bonds["country"] == country]
        bonds.reset_index(drop=True, inplace=True)

        return bonds


def bonds_as_list(country=None):
    """
    This function retrieves all the bond names as stored in `bonds.csv` file, which contains all the
    data from the bonds as previously retrieved from Investing.com. So on, this function will just return
    the government bond names which will be one of the input parameters when it comes to bond data retrieval functions
    from investpy. Additionally, note that the country filtering can be applied, which is really useful since
    this function just returns the names and in bond data retrieval functions both the name and the country
    must be specified and they must match.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.

    Returns:
        :obj:`list` - bonds_list:
            The resulting :obj:`list` contains the all the bond names from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of bond names will look like::

                bonds_list = ['Argentina 1Y', 'Argentina 3Y', 'Argentina 5Y', 'Argentina 9Y', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `bonds.csv` file was not found.
        IOError: raised when `bonds.csv` file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "bonds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    bonds.drop(columns=["tag", "id"], inplace=True)
    bonds = bonds.where(pd.notnull(bonds), None)

    if country is None:
        return bonds["name"].tolist()
    else:
        country = unidecode(country.strip().lower())

        if country not in bond_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        return bonds[bonds["country"] == country]["name"].tolist()


def bonds_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the bonds information stored in the `bonds.csv` file and formats it as a
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the
    JSON structure. Some optional paramaters can be specified such as the country, columns or as_json, which
    are a filtering by country so not to return all the bonds but just the ones from the introduced country,
    the column names that want to be retrieved in case of needing just some columns to avoid unnecessary information
    load, and whether the information wants to be returned as a JSON object or as a dictionary; respectively.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available bonds from.
        columns (:obj:`list`, optional): column names of the bonds data to retrieve, can be: <country, name, full_name>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - bonds_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every bond as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                bonds_dict = {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised when `bonds.csv` file was not found.
        IOError: raised when `bonds.csv` file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "bonds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        bonds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0064: bonds file not found or errored.")

    if bonds is None:
        raise IOError("ERR#0062: bonds country list not found or unable to retrieve.")

    bonds.drop(columns=["tag", "id"], inplace=True)
    bonds = bonds.where(pd.notnull(bonds), None)

    if columns is None:
        columns = bonds.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in bonds.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0063: specified columns does not exist, available columns are "
            "<country, name, full_name>"
        )

    if country is None:
        if as_json:
            return json.dumps(bonds[columns].to_dict(orient="records"))
        else:
            return bonds[columns].to_dict(orient="records")
    else:
        country = unidecode(country.strip().lower())

        if country not in bond_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        if as_json:
            return json.dumps(
                bonds[bonds["country"] == country][columns].to_dict(orient="records")
            )
        else:
            return bonds[bonds["country"] == country][columns].to_dict(orient="records")


def bond_countries_as_list():
    """
    This function returns a listing with all the available countries from where bonds can be retrieved, so to
    let the user know which of them are available, since the parameter country is mandatory in every bond retrieval
    function.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with government bonds as indexed in Investing.com

    """

    return [value["country"] for value in cst.BOND_COUNTRIES]
