# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json
from datetime import date, datetime, timedelta
from random import randint

import pandas as pd
import pkg_resources
import pytz
import requests
from lxml.html import fromstring
from unidecode import unidecode

from .data.crypto_data import cryptos_as_df, cryptos_as_dict, cryptos_as_list
from .utils.data import Data
from .utils.extra import random_user_agent


def get_cryptos():
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

    return cryptos_as_df()


def get_cryptos_list():
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

    return cryptos_as_list()


def get_cryptos_dict(columns=None, as_json=False):
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

    return cryptos_as_dict(columns=columns, as_json=as_json)


def get_crypto_recent_data(crypto, as_json=False, order="ascending", interval="Daily"):
    """
    This function retrieves recent historical data from the introduced crypto from Investing.com. So on, the recent data
    of the introduced crypto will be retrieved and returned as a :obj:`pandas.DataFrame` if the parameters are valid
    and the request to Investing.com succeeds. Note that additionally some optional parameters can be specified: as_json
    and order, which let the user decide if the data is going to be returned as a :obj:`json` or not, and if the historical
    data is going to be ordered ascending or descending (where the index is the date), respectively.

    Args:
        crypto (:obj:`str`): name of the crypto currency to retrieve data from.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            recent data of the specified crypto currency. So on, the resulting dataframe contains the open, high, low,
            close and volume values for the selected crypto on market days and the currency in which those values are presented.

            The resulting recent data, in case that the default parameters were applied, will look like::

                Date || Open | High | Low | Close | Volume | Currency
                -----||------|------|-----|-------|--------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but in case that as_json parameter was defined as True, then the output will be::

                {
                    name: name,
                    recent: [
                        {
                            date: 'dd/mm/yyyy',
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        IOError: raised if cryptos object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced crypto name was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if crypto recent data was unavailable or not found in Investing.com.

    Examples:
        >>> data = investpy.get_crypto_recent_data(crypto='bitcoin')
        >>> data.head()
                      Open     High     Low   Close   Volume Currency
        Date
        2019-10-25  7422.8   8697.7  7404.9  8658.3  1177632      USD
        2019-10-26  8658.4  10540.0  8061.8  9230.6  1784005      USD
        2019-10-27  9230.6   9773.2  9081.0  9529.6  1155038      USD
        2019-10-28  9530.1   9866.9  9202.5  9207.2  1039295      USD
        2019-10-29  9206.5   9531.3  9125.3  9411.3   918477      USD

    """

    if not crypto:
        raise ValueError(
            "ERR#0083: crypto parameter is mandatory and must be a valid crypto name."
        )

    if not isinstance(crypto, str):
        raise ValueError("ERR#0084: crypto argument needs to be a str.")

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

    crypto = unidecode(crypto.strip().lower())

    if crypto not in list(cryptos["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0085: crypto currency: "
            + crypto
            + ", not found, check if it is correct."
        )

    status = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "status"
    ]
    if status == "unavailable":
        raise ValueError(
            "ERR#0086: the selected crypto currency is not available for retrieval in"
            " Investing.com."
        )

    crypto_name = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "name"
    ]
    crypto_id = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "id"
    ]
    crypto_currency = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "currency"
    ]

    header = crypto_name + " Historical Data"

    params = {
        "curr_id": crypto_id,
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
                    "ERR#0087: crypto information unavailable or not found."
                )

            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get("data-real-value"))

            crypto_date = datetime.strptime(
                str(
                    datetime.fromtimestamp(int(info[0]), tz=pytz.timezone("GMT")).date()
                ),
                "%Y-%m-%d",
            )

            crypto_close = float(info[1].replace(",", ""))
            crypto_open = float(info[2].replace(",", ""))
            crypto_high = float(info[3].replace(",", ""))
            crypto_low = float(info[4].replace(",", ""))

            crypto_volume = int(info[5])

            result.insert(
                len(result),
                Data(
                    crypto_date,
                    crypto_open,
                    crypto_high,
                    crypto_low,
                    crypto_close,
                    crypto_volume,
                    crypto_currency,
                    None,
                ),
            )

        if order in ["ascending", "asc"]:
            result = result[::-1]
        elif order in ["descending", "desc"]:
            result = result

        if as_json is True:
            json_ = {
                "name": crypto_name,
                "recent": [value.crypto_as_json() for value in result],
            }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.crypto_to_dict() for value in result])
            df.set_index("Date", inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_crypto_historical_data(
    crypto, from_date, to_date, as_json=False, order="ascending", interval="Daily"
):
    """
    This function retrieves historical data from the introduced crypto from Investing.com. So on, the historical data
    of the introduced crypto will be retrieved and returned as a :obj:`pandas.DataFrame` if the parameters are valid
    and the request to Investing.com succeeds. Note that additionally some optional parameters can be specified: as_json
    and order, which let the user decide if the data is going to be returned as a :obj:`json` or not, and if the historical
    data is going to be ordered ascending or descending (where the index is the date), respectively.

    Args:
        crypto (:obj:`str`): name of the crypto currency to retrieve data from.
        from_date (:obj:`str`): date formatted as `dd/mm/yyyy`, since when data is going to be retrieved.
        to_date (:obj:`str`): date formatted as `dd/mm/yyyy`, until when data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            historical data of the specified crypto currency. So on, the resulting dataframe contains the open, high,
            low, close and volume values for the selected crypto on market days and the currency in which those values are presented.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Volume | Currency
                -----||------|------|-----|-------|--------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: 'dd/mm/yyyy',
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            volume: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        IOError: raised if cryptos object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced crypto currency name was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if crypto historical data was unavailable or not found in Investing.com.

    Examples:
        >>> data = investpy.get_crypto_historical_data(crypto='bitcoin', from_date='01/01/2018', to_date='01/01/2019')
        >>> data.head()
                       Open     High      Low    Close  Volume Currency
        Date
        2018-01-01  13850.5  13921.5  12877.7  13444.9   78425      USD
        2018-01-02  13444.9  15306.1  12934.2  14754.1  137732      USD
        2018-01-03  14754.1  15435.0  14579.7  15156.6  106543      USD
        2018-01-04  15156.5  15408.7  14244.7  15180.1  110969      USD
        2018-01-05  15180.1  17126.9  14832.4  16954.8  141960      USD

    """

    if not crypto:
        raise ValueError(
            "ERR#0083: crypto parameter is mandatory and must be a valid crypto name."
        )

    if not isinstance(crypto, str):
        raise ValueError("ERR#0084: crypto argument needs to be a str.")

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

    try:
        datetime.strptime(from_date, "%d/%m/%Y")
    except ValueError:
        raise ValueError(
            "ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'."
        )

    try:
        datetime.strptime(to_date, "%d/%m/%Y")
    except ValueError:
        raise ValueError(
            "ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'."
        )

    start_date = datetime.strptime(from_date, "%d/%m/%Y")
    end_date = datetime.strptime(to_date, "%d/%m/%Y")

    if start_date >= end_date:
        raise ValueError(
            "ERR#0032: to_date should be greater than from_date, both formatted as"
            " 'dd/mm/yyyy'."
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

    crypto = unidecode(crypto.strip().lower())

    if crypto not in list(cryptos["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0085: crypto currency: "
            + crypto
            + ", not found, check if it is correct."
        )

    status = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "status"
    ]
    if status == "unavailable":
        raise ValueError(
            "ERR#0086: the selected crypto currency is not available for retrieval in"
            " Investing.com."
        )

    crypto_name = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "name"
    ]
    crypto_id = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "id"
    ]
    crypto_currency = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "currency"
    ]

    header = crypto_name + " Historical Data"

    final = list()

    for index in range(len(date_interval["intervals"])):
        interval_counter += 1

        params = {
            "curr_id": crypto_id,
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
                if elements_.xpath(".//td")[0].text_content() == "No results found":
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError(
                            "ERR#0087: crypto information unavailable or not found."
                        )
                else:
                    data_flag = True

                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get("data-real-value"))

                if data_flag is True:
                    crypto_date = datetime.strptime(
                        str(
                            datetime.fromtimestamp(
                                int(info[0]), tz=pytz.timezone("GMT")
                            ).date()
                        ),
                        "%Y-%m-%d",
                    )

                    crypto_close = float(info[1].replace(",", ""))
                    crypto_open = float(info[2].replace(",", ""))
                    crypto_high = float(info[3].replace(",", ""))
                    crypto_low = float(info[4].replace(",", ""))

                    crypto_volume = int(info[5] or 0)

                    result.insert(
                        len(result),
                        Data(
                            crypto_date,
                            crypto_open,
                            crypto_high,
                            crypto_low,
                            crypto_close,
                            crypto_volume,
                            crypto_currency,
                            None,
                        ),
                    )

            if data_flag is True:
                if order in ["ascending", "asc"]:
                    result = result[::-1]
                elif order in ["descending", "desc"]:
                    result = result

                if as_json is True:
                    json_list = [value.crypto_as_json() for value in result]

                    final.append(json_list)
                elif as_json is False:
                    df = pd.DataFrame.from_records(
                        [value.crypto_to_dict() for value in result]
                    )
                    df.set_index("Date", inplace=True)

                    final.append(df)
        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    if order in ["descending", "desc"]:
        final.reverse()

    if as_json is True:
        json_ = {
            "name": crypto_name,
            "historical": [value for json_list in final for value in json_list],
        }
        return json.dumps(json_, sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def get_crypto_information(crypto, as_json=False):
    """
    This function retrieves fundamental financial information from the specified crypto currency. The retrieved
    information from the crypto currency can be valuable as it is additional information that can be used combined
    with OHLC values, so to determine financial insights from the company which holds the specified crypto currency.

    Args:
        currency_cross (:obj:`str`): name of the currency_cross to retrieve recent historical data from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`pandas.DataFrame` or :obj:`dict`- crypto_information:
            The resulting :obj:`pandas.DataFrame` contains the information fields retrieved from Investing.com
            from the specified crypto currency; it can also be returned as a :obj:`dict`, if argument `as_json=True`.

            If any of the information fields could not be retrieved, that field/s will be filled with
            None values. If the retrieval process succeeded, the resulting :obj:`dict` will look like::

                crypto_information = {
                    'Chg (7D)': '-4.63%',
                    'Circulating Supply': ' BTC18.10M',
                    'Crypto Currency': 'Bitcoin',
                    'Currency': 'USD',
                    'Market Cap': '$129.01B',
                    'Max Supply': 'BTC21.00M',
                    'Todays Range': '7,057.8 - 7,153.1',
                    'Vol (24H)': '$17.57B'
                }

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if `cryptos.csv` file was not found or errored.
        IOError: raised if `cryptos.csv` file is empty or errored.
        RuntimeError: raised if scraping process failed while running.
        ConnectionError: raised if the connection to Investing.com errored (did not return HTTP 200)

    """

    if not crypto:
        raise ValueError(
            "ERR#0083: crypto parameter is mandatory and must be a valid crypto name."
        )

    if not isinstance(crypto, str):
        raise ValueError("ERR#0084: crypto argument needs to be a str.")

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

    crypto = unidecode(crypto.strip().lower())

    if crypto not in list(cryptos["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0085: crypto currency: "
            + crypto
            + ", not found, check if it is correct."
        )

    status = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "status"
    ]
    if status == "unavailable":
        raise ValueError(
            "ERR#0086: the selected crypto currency is not available for retrieval in"
            " Investing.com."
        )

    name = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "name"
    ]
    currency = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "currency"
    ]
    tag = cryptos.loc[
        (cryptos["name"].apply(unidecode).str.lower() == crypto).idxmax(), "tag"
    ]

    url = "https://www.investing.com/crypto/" + tag

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
    path_ = root_.xpath("//div[@class='cryptoGlobalData']/div")

    result = pd.DataFrame(
        columns=[
            "Crypto Currency",
            "Market Cap",
            "Circulating Supply",
            "Max Supply",
            "Vol (24H)",
            "Todays Range",
            "Chg (7D)",
            "Currency",
        ]
    )
    result.at[0, "Crypto Currency"] = name
    result.at[0, "Currency"] = currency

    if path_:
        for elements_ in path_:
            element = elements_.xpath(".//span[@class='title']")[0]
            title_ = element.text_content().replace(":", "")
            if title_ == "Day's Range":
                title_ = "Todays Range"
            if title_ in result.columns.tolist():
                result.at[0, title_] = element.getnext().text_content().strip()

        result.replace({"N/A": None}, inplace=True)

        if as_json is True:
            json_ = result.iloc[0].to_dict()
            return json_
        elif as_json is False:
            return result
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_cryptos_overview(as_json=False, n_results=100):
    """
    This function retrieves an overview containing all the real time data available for the main crypto currencies,
    such as the names, symbols, current value, etc. as indexed in Investing.com. So on, the main usage of this
    function is to get an overview on the main crypto currencies, so to get a general view. Note that since
    this function is retrieving a lot of information at once, by default just the overview of the Top 100 crypto
    currencies is being retrieved, but an additional parameter called n_results can be specified so to retrieve N results.

    Args:
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        n_results (:obj:`int`, optional):
            number of results to be displayed on the overview table (0-all_cryptos), where all crypto currencies will
            be retrieved if n_results=None.

    Note:
        The amount of indexed crypto currencies may vary, so if n_results is set to `None`, all the available crypto
        currencies in Investing.com while retrieving the overview, will be retrieved and returned.

    Returns:
        :obj:`pandas.DataFrame` - cryptos_overview:
            The resulting :obj:`pandas.DataFrame` contains all the data available in Investing.com of the main crypto
            currencies in order to get an overview of it.

            If the retrieval process succeeded, the resulting :obj:`pandas.DataFrame` should look like::

                name | symbol | price | market_cap | volume24h | total_volume | change24h | change7d | currency
                -----|--------|-------|------------|-----------|--------------|-----------|----------|----------
                xxxx | xxxxxx | xxxxx | xxxxxxxxxx | xxxxxxxxx | xxxxxxxxxxxx | xxxxxxxxx | xxxxxxxx | xxxxxxxx

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised it no overview results could be retrieved from Investing.com.
        ConnectionError: raised if GET requests does not return 200 status code.

    """

    if not isinstance(as_json, bool):
        raise ValueError(
            "ERR#0002: as_json argument can just be True or False, bool type."
        )

    if n_results is not None and not isinstance(n_results, int):
        raise ValueError(
            "ERR#0089: n_results argument should be an integer between 1 and 1000."
        )

    if n_results is not None:
        if 1 > n_results or n_results > 1000:
            raise ValueError(
                "ERR#0089: n_results argument should be an integer between 1 and 1000."
            )

    header = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/crypto/currencies"

    req = requests.get(url, headers=header)

    root = fromstring(req.text)
    table = root.xpath(".//table[contains(@class, 'allCryptoTlb')]/tbody/tr")

    results = list()

    flag = False

    if len(table) < 1:
        raise RuntimeError(
            "ERR#0092: no data found while retrieving the overview from Investing.com"
        )

    if n_results is not None and n_results <= 100:
        table = table[:n_results]
        flag = True

    for row in table:
        name = (
            row.xpath(".//td[contains(@class, 'cryptoName')]")[0].text_content().strip()
        )
        symbol = row.xpath(".//td[contains(@class, 'symb')]")[0].get("title").strip()

        # Due to Investing.com parsing error
        if symbol in ["GRV", "GLYPH"]:
            continue

        tag = row.xpath(".//td[contains(@class, 'cryptoName')]/a")

        if len(tag) > 0:
            status = "available"
        else:
            status = "unavailable"

        price = row.xpath(".//td[contains(@class, 'price')]")[0].text_content()

        market_cap = row.xpath(".//td[@class='js-market-cap']")[0].get("data-value")
        volume24h = row.xpath(".//td[@class='js-24h-volume']")[0].get("data-value")
        total_volume = row.xpath(".//td[@class='js-total-vol']")[0].text_content()

        change24h = row.xpath(".//td[contains(@class, 'js-currency-change-24h')]")[
            0
        ].text_content()
        change7d = row.xpath(".//td[contains(@class, 'js-currency-change-7d')]")[
            0
        ].text_content()

        data = {
            "name": name,
            "symbol": symbol,
            "status": status,
            "price": float(price.replace(",", "")),
            "market_cap": float(market_cap.replace(",", "")),
            "volume24h": volume24h,
            "total_volume": total_volume,
            "change24h": change24h,
            "change7d": change7d,
            "currency": "USD",
        }

        results.append(data)

    if flag is True:
        df = pd.DataFrame(results)

        if as_json:
            return json.loads(df.to_json(orient="records"))
        else:
            return df
    else:
        header = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        params = {"lastRowId": 100}

        url = "https://www.investing.com/crypto/Service/LoadCryptoCurrencies"

        req = requests.post(url=url, headers=header, data=params)

        root = fromstring(req.json()["html"])
        table = root.xpath(".//tr")

        if n_results is not None:
            remaining_cryptos = n_results - len(results)
            table = table[:remaining_cryptos]

        if len(table) < 1:
            raise RuntimeError(
                "ERR#0092: no data found while retrieving the overview from"
                " Investing.com"
            )

        for row in table:
            name = (
                row.xpath(".//td[contains(@class, 'cryptoName')]")[0]
                .text_content()
                .strip()
            )
            symbol = (
                row.xpath(".//td[contains(@class, 'symb')]")[0].get("title").strip()
            )

            # Due to Investing.com parsing error
            if symbol in ["GRV", "GLYPH"]:
                continue

            tag = row.xpath(".//td[contains(@class, 'cryptoName')]/a")

            if len(tag) > 0:
                status = "available"
            else:
                status = "unavailable"

            price = row.xpath(".//td[contains(@class, 'price')]")[0].text_content()

            market_cap = row.xpath(".//td[@class='js-market-cap']")[0].get("data-value")
            volume24h = row.xpath(".//td[@class='js-24h-volume']")[0].get("data-value")
            total_volume = row.xpath(".//td[@class='js-total-vol']")[0].text_content()

            change24h = row.xpath(".//td[contains(@class, 'js-currency-change-24h')]")[
                0
            ].text_content()
            change7d = row.xpath(".//td[contains(@class, 'js-currency-change-7d')]")[
                0
            ].text_content()

            data = {
                "name": name,
                "symbol": symbol,
                "status": status,
                "price": float(price.replace(",", "")),
                "market_cap": float(market_cap.replace(",", "")),
                "volume24h": volume24h,
                "total_volume": total_volume,
                "change24h": change24h,
                "change7d": change7d,
                "currency": "USD",
            }

            results.append(data)

    df = pd.DataFrame(results)

    if as_json:
        return json.loads(df.to_json(orient="records"))
    else:
        return df


def search_cryptos(by, value):
    """
    This function searches cryptos by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced one for the specified field which is the
    `cryptos.csv` column name to search in. Available fields to search cryptos are 'name' and 'symbol'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name which can be: 'name' or 'symbol'.
        value (:obj:`str`): value of the field to search for, which is the value that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting :obj:`pandas.DataFrame` contains the search results from the given query, which is
            any match of the specified value in the specified field. If there are no results for the given query,
            an error will be raised, but otherwise the resulting :obj:`pandas.DataFrame` will contain all the
            available cryptos that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        FileNotFoundError: raised if `cryptos.csv` file is missing.
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

    cryptos.drop(columns=["tag", "id"], inplace=True)

    available_search_fields = cryptos.columns.tolist()

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError(
            "ERR#0026: the introduced field to search can either just be "
            + " or ".join(available_search_fields)
        )

    cryptos["matches"] = cryptos[by].str.contains(value, case=False)

    search_result = cryptos.loc[cryptos["matches"] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError(
            "ERR#0043: no results were found for the introduced " + str(by) + "."
        )

    search_result.drop(columns=["matches"], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
