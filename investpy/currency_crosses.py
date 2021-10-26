# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json
import string
from datetime import date, datetime, timedelta
from random import randint, sample

import pandas as pd
import pkg_resources
import pytz
import requests
from lxml.html import fromstring
from unidecode import unidecode

from .data.currency_crosses_data import (
    available_currencies_as_list,
    currency_crosses_as_df,
    currency_crosses_as_dict,
    currency_crosses_as_list,
)
from .utils import constant as cst
from .utils.data import Data
from .utils.extra import random_user_agent


def get_currency_crosses(base=None, second=None):
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

    return currency_crosses_as_df(base=base, second=second)


def get_currency_crosses_list(base=None, second=None):
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

    return currency_crosses_as_list(base=base, second=second)


def get_currency_crosses_dict(base=None, second=None, columns=None, as_json=False):
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

                {
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

    return currency_crosses_as_dict(
        base=base, second=second, columns=columns, as_json=as_json
    )


def get_available_currencies():
    """
    This function retrieves a listing with all the available currencies with indexed currency crosses in order to
    get to know which are the available currencies. The currencies listed in this function, so on, can be used to
    search currency crosses and used the retrieved data to get historical data of those currency crosses, so to
    determine which is the value of one base currency in the second currency.

    Returns:
        :obj:`list` - available_currencies:
            The resulting :obj:`list` contains all the available currencies with currency crosses being either the base
            or the second value of the cross, as listed in Investing.com.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                available_currencies = [
                    'AED', 'AFN', 'ALL', 'AMD', 'ANG', ...
                ]

    Raises:
        FileNotFoundError: raised if `currency_crosses.csv` file was not found.
        IOError: raised if currency crosses retrieval failed, both for missing file or empty file.

    """

    return available_currencies_as_list()


def get_currency_cross_recent_data(
    currency_cross, as_json=False, order="ascending", interval="Daily"
):
    """
    This function retrieves recent historical data from the introduced `currency_cross` as indexed in Investing.com
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        currency_cross (:obj:`str`): name of the currency_cross to retrieve recent historical data from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified currency_cross via argument. The dataset contains the open, high, low, close,
            volume and currency values for the selected currency_cross on market days.

            The return data is in case we use default arguments will look like::

                Date || Open | High | Low | Close | Currency
                -----||------|------|-----|-------|---------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        dd/mm/yyyy: {
                            'open': x,
                            'high': x,
                            'low': x,
                            'close': x,
                            'currency' : x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised if any of the introduced arguments was not valid or errored.
        IOError: raised if currency_crosses object/file not found or unable to retrieve.
        RuntimeError: raised introduced currency_cross does not match any of the indexed ones.
        ConnectionError: raised if GET request did not return 200 status code.
        IndexError: raised if currency_cross information was unavailable or not found.

    Examples:
        >>> data = investpy.get_currency_cross_recent_data(currency_cross='EUR/USD')
        >>> data.head()
                      Open    High     Low   Close Currency
        Date
        2019-08-27  1.1101  1.1116  1.1084  1.1091      USD
        2019-08-28  1.1090  1.1099  1.1072  1.1078      USD
        2019-08-29  1.1078  1.1093  1.1042  1.1057      USD
        2019-08-30  1.1058  1.1062  1.0963  1.0991      USD
        2019-09-02  1.0990  1.1000  1.0958  1.0968      USD

    """

    if not currency_cross:
        raise ValueError(
            "ERR#0052: currency_cross param is mandatory and should be a str."
        )

    if not isinstance(currency_cross, str):
        raise ValueError(
            "ERR#0052: currency_cross param is mandatory and should be a str."
        )

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    if order not in ["ascending", "asc", "descending", "desc"]:
        raise ValueError(
            "ERR#0003: order argument can just be ascending (asc) or descending (desc),"
            " str type."
        )

    if not interval:
        raise ValueError(
            "ERR#0073: interval value should be a str type and it can just be either"
            " 'Daily', 'Weekly' or 'Monthly'."
        )

    if not isinstance(interval, str):
        raise ValueError(
            "ERR#0073: interval value should be a str type and it can just be either"
            " 'Daily', 'Weekly' or 'Monthly'."
        )

    interval = interval.lower()

    if interval not in ["daily", "weekly", "monthly"]:
        raise ValueError(
            "ERR#0073: interval value should be a str type and it can just be either"
            " 'Daily', 'Weekly' or 'Monthly'."
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

    currency_cross = unidecode(currency_cross.strip().lower())

    if currency_cross not in list(
        currency_crosses["name"].apply(unidecode).str.lower()
    ):
        raise RuntimeError(
            "ERR#0054: the introduced currency_cross "
            + str(currency_cross)
            + " does not exist."
        )

    id_ = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "id",
    ]
    name = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "name",
    ]
    currency = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "second",
    ]

    header = name + " Historical Data"

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": interval.capitalize(),
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
    }

    head = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/HistoricalDataAjax"

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        for elements_ in path_:
            if elements_.xpath(".//td")[0].text_content() == "No results found":
                raise IndexError(
                    "ERR#0055: currency_cross information unavailable or not found."
                )

            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get("data-real-value"))

            currency_cross_date = datetime.strptime(
                str(
                    datetime.fromtimestamp(int(info[0]), tz=pytz.timezone("GMT")).date()
                ),
                "%Y-%m-%d",
            )

            currency_cross_close = float(info[1].replace(",", ""))
            currency_cross_open = float(info[2].replace(",", ""))
            currency_cross_high = float(info[3].replace(",", ""))
            currency_cross_low = float(info[4].replace(",", ""))

            result.insert(
                len(result),
                Data(
                    currency_cross_date,
                    currency_cross_open,
                    currency_cross_high,
                    currency_cross_low,
                    currency_cross_close,
                    None,
                    currency,
                    None,
                ),
            )

        if order in ["ascending", "asc"]:
            result = result[::-1]
        elif order in ["descending", "desc"]:
            result = result

        if as_json is True:
            json_ = {
                "name": name,
                "recent": [value.currency_cross_as_json() for value in result],
            }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records(
                [value.currency_cross_to_dict() for value in result]
            )
            df.set_index("Date", inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_currency_cross_historical_data(
    currency_cross,
    from_date,
    to_date,
    as_json=False,
    order="ascending",
    interval="Daily",
):
    """
    This function retrieves recent historical data from the introduced `currency_cross` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        currency_cross (:obj:`str`): name of the currency cross to retrieve recent historical data from.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified currency_cross via argument. The dataset contains the open, high, low, close and
            volume values for the selected currency_cross on market days.

            The return data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Currency
                -----||------|------|-----|-------|---------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        dd/mm/yyyy: {
                            'open': x,
                            'high': x,
                            'low': x,
                            'close': x,
                            'currency' : x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: stocks object/file not found or unable to retrieve.
        RuntimeError: introduced currency_cross does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if currency_cross information was unavailable or not found.

    Examples:
        >>> data = investpy.get_currency_cross_historical_data(currency_cross='EUR/USD', from_date='01/01/2018', to_date='01/01/2019')
        >>> data.head()
                      Open    High     Low   Close Currency
        Date
        2018-01-01  1.2003  1.2014  1.1995  1.2010      USD
        2018-01-02  1.2013  1.2084  1.2003  1.2059      USD
        2018-01-03  1.2058  1.2070  1.2001  1.2014      USD
        2018-01-04  1.2015  1.2090  1.2004  1.2068      USD
        2018-01-05  1.2068  1.2085  1.2021  1.2030      USD

    """

    if not currency_cross:
        raise ValueError(
            "ERR#0052: currency_cross param is mandatory and should be a str."
        )

    if not isinstance(currency_cross, str):
        raise ValueError(
            "ERR#0052: currency_cross param is mandatory and should be a str."
        )

    try:
        datetime.strptime(from_date, "%d/%m/%Y")
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.strptime(to_date, "%d/%m/%Y")
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.strptime(from_date, "%d/%m/%Y")
    end_date = datetime.strptime(to_date, "%d/%m/%Y")

    if start_date >= end_date:
        raise ValueError(
            "ERR#0032: to_date should be greater than from_date, both formatted as"
            " 'dd/mm/yyyy'."
        )

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    if order not in ["ascending", "asc", "descending", "desc"]:
        raise ValueError(
            "ERR#0003: order argument can just be ascending (asc) or descending (desc),"
            " str type."
        )

    if not interval:
        raise ValueError(
            "ERR#0073: interval value should be a str type and it can just be either"
            " 'Daily', 'Weekly' or 'Monthly'."
        )

    if not isinstance(interval, str):
        raise ValueError(
            "ERR#0073: interval value should be a str type and it can just be either"
            " 'Daily', 'Weekly' or 'Monthly'."
        )

    interval = interval.lower()

    if interval not in ["daily", "weekly", "monthly"]:
        raise ValueError(
            "ERR#0073: interval value should be a str type and it can just be either"
            " 'Daily', 'Weekly' or 'Monthly'."
        )

    date_interval = {
        "intervals": [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 19:
            obj = {
                "start": start_date.strftime("%m/%d/%Y"),
                "end": start_date.replace(year=start_date.year + 19).strftime(
                    "%m/%d/%Y"
                ),
            }

            date_interval["intervals"].append(obj)

            start_date = start_date.replace(year=start_date.year + 19) + timedelta(
                days=1
            )
        else:
            obj = {
                "start": start_date.strftime("%m/%d/%Y"),
                "end": end_date.strftime("%m/%d/%Y"),
            }

            date_interval["intervals"].append(obj)

            flag = False

    interval_limit = len(date_interval["intervals"])
    interval_counter = 0

    data_flag = False

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

    currency_cross = unidecode(currency_cross.strip().lower())

    if currency_cross not in list(
        currency_crosses["name"].apply(unidecode).str.lower()
    ):
        raise RuntimeError(
            "ERR#0054: the introduced currency_cross "
            + str(currency_cross)
            + " does not exist."
        )

    id_ = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "id",
    ]
    name = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "name",
    ]
    currency = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "second",
    ]

    final = list()

    header = name + " Historical Data"

    for index in range(len(date_interval["intervals"])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval["intervals"][index]["start"],
            "end_date": date_interval["intervals"][index]["end"],
            "interval_sec": interval.capitalize(),
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data",
        }

        head = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        url = "https://www.investing.com/instruments/HistoricalDataAjax"

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError(
                "ERR#0015: error " + str(req.status_code) + ", try again later."
            )

        if not req.text:
            continue

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")

        result = list()

        if path_:
            for elements_ in path_:
                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get("data-real-value"))

                if elements_.xpath(".//td")[0].text_content() == "No results found":
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError(
                            "ERR#0055: currency_cross information unavailable or not"
                            " found."
                        )
                else:
                    data_flag = True

                if data_flag is True:
                    currency_cross_date = datetime.strptime(
                        str(
                            datetime.fromtimestamp(
                                int(info[0]), tz=pytz.timezone("GMT")
                            ).date()
                        ),
                        "%Y-%m-%d",
                    )

                    currency_cross_close = float(info[1].replace(",", ""))
                    currency_cross_open = float(info[2].replace(",", ""))
                    currency_cross_high = float(info[3].replace(",", ""))
                    currency_cross_low = float(info[4].replace(",", ""))

                    result.insert(
                        len(result),
                        Data(
                            currency_cross_date,
                            currency_cross_open,
                            currency_cross_high,
                            currency_cross_low,
                            currency_cross_close,
                            None,
                            currency,
                            None,
                        ),
                    )

            if data_flag is True:
                if order in ["ascending", "asc"]:
                    result = result[::-1]
                elif order in ["descending", "desc"]:
                    result = result

                if as_json is True:
                    json_list = [value.currency_cross_as_json() for value in result]

                    final.append(json_list)
                elif as_json is False:
                    df = pd.DataFrame.from_records(
                        [value.currency_cross_to_dict() for value in result]
                    )
                    df.set_index("Date", inplace=True)

                    final.append(df)
        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    if order in ["descending", "desc"]:
        final.reverse()

    if as_json is True:
        json_ = {
            "name": name,
            "historical": [value for json_list in final for value in json_list],
        }
        return json.dumps(json_, sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def get_currency_cross_information(currency_cross, as_json=False):
    """
    This function retrieves fundamental financial information from the specified currency cross. The retrieved
    information from the currency cross can be valuable as it is additional information that can be used combined
    with OHLC values, so to determine financial insights from the company which holds the specified currency cross.

    Args:
        currency_cross (:obj:`str`): name of the currency_cross to retrieve recent historical data from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`pandas.DataFrame` or :obj:`dict`- currency cross_information:
            The resulting :obj:`pandas.DataFrame` contains the information fields retrieved from Investing.com
            from the specified currency cross; it can also be returned as a :obj:`dict`, if argument `as_json=True`.

            If any of the information fields could not be retrieved, that field/s will be filled with
            None values. If the retrieval process succeeded, the resulting :obj:`dict` will look like::

                currency_cross_information = {
                    "1-Year Change": "- 1.61%",
                    "52 wk Range": "1.0879 - 1.1572",
                    "Ask": 1.1144,
                    "Bid": 1.114,
                    "Currency Cross": "EUR/USD",
                    "Open": 1.1121,
                    "Prev. Close": 1.1119,
                    "Todays Range": "1.1123 - 1.1159"
                }

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if `currency_crosses.csv` file was not found.
        IOError: raised if `currency_crosses.csv` file is empty or errored.
        RuntimeError: raised if scraping process failed while running.
        ConnectionError: raised if the connection to Investing.com errored (did not return HTTP 200)

    """

    if not currency_cross:
        raise ValueError(
            "ERR#0052: currency_cross param is mandatory and should be a str."
        )

    if not isinstance(currency_cross, str):
        raise ValueError(
            "ERR#0052: currency_cross param is mandatory and should be a str."
        )

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

    currency_cross = unidecode(currency_cross.strip().lower())

    if currency_cross not in list(
        currency_crosses["name"].apply(unidecode).str.lower()
    ):
        raise RuntimeError(
            "ERR#0054: the introduced currency_cross "
            + str(currency_cross)
            + " does not exist."
        )

    name = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "name",
    ]
    tag = currency_crosses.loc[
        (
            currency_crosses["name"].apply(unidecode).str.lower() == currency_cross
        ).idxmax(),
        "tag",
    ]

    url = "https://www.investing.com/currencies/" + tag

    head = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root_ = fromstring(req.text)
    path_ = root_.xpath("//div[contains(@class, 'overviewDataTable')]/div")

    result = pd.DataFrame(
        columns=[
            "Currency Cross",
            "Prev. Close",
            "Bid",
            "Todays Range",
            "Open",
            "Ask",
            "52 wk Range",
            "1-Year Change",
        ]
    )
    result.at[0, "Currency Cross"] = name

    if path_:
        for elements_ in path_:
            element = elements_.xpath(".//span[@class='float_lang_base_1']")[0]
            title_ = element.text_content()
            if title_ == "Day's Range":
                title_ = "Todays Range"
            if title_ in result.columns.tolist():
                try:
                    result.at[0, title_] = float(
                        element.getnext().text_content().replace(",", "")
                    )
                    continue
                except:
                    pass
                try:
                    text = element.getnext().text_content().strip()
                    result.at[0, title_] = datetime.strptime(
                        text, "%b %d, %Y"
                    ).strftime("%d/%m/%Y")
                    continue
                except:
                    pass
                try:
                    value = element.getnext().text_content().strip()
                    if value.__contains__("K"):
                        value = float(value.replace("K", "").replace(",", "")) * 1e3
                    elif value.__contains__("M"):
                        value = float(value.replace("M", "").replace(",", "")) * 1e6
                    elif value.__contains__("B"):
                        value = float(value.replace("B", "").replace(",", "")) * 1e9
                    elif value.__contains__("T"):
                        value = float(value.replace("T", "").replace(",", "")) * 1e12
                    result.at[0, title_] = value
                    continue
                except:
                    pass

        result.replace({"N/A": None}, inplace=True)

        if as_json is True:
            json_ = result.iloc[0].to_dict()
            return json_
        elif as_json is False:
            return result
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_currency_crosses_overview(currency, as_json=False, n_results=100):
    """
    This function retrieves an overview containing all the real time data available for the main stocks from a country,
    such as the names, symbols, current value, etc. as indexed in Investing.com. So on, the main usage of this
    function is to get an overview on the main stocks from a country, so to get a general view. Note that since
    this function is retrieving a lot of information at once, by default just the overview of the Top 100 stocks
    is being retrieved, but an additional parameter called n_results can be specified so to retrieve N results.

    Args:
        currency (:obj:`str`): name of the currency to retrieve the currency crosses overview from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        n_results (:obj:`int`, optional): number of results to be displayed on the overview table (0-1000).

    Returns:
        :obj:`pandas.DataFrame` - stocks_overview:
            The resulting :obj:`pandas.DataFrame` contains all the data available in Investing.com of the main currency
            crosses from a given currency in order to get an overview of them.

            If the retrieval process succeeded, the resulting :obj:`pandas.DataFrame` should look like::

                symbol | name | bid | ask | high | low | change | change_percentage
                -------|------|-----|-----|------|-----|--------|-------------------
                xxxxxx | xxxx | xxx | xxx | xxxx | xxx | xxxxxx | xxxxxxxxxxxxxxxxx

    Raises:
        ValueError: raised if any of the introduced arguments errored.
        FileNotFoundError: raised if `currencies.csv` file is missing.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError:
            raised either if the introduced currency does not match any of the listed ones or if no overview results could be
            retrieved from Investing.com.
        ConnectionError: raised if GET requests does not return 200 status code.

    """

    if currency is None:
        raise ValueError("ERR#0105: currency can not be None, it should be a str.")

    if not isinstance(currency, str):
        raise ValueError("ERR#0106: specified currency value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    if not isinstance(n_results, int):
        raise ValueError(
            "ERR#0089: n_results argument should be an integer between 1 and 1000."
        )

    if 1 > n_results or n_results > 1000:
        raise ValueError(
            "ERR#0089: n_results argument should be an integer between 1 and 1000."
        )

    currency = unidecode(currency.strip().lower())

    if currency not in [value.lower() for value in list(cst.CURRENCIES.keys())]:
        raise ValueError("ERR#0106: specified currency value not valid.")

    session_id = "".join(sample(string.ascii_lowercase, 9))

    params = {
        "session_uniq_id": session_id,
        "currencies": cst.CURRENCIES[currency.upper()],
    }

    head = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/currencies/Service/ChangeCurrency"

    req = requests.get(url, headers=head, params=params)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root_ = fromstring(req.json()["HTML"])
    table = root_.xpath(".//table[@id='cr1']/tbody/tr")

    results = list()

    if len(table) > 0:
        for row in table[:n_results]:
            id_ = row.get("id").replace("pair_", "")

            symbol = (
                row.xpath(".//td[contains(@class, 'elp')]/a")[0].text_content().strip()
            )
            name = row.xpath(".//td[contains(@class, 'elp')]/a")[0].get("title")

            if symbol.__contains__(currency + "="):
                old_symbol = symbol
                symbol = symbol.replace("=", "").replace(currency, "/" + currency)
                name = name.replace(old_symbol, symbol)
            elif symbol.__contains__("="):
                old_symbol = symbol
                symbol = symbol.replace("=", "").replace(currency, currency + "/")
                name = name.replace(old_symbol, symbol)

            pid = "pid-" + id_

            bid = row.xpath(".//td[@class='" + pid + "-bid']")[0].text_content()
            ask = row.xpath(".//td[@class='" + pid + "-ask']")[0].text_content()
            high = row.xpath(".//td[@class='" + pid + "-high']")[0].text_content()
            low = row.xpath(".//td[@class='" + pid + "-low']")[0].text_content()

            pc = row.xpath(".//td[contains(@class, '" + pid + "-pc')]")[
                0
            ].text_content()
            pcp = row.xpath(".//td[contains(@class, '" + pid + "-pcp')]")[
                0
            ].text_content()

            data = {
                "symbol": symbol,
                "name": name,
                "bid": float(bid.replace(",", "")),
                "ask": float(ask.replace(",", "")),
                "high": float(high.replace(",", "")),
                "low": float(low.replace(",", "")),
                "change": pc,
                "change_percentage": pcp,
            }

            results.append(data)
    else:
        raise RuntimeError(
            "ERR#0092: no data found while retrieving the overview from Investing.com"
        )

    df = pd.DataFrame(results)

    if as_json:
        return json.loads(df.to_json(orient="records"))
    else:
        return df


def search_currency_crosses(by, value):
    """
    This function searches currency crosses by the introduced value for the specified field. This means that this
    function is going to search if there is a value that matches the introduced value for the specified field which is
    the `currency_crosses.csv` column name to search in. Available fields to search indices are 'name', 'full_name',
    'base', 'second', 'base_name' and 'second_name'.

    Args:
        by (:obj:`str`):
            name of the field to search for, which is the column name ('name', 'full_name', 'base', 'second',
            'base_name' or 'second_name').
        value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
       :obj:`pandas.DataFrame` - search_result:
           The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
           in the specified field). If there are no results and error will be raised, but otherwise this
           `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
       ValueError: raised if any of the introduced params is not valid or errored.
       FileNotFoundError: raised if `currency_crosses.csv` file is missing.
       IOError: raised if data could not be retrieved due to file error.
       RuntimeError: raised if no results were found for the introduced value in the introduced field.

    """

    if not by:
        raise ValueError(
            "ERR#0006: the introduced field to search is mandatory and should be a str."
        )

    if not isinstance(by, str):
        raise ValueError(
            "ERR#0006: the introduced field to search is mandatory and should be a str."
        )

    if not value:
        raise ValueError(
            "ERR#0017: the introduced value to search is mandatory and should be a str."
        )

    if not isinstance(value, str):
        raise ValueError(
            "ERR#0017: the introduced value to search is mandatory and should be a str."
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

    currency_crosses.drop(columns=["tag", "id"], inplace=True)

    available_search_fields = currency_crosses.columns.tolist()

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError(
            "ERR#0026: the introduced field to search can either just be "
            + " or ".join(available_search_fields)
        )

    currency_crosses["matches"] = currency_crosses[by].str.contains(value, case=False)

    search_result = currency_crosses.loc[currency_crosses["matches"] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError(
            "ERR#0043: no results were found for the introduced " + str(by) + " value."
        )

    search_result.drop(columns=["matches"], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
