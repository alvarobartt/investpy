# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode


def cryptos_as_df():
    """
    This function retrieves all the crypto data stored in `cryptos.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the crypto data is properly
    structured in rows and columns, where columns are the crypto data attribute names.

    Note that just some cryptos are available for retrieval, since Investing.com does not provide information
    from all the available ones, just the main ones.

    Returns:
        :obj:`pandas.DataFrame` - cryptos_df:
            The resulting :obj:`pandas.DataFrame` contains all the crypto data from every available crypto coin as
            indexed in Investing.com from the information previously retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                name | symbol | currency
                -----|--------|----------
                xxxx | xxxxxx | xxxxxxxx

    Raises:
        FileNotFoundError: raised if `cryptos.csv` file was not found.
        IOError: raised when `cryptos.csv` file is missing or empty.

    """

    resource_package = "investpy"
    resource_path = "/".join(("resources", "cryptos.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        cryptos = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0081: cryptos file not found or errored.")

    if cryptos is None:
        raise IOError("ERR#0082: cryptos not found or unable to retrieve.")

    cryptos = cryptos[cryptos["status"] == "available"]

    cryptos.drop(columns=["tag", "id", "status"], inplace=True)
    cryptos = cryptos.where(pd.notnull(cryptos), None)
    cryptos.reset_index(drop=True, inplace=True)

    return cryptos


def cryptos_as_list():
    """
    This function retrieves all the crypto coin names stored in `cryptos.csv` file, which contains all the
    data from the crypto coins as previously retrieved from Investing.com. So on, this function will just return
    the crypto coin names which will be the main input parameters when it comes to crypto data retrieval functions
    from investpy.

    Note that just some cryptos are available for retrieval, since Investing.com does not provide information
    from all the available ones, just the main ones.

    Returns:
        :obj:`list` - cryptos_list:
            The resulting :obj:`list` contains the all the available crypto coin names as indexed in Investing.com
            from the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of crypto coin names will look like::

                cryptos_list = ['Bitcoin', 'Ethereum', 'XRP', 'Bitcoin Cash', 'Tether', 'Litecoin', ...]

    Raises:
        FileNotFoundError: raised if `cryptos.csv` file was not found.
        IOError: raised when `cryptos.csv` file is missing or empty.

    """

    resource_package = "investpy"
    resource_path = "/".join(("resources", "cryptos.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        cryptos = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0081: cryptos file not found or errored.")

    if cryptos is None:
        raise IOError("ERR#0082: cryptos not found or unable to retrieve.")

    cryptos = cryptos[cryptos["status"] == "available"]
    cryptos.drop(columns=["tag", "id", "status"], inplace=True)
    cryptos = cryptos.where(pd.notnull(cryptos), None)

    return cryptos["name"].tolist()


def cryptos_as_dict(columns=None, as_json=False):
    """
    This function retrieves all the crypto information stored in the `cryptos.csv` file and formats it as a
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the
    JSON structure. Some optional paramaters can be specified such as the columns or as_json, which are the
    column names that want to be retrieved in case of needing just some columns to avoid unnecessary information
    load, and whether the information wants to be returned as a JSON object or as a dictionary; respectively.

    Note that just some cryptos are available for retrieval, since Investing.com does not provide information
    from all the available ones, just the main ones.

    Args:
        columns (:obj:`list`, optional):column names of the crypto data to retrieve, can be: <name, currency, symbol>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - cryptos_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every crypto coin as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                cryptos_dict = {
                    'name': name,
                    'currency': currency,
                    'symbol': symbol,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if `cryptos.csv` file was not found.
        IOError: raised when `cryptos.csv` file is missing or empty.

    """

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "cryptos.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        cryptos = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0081: cryptos file not found or errored.")

    if cryptos is None:
        raise IOError("ERR#0082: cryptos not found or unable to retrieve.")

    cryptos = cryptos[cryptos["status"] == "available"]
    cryptos.drop(columns=["tag", "id", "status"], inplace=True)
    cryptos = cryptos.where(pd.notnull(cryptos), None)

    if columns is None:
        columns = cryptos.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in cryptos.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0021: specified columns does not exist, available columns are "
            "<name, symbol, currency>"
        )

    if as_json:
        return json.dumps(cryptos[columns].to_dict(orient="records"))
    else:
        return cryptos[columns].to_dict(orient="records")
