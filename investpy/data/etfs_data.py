# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode

from ..utils import constant as cst


def etfs_as_df(country=None):
    """
    This function retrieves all the available etfs indexed on Investing.com, already stored on `etfs.csv`.
    This function also allows the users to specify which country do they want to retrieve data from or if they
    want to retrieve it from every listed country; so on, all the indexed etfs will be returned.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`pandas.DataFrame` - etfs:
            The resulting :obj:`pandas.DataFrame` contains all the etfs basic information stored on `etfs.csv`, since it
            was previously retrieved by investpy. Unless the country is specified, all the available etfs indexed on
            Investing.com is returned, but if it is specified, just the etfs from that country are returned.

            In the case that the file reading of `etfs.csv` or the retrieval process from Investing.com was
            successfully completed, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | full_name | symbol | isin | asset_class | currency | stock_exchange | def_stock_exchange
                --------|------|-----------|--------|------|-------------|----------|----------------|--------------------
                xxxxxxx | xxxx | xxxxxxxxx | xxxxxx | xxxx | xxxxxxxxxxx | xxxxxxxx | xxxxxxxxxxxxxx | xxxxxxxxxxxxxxxxxx

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        FileNotFoundError: raised when `etfs.csv` file was not found.
        IOError: raised when `etfs.csv` file is missing.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "etfs.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs not found or unable to retrieve.")

    etfs.drop(columns=["tag", "id"], inplace=True)
    etfs = etfs.where(pd.notnull(etfs), None)

    if country is None:
        etfs.reset_index(drop=True, inplace=True)
        return etfs
    else:
        country = unidecode(country.strip().lower())

        if country not in etf_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        etfs = etfs[etfs["country"] == country]
        etfs.reset_index(drop=True, inplace=True)

        return etfs


def etfs_as_list(country=None):
    """
    This function retrieves all the available etfs indexed on Investing.com, already stored on `etfs.csv`.
    This function also allows the users to specify which country do they want to retrieve data from or if they
    want to retrieve it from every listed country; so on, a listing of etfs will be returned. This function
    helps the user to get to know which etfs are available on Investing.com.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`list` - etfs_list:
            The resulting :obj:`list` contains the retrieved data from the `etfs.csv` file, which is
            a listing of the names of the etfs listed on Investing.com, which is the input for data
            retrieval functions as the name of the etf to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                etfs_list = [
                    'Betashares U.S. Equities Strong Bear Currency Hedg',
                    'Betashares Active Australian Hybrids',
                    'Australian High Interest Cash', ...
                ]

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        FileNotFoundError: raised when `etfs.csv` file was not found.
        IOError: raised when `etfs.csv` file is missing.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "etfs.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs not found or unable to retrieve.")

    etfs.drop(columns=["tag", "id"], inplace=True)
    etfs = etfs.where(pd.notnull(etfs), None)

    if country is None:
        return etfs["name"].tolist()
    else:
        country = unidecode(country.strip().lower())

        if country not in etf_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        return etfs[etfs["country"] == country]["name"].tolist()


def etfs_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available etfs indexed on Investing.com, already stored on `etfs.csv`.
    This function also allows the user to specify which country do they want to retrieve data from,
    or from every listed country; the columns which the user wants to be included on the resulting
    :obj:`dict`; and the output of the function will either be a :obj:`dict` or a :obj:`json`.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.
        columns (:obj:`list`, optional):
            names of the columns of the etf data to retrieve <country, name, full_name, symbol, isin, asset_class,
            currency, stock_exchange>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

    Returns:
        :obj:`dict` or :obj:`json` - etfs_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                etfs_dict = {
                    "country": country,
                    "name": name,
                    "full_name": full_name,
                    "symbol": symbol,
                    "isin": isin,
                    "asset_class": asset_class,
                    "currency": currency,
                    "stock_exchange": stock_exchange,
                    "def_stock_exchange": def_stock_exchange
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        FileNotFoundError: raised when `etfs.csv` file was not found.
        IOError: raised when `etfs.csv` file is missing.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "etfs.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs not found or unable to retrieve.")

    etfs.drop(columns=["tag", "id"], inplace=True)
    etfs = etfs.where(pd.notnull(etfs), None)

    if columns is None:
        columns = etfs.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in etfs.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0021: specified columns does not exist, available columns are"
            " <country, name, full_name, symbol, isin, asset_class, currency,"
            " stock_exchange>"
        )

    if country is None:
        if as_json:
            return json.dumps(etfs[columns].to_dict(orient="records"))
        else:
            return etfs[columns].to_dict(orient="records")
    else:
        country = unidecode(country.strip().lower())

        if country not in etf_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        if as_json:
            return json.dumps(
                etfs[etfs["country"] == country][columns].to_dict(orient="records")
            )
        else:
            return etfs[etfs["country"] == country][columns].to_dict(orient="records")


def etf_countries_as_list():
    """
    This function returns a listing with all the available countries from where funds can be retrieved, so to
    let the user know which of them are available, since the parameter country is mandatory in every fund retrieval
    function.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with funds as indexed in Investing.com

    """

    return [value["country"] for value in cst.ETF_COUNTRIES]
