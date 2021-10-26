# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode

from ..utils import constant as cst


def funds_as_df(country=None):
    """
    This function retrieves all the available `funds` from Investing.com and returns them as a :obj:`pandas.DataFrame`,
    which contains not just the fund names, but all the fields contained on the `funds.csv` file.
    All the available funds can be found at: https://www.investing.com/funds/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available funds from.

    Returns:
        :obj:`pandas.DataFrame` - funds_df:
            The resulting :obj:`pandas.DataFrame` contains all the funds basic information retrieved from Investing.com,
            some of which is not useful for the user, but for the inner package functions, such as the `id` field,
            for example.

            In case the information was successfully retrieved, the :obj:`pandas.DataFrame` will look like::

                country | name | symbol | issuer | isin | asset_class | currency | underlying
                --------|------|--------|--------|------|-------------|----------|------------
                xxxxxxx | xxxx | xxxxxx | xxxxxx | xxxx | xxxxxxxxxxx | xxxxxxxx | xxxxxxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised when the `funds.csv` file was not found.
        IOError: raised if the `funds.csv` file is missing or errored.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds not found or unable to retrieve.")

    funds.drop(columns=["tag", "id"], inplace=True)
    funds = funds.where(pd.notnull(funds), None)

    if country is None:
        funds.reset_index(drop=True, inplace=True)
        return funds
    else:
        country = unidecode(country.strip().lower())

        if country not in fund_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        funds = funds[funds["country"] == unidecode(country.lower())]
        funds.reset_index(drop=True, inplace=True)

        return funds


def funds_as_list(country=None):
    """
    This function retrieves all the available funds and returns a list of each one of them.
    All the available funds can be found at: https://www.investing.com/funds/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available funds from.

    Returns:
        :obj:`list` - funds_list:
            The resulting list contains the retrieved data, which corresponds to the fund names of
            every fund listed on Investing.com.

            In case the information was successfully retrieved from the CSV file, the :obj:`list` will look like::

                funds = [
                    'Blackrock Global Funds - Global Allocation Fund E2',
                    'Quality Inversión Conservadora Fi',
                    'Nordea 1 - Stable Return Fund E Eur',
                    ...
                ]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised when the `funds.csv` file was not found.
        IOError: raised if the `funds.csv` file is missing or errored.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds not found or unable to retrieve.")

    funds.drop(columns=["tag", "id"], inplace=True)
    funds = funds.where(pd.notnull(funds), None)

    if country is None:
        return funds["name"].tolist()
    else:
        country = unidecode(country.strip().lower())

        if country not in fund_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        return funds[funds["country"] == country]["name"].tolist()


def funds_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available funds on Investing.com and returns them as a :obj:`dict` containing
    the country, name, symbol, tag, id, issuer, isin, asset_class, currency and underlying data. All the available
    funds can be found at: https://www.investing.com/funds/

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available funds from.
        columns (:obj:`list` of :obj:`str`, optional): description
            a :obj:`list` containing the column names from which the data is going to be retrieved.
        as_json (:obj:`bool`, optional): description
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - funds_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'country': country,
                    'name': name,
                    'symbol': symbol,
                    'issuer': issuer,
                    'isin': isin,
                    'asset_class': asset_class,
                    'currency': currency,
                    'underlying': underlying
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised when the `funds.csv` file was not found.
        IOError: raised if the `funds.csv` file is missing or errored.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds not found or unable to retrieve.")

    funds.drop(columns=["tag", "id"], inplace=True)
    funds = funds.where(pd.notnull(funds), None)

    if columns is None:
        columns = funds.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in funds.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0023: specified columns does not exist, available columns are "
            "<country, name, symbol, issuer, isin, asset_class, currency, underlying>"
        )

    if country is None:
        if as_json:
            return json.dumps(funds[columns].to_dict(orient="records"))
        else:
            return funds[columns].to_dict(orient="records")
    else:
        country = unidecode(country.strip().lower())

        if country not in fund_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        if as_json:
            return json.dumps(
                funds[funds["country"] == country][columns].to_dict(orient="records")
            )
        else:
            return funds[funds["country"] == country][columns].to_dict(orient="records")


def fund_countries_as_list():
    """
    This function returns a listing with all the available countries from where funds can be retrieved, so to
    let the user know which of them are available, since the parameter country is mandatory in every fund retrieval
    function.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with funds as indexed in Investing.com

    """

    return [value["country"] for value in cst.FUND_COUNTRIES]
