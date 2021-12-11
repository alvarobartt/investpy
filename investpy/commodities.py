# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json
import warnings
from datetime import date, datetime, timedelta
from random import randint

import pandas as pd
import pkg_resources
import pytz
import requests
from lxml.html import fromstring
from unidecode import unidecode

from .data.commodities_data import (
    commodities_as_df,
    commodities_as_dict,
    commodities_as_list,
    commodity_groups_list,
)
from .utils.data import Data
from .utils.extra import random_user_agent


def get_commodities(group=None):
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

    return commodities_as_df(group=group)


def get_commodities_list(group=None):
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

    return commodities_as_list(group=group)


def get_commodities_dict(group=None, columns=None, as_json=False):
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

    return commodities_as_dict(group=group, columns=columns, as_json=as_json)


def get_commodity_groups():
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

    return commodity_groups_list()


def get_commodity_recent_data(
    commodity, country=None, as_json=False, order="ascending", interval="Daily"
):
    """
    This function retrieves recent historical data from the introduced commodity from Investing.com, which will be
    returned as a :obj:`pandas.DataFrame` if the parameters are valid and the request to Investing.com succeeds.
    Note that additionally some optional parameters can be specified: as_json and order, which let the user decide
    if the data is going to be returned as a :obj:`json` or not, and if the historical data is going to be ordered
    ascending or descending (where the index is the date), respectively.

    Args:
        commodity (:obj:`str`): name of the commodity to retrieve recent data from.
        country (:obj:`str`, optional):
            name of the country to retrieve the commodity data from (if there is more than one country that
            provides data from the same commodity).
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function can return either a :obj:`pandas.DataFrame` or a :obj:`json` object, containing the retrieved
            recent data of the specified commodity. So on, the resulting dataframe contains the open, high, low and close
            values for the selected commodity on market days and the currency in which those values are presented.

            The returned data is case we use default arguments will look like::

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
        IOError: raised if commodities object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced commodity was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if commodity recent data was unavailable or not found in Investing.com.

    Examples:
        >>> data = investpy.get_commodity_recent_data(commodity='gold')
        >>> data.head()
                      Open    High     Low   Close  Volume Currency
        Date
        2019-10-25  1506.4  1520.9  1503.1  1505.3  368743      USD
        2019-10-28  1507.4  1510.8  1492.3  1495.8  318126      USD
        2019-10-29  1494.3  1497.1  1485.6  1490.7  291980      USD
        2019-10-30  1490.5  1499.3  1483.1  1496.7  353638      USD
        2019-10-31  1498.8  1516.7  1496.0  1514.8  390013      USD

    """

    if not commodity:
        raise ValueError(
            "ERR#0078: commodity parameter is mandatory and must be a valid commodity"
            " name."
        )

    if not isinstance(commodity, str):
        raise ValueError(
            "ERR#0078: commodity parameter is mandatory and must be a valid commodity"
            " name."
        )

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

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

    commodity = unidecode(commodity.strip().lower())

    if commodity not in list(commodities["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0079: commodity " + commodity + " not found, check if it is correct."
        )

    if country is None:
        found_commodities = commodities[
            commodities["name"].apply(unidecode).str.lower() == commodity
        ]

        if len(found_commodities) > 1:
            msg = (
                "Note that the displayed commodity data can differ depending on the"
                " country. If you want to retrieve "
                + commodity
                + " data from either "
                + " or ".join(found_commodities["country"].tolist())
                + ", specify the country parameter."
            )
            warnings.warn(msg, Warning)

        del found_commodities
    else:
        country = unidecode(country.strip().lower())

        if country not in list(set(commodities["country"].str.lower())):
            raise RuntimeError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        commodities = commodities[commodities["country"] == country]

    full_name = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(),
        "full_name",
    ]
    id_ = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(), "id"
    ]
    name = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(), "name"
    ]

    currency = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(),
        "currency",
    ]

    header = full_name + " Historical Data"

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
                    "ERR#0080: commodity information unavailable or not found."
                )

            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get("data-real-value"))

            commodity_date = datetime.strptime(
                str(
                    datetime.fromtimestamp(int(info[0]), tz=pytz.timezone("GMT")).date()
                ),
                "%Y-%m-%d",
            )

            commodity_close = float(info[1].replace(",", ""))
            commodity_open = float(info[2].replace(",", ""))
            commodity_high = float(info[3].replace(",", ""))
            commodity_low = float(info[4].replace(",", ""))

            commodity_volume = int(info[5])

            result.insert(
                len(result),
                Data(
                    commodity_date,
                    commodity_open,
                    commodity_high,
                    commodity_low,
                    commodity_close,
                    commodity_volume,
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
                "recent": [value.commodity_as_json() for value in result],
            }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records(
                [value.commodity_to_dict() for value in result]
            )
            df.set_index("Date", inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_commodity_historical_data(
    commodity,
    from_date,
    to_date,
    country=None,
    as_json=False,
    order="ascending",
    interval="Daily",
):
    """
    This function retrieves historical data from the introduced commodity from Investing.com. So on, the historical data
    of the introduced commodity in the specified date range will be retrieved and returned as a :obj:`pandas.DataFrame`
    if the parameters are valid and the request to Investing.com succeeds. Note that additionally some optional parameters
    can be specified: as_json and order, which let the user decide if the data is going to be returned as a :obj:`json` or not,
    and if the historical data is going to be ordered ascending or descending (where the index is the date), respectively.

    Args:
        commodity (:obj:`str`): name of the commodity to retrieve recent data from.
        from_date (:obj:`str`): date formatted as `dd/mm/yyyy`, since when data is going to be retrieved.
        to_date (:obj:`str`): date formatted as `dd/mm/yyyy`, until when data is going to be retrieved.
        country (:obj:`str`, optional):
            name of the country to retrieve the commodity data from (if there is more than one country that
            provides data from the same commodity).
        as_json (:obj:`bool`, optional):
            to determine the format of the output data, either a :obj:`pandas.DataFrame` if False and a :obj:`json` if True.
        order (:obj:`str`, optional): to define the order of the retrieved data which can either be ascending or descending.
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            historical data of the specified commodity. So on, the resulting dataframe contains the open, high, low and close
            values for the selected commodity on market days and the currency in which those values are presented.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Volume | Currency
                -----||------|------|-----|-------|--------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxx | xxxxxxxx

            but in case that as_json parameter was defined as True, then the output will be::

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
        IOError: raised if commodities object/file was not found or unable to retrieve.
        RuntimeError: raised if the introduced commodity was not found or did not match any of the existing ones.
        ConnectionError: raised if connection to Investing.com could not be established.
        IndexError: raised if commodity historical data was unavailable or not found in Investing.com.

    Examples:
        >>> data = investpy.get_commodity_historical_data(commodity='gold', from_date='01/01/2018', to_date='01/01/2019')
        >>> data.head()
                      Open    High     Low   Close  Volume Currency
        Date
        2018-01-01  1305.8  1309.7  1304.6  1308.7       0      USD
        2018-01-02  1370.5  1370.5  1370.5  1370.5      97      USD
        2018-01-03  1372.0  1372.0  1369.0  1374.2      22      USD
        2018-01-04  1363.4  1375.6  1362.7  1377.4      13      USD
        2018-01-05  1377.8  1377.8  1377.8  1378.4      10      USD

    """

    if not commodity:
        raise ValueError(
            "ERR#0078: commodity parameter is mandatory and must be a valid commodity"
            " name."
        )

    if not isinstance(commodity, str):
        raise ValueError(
            "ERR#0078: commodity parameter is mandatory and must be a valid commodity"
            " name."
        )

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

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

    commodity = unidecode(commodity.strip().lower())

    if commodity not in list(commodities["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0079: commodity " + commodity + " not found, check if it is correct."
        )

    if country is None:
        found_commodities = commodities[
            commodities["name"].apply(unidecode).str.lower() == commodity
        ]

        if len(found_commodities) > 1:
            msg = (
                "Note that the displayed commodity data can differ depending on the"
                " country. If you want to retrieve "
                + commodity
                + " data from either "
                + " or ".join(found_commodities["country"].tolist())
                + ", specify the country parameter."
            )
            warnings.warn(msg, Warning)

        del found_commodities
    else:
        country = unidecode(country.strip().lower())

        if country not in list(set(commodities["country"].str.lower())):
            raise RuntimeError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        commodities = commodities[commodities["country"] == country]

    full_name = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(),
        "full_name",
    ]
    id_ = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(), "id"
    ]
    name = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(), "name"
    ]

    currency = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(),
        "currency",
    ]

    header = full_name + " Historical Data"

    final = list()

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
                if elements_.xpath(".//td")[0].text_content() == "No results found":
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError(
                            "ERR#0080: commodity information unavailable or not found."
                        )
                else:
                    data_flag = True

                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get("data-real-value"))

                if data_flag is True:
                    commodity_date = datetime.strptime(
                        str(
                            datetime.fromtimestamp(
                                int(info[0]), tz=pytz.timezone("GMT")
                            ).date()
                        ),
                        "%Y-%m-%d",
                    )

                    commodity_close = float(info[1].replace(",", ""))
                    commodity_open = float(info[2].replace(",", ""))
                    commodity_high = float(info[3].replace(",", ""))
                    commodity_low = float(info[4].replace(",", ""))

                    commodity_volume = int(info[5])

                    result.insert(
                        len(result),
                        Data(
                            commodity_date,
                            commodity_open,
                            commodity_high,
                            commodity_low,
                            commodity_close,
                            commodity_volume,
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
                    json_list = [value.commodity_as_json() for value in result]

                    final.append(json_list)
                elif as_json is False:
                    df = pd.DataFrame.from_records(
                        [value.commodity_to_dict() for value in result]
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


def get_commodity_information(commodity, country=None, as_json=False):
    """
    This function retrieves fundamental financial information from the specified commodity. The retrieved
    information from the commodity can be valuable as it is additional information that can be used combined
    with OHLC values, so to determine financial insights from the company which holds the specified commodity.

    Args:
        commodity (:obj:`str`): name of the commodity to retrieve information from.
        country (:obj:`str`, optional):
            name of the country to retrieve the commodity information from (if there is more than one country
            that provides data from the same commodity).
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`pandas.DataFrame` or :obj:`dict`- commodity_information:
            The resulting :obj:`pandas.DataFrame` contains the information fields retrieved from Investing.com
            from the specified commodity; it can also be returned as a :obj:`dict`, if argument `as_json=True`.

            If any of the information fields could not be retrieved, that field/s will be filled with
            None values. If the retrieval process succeeded, the resulting :obj:`dict` will look like::

                commodity_information = {
                    "1-Year Change": "16.15%",
                    "52 wk Range": "1,270.2 - 1,566.2",
                    "Base Symbol": "GC",
                    "Commodity Name": "Gold",
                    "Contract Size": "100 Troy Ounces",
                    "Last Rollover Day": "24/11/2019",
                    "Month": "Feb 20",
                    "Months": "GJMQVZ",
                    "Open": 1479.8,
                    "Point Value": "$100",
                    "Prev. Close": 1481.2,
                    "Settlement Day": "25/01/2020",
                    "Settlement Type": "Physical",
                    "Tick Size": 0.1,
                    "Tick Value": 10.0,
                    "Day's Range": "1,477.55 - 1,484.25"
                }

    Raises:
        ValueError: raised if any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if `commodities.csv` file was not found or errored.
        IOError: raised if commodities.csv file is empty or errored.
        RuntimeError: raised if scraping process failed while running.
        ConnectionError: raised if the connection to Investing.com errored (did not return HTTP 200)

    """

    if not commodity:
        raise ValueError(
            "ERR#0078: commodity parameter is mandatory and must be a valid commodity"
            " name."
        )

    if not isinstance(commodity, str):
        raise ValueError(
            "ERR#0078: commodity parameter is mandatory and must be a valid commodity"
            " name."
        )

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

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

    commodity = unidecode(commodity.strip().lower())

    if commodity not in list(commodities["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0079: commodity " + commodity + " not found, check if it is correct."
        )

    if country is None:
        found_commodities = commodities[
            commodities["name"].apply(unidecode).str.lower() == commodity
        ]

        if len(found_commodities) > 1:
            msg = (
                "Note that the displayed commodity information can differ depending on"
                " the country. If you want to retrieve "
                + commodity
                + " data from either "
                + " or ".join(found_commodities["country"].tolist())
                + ", specify the country parameter."
            )
            warnings.warn(msg, Warning)

        del found_commodities
    else:
        country = unidecode(country.strip().lower())

        if country not in list(set(commodities["country"].str.lower())):
            raise RuntimeError(
                "ERR#0034: country " + country + " not found, check if it is correct."
            )

        commodities = commodities[commodities["country"] == country]

    name = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(), "name"
    ]
    tag = commodities.loc[
        (commodities["name"].apply(unidecode).str.lower() == commodity).idxmax(), "tag"
    ]

    url = "https://www.investing.com/commodities/" + tag

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
    path_ = root_.xpath("//dl[@data-test='key-info']/div")

    result = pd.DataFrame(
        columns=[
            "Commodity Name",
            "Prev. Close",
            "Month",
            "Tick Size",
            "Open",
            "Contract Size",
            "Tick Value",
            "Day's Range",
            "Settlement Type",
            "Base Symbol",
            "52 wk Range",
            "Settlement Day",
            "Point Value",
            "1-Year Change",
            "Last Rollover Day",
            "Months",
        ]
    )
    result.at[0, "Commodity Name"] = name

    if not path_:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    for elements_ in path_:
        title_ = elements_.xpath(".//dt")[0].text_content()
        element = elements_.xpath(".//dd")[0]
        if title_ in result.columns.tolist():
            try:
                result.at[0, title_] = float(element.text_content().replace(",", ""))
                continue
            except:
                pass
            try:
                text = element.text_content().strip()
                result.at[0, title_] = datetime.strptime(text, "%m/%d/%Y").strftime(
                    "%d/%m/%Y"
                )
                continue
            except:
                pass
            try:
                text = element.text_content().strip()
                if text.__contains__("1 = "):
                    result.at[0, title_] = text.replace("1 = ", "")
                    continue
            except:
                pass
            try:
                value = element.text_content().strip()
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


def get_commodities_overview(group, as_json=False, n_results=100):
    """
    This function retrieves an overview containing all the real time data available for the main commodities from
    every commodity group (metals, softs, meats, energy and grains), such as the names, symbols, current value, etc.
    as indexed in Investing.com. So on, the main usage of this function is to get an overview on the main commodities
    from a group, so to get a general view. Note that since this function is retrieving a lot of information at once,
    by default just the overview of the Top 100 commodities is being retrieved, but an additional parameter called n_results
    can be specified so to retrieve N results. Anyways, note that in commodities case, there are just a few ones available.

    Args:
        group (:obj:`str`): name of the commodity group to retrieve an overview from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        n_results (:obj:`int`, optional): number of results to be displayed on the overview table (0-1000).

    Returns:
        :obj:`pandas.DataFrame` - commodities_overview:
            The resulting :obj:`pandas.DataFrame` contains all the data available in Investing.com of the main commodities
            from a commodity group in order to get an overview of it.

            If the retrieval process succeeded, the resulting :obj:`pandas.DataFrame` should look like::

                country | name | last | last_close | high | low | change | change_percentage | currency
                --------|------|------|------------|------|-----|--------|-------------------|----------
                xxxxxxx | xxxx | xxxx | xxxxxxxxxx | xxxx | xxx | xxxxxx | xxxxxxxxxxxxxxxxx | xxxxxxxx

    Raises:
        ValueError: raised if any of the introduced arguments errored.
        FileNotFoundError: raised if `commodities.csv` file is missing.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError:
            raised either if the introduced group does not match any of the listed ones or if no overview results could be
            retrieved from Investing.com.
        ConnectionError: raised if GET requests does not return 200 status code.

    """

    if group is None:
        raise ValueError("ERR#0090: group can not be None, it should be a str.")

    if group is not None and not isinstance(group, str):
        raise ValueError("ERR#0090: group can not be None, it should be a str.")

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

    group = unidecode(group.strip().lower())

    if group not in get_commodity_groups():
        raise RuntimeError("ERR#0091: specified commodity group value is not valid.")

    commodities = commodities[commodities["group"] == group]

    head = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/commodities/" + group

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root_ = fromstring(req.text)
    table = root_.xpath(".//table[@id='cross_rate_1']/tbody/tr")

    results = list()

    if len(table) > 0:
        for row in table[:n_results]:
            id_ = row.get("id").replace("pair_", "")
            country_check = (
                row.xpath(".//td[@class='flag']/span")[0].get("title").lower()
            )

            name = (
                row.xpath(".//td[contains(@class, 'elp')]/a")[0].text_content().strip()
            )

            pid = "pid-" + id_

            last = row.xpath(".//td[@class='" + pid + "-last']")[0].text_content()
            last_close = row.xpath(".//td[@class='" + pid + "-last_close']")[
                0
            ].text_content()
            high = row.xpath(".//td[@class='" + pid + "-high']")[0].text_content()
            low = row.xpath(".//td[@class='" + pid + "-low']")[0].text_content()

            pc = row.xpath(".//td[contains(@class, '" + pid + "-pc')]")[
                0
            ].text_content()
            pcp = row.xpath(".//td[contains(@class, '" + pid + "-pcp')]")[
                0
            ].text_content()

            data = {
                "country": country_check if country_check != "" else None,
                "name": name,
                "last": float(last.replace(",", "")),
                "last_close": float(last_close.replace(",", "")),
                "high": float(high.replace(",", "")),
                "low": float(low.replace(",", "")),
                "change": pc,
                "change_percentage": pcp,
                "currency": commodities.loc[
                    (
                        (commodities["name"] == name)
                        & (commodities["country"] == country_check)
                    ).idxmax(),
                    "currency",
                ]
                if country_check != ""
                else commodities.loc[
                    (commodities["name"] == name).idxmax(), "currency"
                ],
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


def search_commodities(by, value):
    """
    This function searches commodities by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced one for the specified field which is the
    `commodities.csv` column name to search in. Available fields to search commodities are 'name', 'full_name' and 'title'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name which can be: ''name', 'full_name' or 'title'.
        value (:obj:`str`): value of the field to search for, which is the value that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting :obj:`pandas.DataFrame` contains the search results from the given query, which is
            any match of the specified value in the specified field. If there are no results for the given query,
            an error will be raised, but otherwise the resulting :obj:`pandas.DataFrame` will contain all the
            available commodities that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        FileNotFoundError: raised if `commodities.csv` file is missing.
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

    available_search_fields = commodities.columns.tolist()

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError(
            "ERR#0026: the introduced field to search can either just be "
            + " or ".join(available_search_fields)
        )

    commodities["matches"] = commodities[by].str.contains(value, case=False)

    search_result = commodities.loc[commodities["matches"] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError(
            "ERR#0043: no results were found for the introduced " + str(by) + "."
        )

    search_result.drop(columns=["matches"], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
