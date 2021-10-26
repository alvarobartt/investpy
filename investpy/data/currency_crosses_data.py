# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources
from unidecode import unidecode

from ..utils import constant as cst


def currency_crosses_as_df(base=None, second=None):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`pandas.DataFrame`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file. Note that the filtering params are both base and second, which mean the base and the
    second currency of the currency cross, for example, in the currency cross `EUR/USD` the base currency is EUR and
    the second currency is USD. These are optional parameters, so specifying one of them means that all the currency
    crosses where the introduced currency is either base or second will be returned; if both are specified,
    just the introduced currency cross will be returned if it exists. All the available currency crosses can be found
    at: https://www.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.

    Returns:
        :obj:`pandas.DataFrame` - currency_crosses_df:
            The resulting :obj:`pandas.DataFrame` contains all the currency crosses basic information retrieved from
            Investing.com.

            In case the information was successfully retrieved, the resulting :obj:`pandas.DataFrame` will look like::

                name | full_name | base | second | base_name | second_name
                -----|-----------|------|--------|-----------|-------------
                xxxx | xxxxxxxxx | xxxx | xxxxxx | xxxxxxxxx | xxxxxxxxxxx

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if `currency_crosses.csv` file was not found.
        IOError: raised if currency crosses retrieval failed, both for missing file or empty file.

    """

    if base is not None and not isinstance(base, str):
        raise ValueError("ERR#0049: specified base currency value is not valid.")

    if second is not None and not isinstance(second, str):
        raise ValueError("ERR#0051: specified second currency value is not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "currency_crosses.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0060: currency_crosses file not found or errored.")

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    available_currencies = available_currencies_as_list()

    currency_crosses.drop(columns=["tag", "id"], inplace=True)
    currency_crosses = currency_crosses.where(pd.notnull(currency_crosses), None)

    if base is None and second is None:
        currency_crosses.reset_index(drop=True, inplace=True)
        return currency_crosses
    elif base is not None:
        base = unidecode(base.strip().upper())

        if base not in available_currencies:
            raise ValueError(
                "ERR#0053: the introduced currency " + base + " does not exists."
            )

        if second is not None:
            second = unidecode(second.strip().upper())

            if second not in available_currencies:
                raise ValueError(
                    "ERR#0053: the introduced currency " + second + " does not exists."
                )

            currency_crosses = currency_crosses[
                (currency_crosses["base"] == base)
                & (currency_crosses["second"] == second)
            ]

            currency_crosses.reset_index(drop=True, inplace=True)

            if len(currency_crosses) > 0:
                return currency_crosses
            else:
                raise ValueError(
                    "ERR#0054: the introduced currency cross "
                    + base
                    + "/"
                    + second
                    + " does not exists."
                )
        else:
            currency_crosses = currency_crosses[currency_crosses["base"] == base]
            currency_crosses.reset_index(drop=True, inplace=True)

            return currency_crosses
    elif second is not None:
        second = unidecode(second.strip().upper())

        if second not in available_currencies:
            raise ValueError(
                "ERR#0053: the introduced currency " + second + " does not exists."
            )

        currency_crosses = currency_crosses[currency_crosses["second"] == second]
        currency_crosses.reset_index(drop=True, inplace=True)

        return currency_crosses


def currency_crosses_as_list(base=None, second=None):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`dict`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file is columns is None, otherwise, just the specified column values will be returned. Note
    that the filtering params are both base and second, which mean the base and the second currency of the currency
    cross, for example, in the currency cross `EUR/USD` the base currency is EUR and the second currency is USD. These
    are optional parameters, so specifying one of them means that all the currency crosses where the introduced
    currency is either base or second will be returned; if both are specified, just the introduced currency cross will
    be returned if it exists. All the available currency crosses can be found at: https://www.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.

    Returns:
        :obj:`list` - currency_crosses_list:
            The resulting :obj:`list` contains the retrieved data from the `currency_crosses.csv` file, which is
            a listing of the names of the currency crosses listed in Investing.com, which is the input for data
            retrieval functions as the name of the currency cross to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                currency_crosses_list = [
                    'USD/BRLT', 'CAD/CHF', 'CHF/CAD', 'CAD/PLN', 'PLN/CAD', ...
                ]

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if `currency_crosses.csv` file was not found.
        IOError: raised if currency crosses retrieval failed, both for missing file or empty file.

    """

    if base is not None and not isinstance(base, str):
        raise ValueError("ERR#0049: specified base currency value is not valid.")

    if second is not None and not isinstance(second, str):
        raise ValueError("ERR#0051: specified second currency value is not valid.")

    resource_package = "investpy"
    resource_path = "/".join(("resources", "currency_crosses.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0060: currency_crosses file not found or errored.")

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    available_currencies = available_currencies_as_list()

    currency_crosses.drop(columns=["tag", "id"], inplace=True)
    currency_crosses = currency_crosses.where(pd.notnull(currency_crosses), None)

    if base is None and second is None:
        currency_crosses.reset_index(drop=True, inplace=True)
        return currency_crosses["name"].tolist()
    elif base is not None:
        base = unidecode(base.strip().upper())

        if base not in available_currencies:
            raise ValueError(
                "ERR#0053: the introduced currency " + base + " does not exists."
            )

        if second is not None:
            second = unidecode(second.strip().upper())

            if second not in available_currencies:
                raise ValueError(
                    "ERR#0053: the introduced currency " + second + " does not exists."
                )

            currency_crosses = currency_crosses[
                (currency_crosses["base"] == base)
                & (currency_crosses["second"] == second)
            ]

            currency_crosses.reset_index(drop=True, inplace=True)

            if len(currency_crosses) > 0:
                return currency_crosses["name"].tolist()
            else:
                raise ValueError(
                    "ERR#0054: the introduced currency cross "
                    + base
                    + "/"
                    + second
                    + " does not exists."
                )
        else:
            currency_crosses = currency_crosses[currency_crosses["base"] == base]
            currency_crosses.reset_index(drop=True, inplace=True)

            return currency_crosses["name"].tolist()
    elif second is not None:
        second = unidecode(second.strip().upper())

        if second not in available_currencies:
            raise ValueError(
                "ERR#0053: the introduced currency " + second + " does not exists."
            )

        currency_crosses = currency_crosses[currency_crosses["second"] == second]
        currency_crosses.reset_index(drop=True, inplace=True)

        return currency_crosses["name"].tolist()


def currency_crosses_as_dict(base=None, second=None, columns=None, as_json=False):
    """
    This function retrieves all the available currency crosses from Investing.com and returns them as a
    :obj:`dict`, which contains not just the currency crosses names, but all the fields contained on
    the currency_crosses file is columns is None, otherwise, just the specified column values will be returned. Note
    that the filtering params are both base and second, which mean the base and the second currency of the currency
    cross, for example, in the currency cross `EUR/USD` the base currency is EUR and the second currency is USD. These
    are optional parameters, so specifying one of them means that all the currency crosses where the introduced
    currency is either base or second will be returned; if both are specified, just the introduced currency cross will
    be returned if it exists. All the available currency crosses can be found at: https://www.investing.com/currencies/

    Args:
        base (:obj:`str`, optional):
            symbol of the base currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the base currency matches the introduced one.
        second (:obj:`str`):
            symbol of the second currency of the currency cross, this will return a :obj:`pandas.DataFrame` containing
            all the currency crosses where the second currency matches the introduced one.
        columns (:obj:`list`, optional):
            names of the columns of the currency crosses data to retrieve <name, full_name, base, base_name,
            second, second_name>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data which can either be a :obj:`dict` or a :obj:`json`.

    Returns:
        :obj:`dict` or :obj:`json` - currency_crosses_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                currency_crosses_dict = {
                    'name': name,
                    'full_name': full_name,
                    'base': base,
                    'base_name': base_name,
                    'second': second,
                    'second_name': second_name
                }

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if `currency_crosses.csv` file was not found.
        IOError: raised if currency crosses retrieval failed, both for missing file or empty file.

    """

    if base is not None and not isinstance(base, str):
        raise ValueError("ERR#0049: specified base currency value is not valid.")

    if second is not None and not isinstance(second, str):
        raise ValueError("ERR#0051: specified second currency value is not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    resource_package = "investpy"
    resource_path = "/".join(("resources", "currency_crosses.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        currency_crosses = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0060: currency_crosses file not found or errored.")

    if currency_crosses is None:
        raise IOError("ERR#0050: currency_crosses not found or unable to retrieve.")

    available_currencies = available_currencies_as_list()

    currency_crosses.drop(columns=["tag", "id"], inplace=True)
    currency_crosses = currency_crosses.where(pd.notnull(currency_crosses), None)

    if columns is None:
        columns = currency_crosses.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError(
                "ERR#0020: specified columns argument is not a list, it can just be"
                " list type."
            )

    if not all(column in currency_crosses.columns.tolist() for column in columns):
        raise ValueError(
            "ERR#0021: specified columns does not exist, available columns are "
            "<name, full_name, base, base_name, second, second_name>"
        )

    if base is None and second is None:
        currency_crosses.reset_index(drop=True, inplace=True)

        if as_json:
            return json.dumps(currency_crosses[columns].to_dict(orient="records"))
        else:
            return currency_crosses[columns].to_dict(orient="records")
    elif base is not None:
        base = unidecode(base.strip().upper())

        if base not in available_currencies:
            raise ValueError(
                "ERR#0053: the introduced currency " + base + " does not exists."
            )

        if second is not None:
            second = unidecode(second.strip().upper())

            if second not in available_currencies:
                raise ValueError(
                    "ERR#0053: the introduced currency " + second + " does not exists."
                )

            currency_crosses = currency_crosses[
                (currency_crosses["base"] == base)
                & (currency_crosses["second"] == second)
            ]

            currency_crosses.reset_index(drop=True, inplace=True)

            if len(currency_crosses) > 0:
                if as_json:
                    return json.dumps(
                        currency_crosses[columns].to_dict(orient="records")
                    )
                else:
                    return currency_crosses[columns].to_dict(orient="records")
            else:
                raise ValueError(
                    "ERR#0054: the introduced currency cross "
                    + base
                    + "/"
                    + second
                    + " does not exists."
                )
        else:
            currency_crosses = currency_crosses[currency_crosses["base"] == base]
            currency_crosses.reset_index(drop=True, inplace=True)

            if as_json:
                return json.dumps(currency_crosses[columns].to_dict(orient="records"))
            else:
                return currency_crosses[columns].to_dict(orient="records")
    elif second is not None:
        second = unidecode(second.strip().upper())

        if second not in available_currencies:
            raise ValueError(
                "ERR#0053: the introduced currency " + second + " does not exists."
            )

        currency_crosses = currency_crosses[
            currency_crosses["second"] == unidecode(second.upper())
        ]
        currency_crosses.reset_index(drop=True, inplace=True)

        if as_json:
            return json.dumps(currency_crosses[columns].to_dict(orient="records"))
        else:
            return currency_crosses[columns].to_dict(orient="records")


def available_currencies_as_list():
    """
    This function retrieves a listing with all the available currencies with indexed currency crosses in order to
    get to know which are the available currencies. The currencies listed in this function, so on, can be used to
    search currency crosses and used the retrieved data to get historical data of those currency crosses, so to
    determine which is the value of one base currency in the second currency.

    Returns:
        :obj:`list` - available_currencies:
            The resulting :obj:`list` contains all the available currencies with currency crosses being either the base
            or the second value of the cross, as listed in Investing.com.

    """

    return list(cst.CURRENCIES.keys())
