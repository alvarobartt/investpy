# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode

from ..utils import constant as cst


def certificates_as_df(country=None):
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
        FileNotFoundError: raised if `certificates.csv` file was not found.
        IOError: raised when `certificates.csv` file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "certificates.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        certificates = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0096: certificates file not found or errored.")

    if certificates is None:
        raise IOError("ERR#0097: certificates not found or unable to retrieve.")

    certificates.drop(columns=["tag", "id"], inplace=True)
    certificates = certificates.where(pd.notnull(certificates), None)

    if country is None:
        certificates.reset_index(drop=True, inplace=True)
        return certificates
    else:
        country = unidecode(country.strip().lower())

        if country not in certificate_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        certificates = certificates[certificates["country"] == country]
        certificates.reset_index(drop=True, inplace=True)

        return certificates


def certificates_as_list(country=None):
    """
    This function retrieves all the available certificates indexed on Investing.com, already stored on `certificates.csv`.
    This function also allows the users to specify which country do they want to retrieve data from or if they
    want to retrieve it from every listed country; so on, a listing of certificates will be returned. This function
    helps the user to get to know which certificates are available on Investing.com.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available certificates from.

    Returns:
        :obj:`list` - certificates_list:
            The resulting :obj:`list` contains the retrieved data from the `certificates.csv` file, which is
            a listing of the names of the certificates listed on Investing.com, which is the input for data
            retrieval functions as the name of the certificate to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                certificates_list = ['SOCIETE GENERALE CAC 40 X10 31DEC99', 'SG ZT CAC 40 x7 Short 31Dec99', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if `certificates.csv` file was not found.
        IOError: raised when `certificates.csv` file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "certificates.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        certificates = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0096: certificates file not found or errored.")

    if certificates is None:
        raise IOError("ERR#0097: certificates not found or unable to retrieve.")

    certificates.drop(columns=["tag", "id"], inplace=True)
    certificates = certificates.where(pd.notnull(certificates), None)

    if country is None:
        return certificates["name"].tolist()
    else:
        country = unidecode(country.strip().lower())

        if country not in certificate_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        return certificates[certificates["country"] == country]["name"].tolist()


def certificates_as_dict(country=None, columns=None, as_json=False):
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
        FileNotFoundError: raised if `certificates.csv` file was not found.
        IOError: raised when `certificates.csv` file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "certificates.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        certificates = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0096: certificates file not found or errored.")

    certificates.drop(columns=["tag", "id"], inplace=True)
    certificates = certificates.where(pd.notnull(certificates), None)

    if certificates is None:
        raise IOError("ERR#0097: certificates not found or unable to retrieve.")

    if columns is None:
        columns = certificates.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in certificates.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0021: specified columns does not exist, available columns are "
            "<country, name, full_name, symbol, issuer, isin, asset_class, underlying>"
        )

    if country is None:
        if as_json:
            return json.dumps(certificates[columns].to_dict(orient="records"))
        else:
            return certificates[columns].to_dict(orient="records")
    else:
        country = unidecode(country.strip().lower())

        if country not in certificate_countries_as_list():
            raise ValueError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        if as_json:
            return json.dumps(
                certificates[certificates["country"] == country][columns].to_dict(
                    orient="records"
                )
            )
        else:
            return certificates[certificates["country"] == country][columns].to_dict(
                orient="records"
            )


def certificate_countries_as_list():
    """
    This function retrieves all the available countries to retrieve certificates from, as the listed countries
    are the ones indexed on Investing.com. The purpose of this function is to list the countries which
    have available certificates according to Investing.com data, since the country parameter is needed when
    retrieving data from any certificate available.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the countries listed on Investing.com with available certificates
            to retrieve data from.

    """

    return [value["country"] for value in cst.CERTIFICATE_COUNTRIES]
