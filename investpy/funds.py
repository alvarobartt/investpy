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

from .data.funds_data import (
    fund_countries_as_list,
    funds_as_df,
    funds_as_dict,
    funds_as_list,
)
from .utils.data import Data
from .utils.extra import random_user_agent


def get_funds(country=None):
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

    return funds_as_df(country=country)


def get_funds_list(country=None):
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

    return funds_as_list(country=country)


def get_funds_dict(country=None, columns=None, as_json=False):
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

    return funds_as_dict(country=country, columns=columns, as_json=as_json)


def get_fund_countries():
    """
    This function retrieves all the country names indexed in Investing.com with available funds to retrieve data
    from, via reading the `fund_countries.csv` file from the resources directory. So on, this function will display a
    listing containing a set of countries, in order to let the user know which countries are taken into account and also
    the return listing from this function can be used for country param check if needed.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with funds as indexed in Investing.com

    Raises:
        FileNotFoundError: raised when the `fund_countries.csv` file was not found.
        IndexError: raised if `fund_countries.csv` file was unavailable or not found.

    """

    return fund_countries_as_list()


def get_fund_recent_data(
    fund, country, as_json=False, order="ascending", interval="Daily"
):
    """
    This function retrieves recent historical data from the introduced `fund` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        fund (:obj:`str`): name of the fund to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the introduced fund is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified fund via argument. The dataset contains the open, high, low and close
            values for the selected fund on market days.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Currency
                -----||------|------|-----|-------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: funds object/file not found or unable to retrieve.
        RuntimeError: introduced fund does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.

    Examples:
        >>> data = investpy.get_fund_recent_data(fund='bbva multiactivo conservador pp', country='spain')
        >>> data.head()
                     Open   High    Low  Close Currency
        Date
        2019-08-13  1.110  1.110  1.110  1.110      EUR
        2019-08-16  1.109  1.109  1.109  1.109      EUR
        2019-08-19  1.114  1.114  1.114  1.114      EUR
        2019-08-20  1.112  1.112  1.112  1.112      EUR
        2019-08-21  1.115  1.115  1.115  1.115      EUR

    """

    if not fund:
        raise ValueError(
            "ERR#0029: fund parameter is mandatory and must be a valid fund name."
        )

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

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
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    country = unidecode(country.strip().lower())

    if country not in get_fund_countries():
        raise RuntimeError(
            "ERR#0034: country " + country + " not found, check if it is correct."
        )

    funds = funds[funds["country"].str.lower() == country]

    fund = unidecode(fund.strip().lower())

    if fund not in list(funds["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0019: fund " + fund + " not found, check if it is correct."
        )

    symbol = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "symbol"
    ]
    id_ = funds.loc[(funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "id"]
    name = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "name"
    ]
    fund_currency = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "currency"
    ]

    header = symbol + " Historical Data"

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
                raise IndexError("ERR#0008: fund information unavailable or not found.")

            info = []

            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.get("data-real-value"))

            fund_date = datetime.strptime(
                str(
                    datetime.fromtimestamp(int(info[0]), tz=pytz.timezone("GMT")).date()
                ),
                "%Y-%m-%d",
            )

            fund_close = float(info[1].replace(",", ""))
            fund_open = float(info[2].replace(",", ""))
            fund_high = float(info[3].replace(",", ""))
            fund_low = float(info[4].replace(",", ""))

            result.insert(
                len(result),
                Data(
                    fund_date,
                    fund_open,
                    fund_high,
                    fund_low,
                    fund_close,
                    None,
                    fund_currency,
                    None,
                ),
            )

        if order in ["ascending", "asc"]:
            result = result[::-1]
        elif order in ["descending", "desc"]:
            result = result

        if as_json is True:
            json_ = {"name": name, "recent": [value.fund_as_json() for value in result]}

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.fund_to_dict() for value in result])
            df.set_index("Date", inplace=True)

            return df
    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_fund_historical_data(
    fund,
    country,
    from_date,
    to_date,
    as_json=False,
    order="ascending",
    interval="Daily",
):
    """
    This function retrieves historical data from the introduced `fund` from Investing
    via Web Scraping on the introduced date range. The resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` object with `ascending` or `descending` order.

    Args:
        fund (:obj:`str`): name of the fund to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the introduced fund is.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        interval (:obj:`str`, optional):
            value to define the historical data interval to retrieve, by default `Daily`, but it can also be `Weekly` or `Monthly`.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns a either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified fund via argument. The dataset contains the open, high, low and close
            values for the selected fund on market days.

            The returned data is case we use default arguments will look like::

                Date || Open | High | Low | Close | Currency
                -----||------|------|-----|-------|----------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: funds object/file not found or unable to retrieve.
        RuntimeError: introduced fund does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if fund information was unavailable or not found.

    Examples:
        >>> data = investpy.get_fund_historical_data(fund='bbva multiactivo conservador pp', country='spain', from_date='01/01/2010', to_date='01/01/2019')
        >>> data.head()
                     Open   High    Low  Close Currency
        Date
        2018-02-15  1.105  1.105  1.105  1.105      EUR
        2018-02-16  1.113  1.113  1.113  1.113      EUR
        2018-02-17  1.113  1.113  1.113  1.113      EUR
        2018-02-18  1.113  1.113  1.113  1.113      EUR
        2018-02-19  1.111  1.111  1.111  1.111      EUR

    """

    if not fund:
        raise ValueError(
            "ERR#0029: fund parameter is mandatory and must be a valid fund name."
        )

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

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
            "ERR#0011: incorrect start date format, it should be 'dd/mm/yyyy'."
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
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    country = unidecode(country.strip().lower())

    if country not in get_fund_countries():
        raise RuntimeError(
            "ERR#0034: country " + country + " not found, check if it is correct."
        )

    funds = funds[funds["country"].str.lower() == country]

    fund = unidecode(fund.strip().lower())

    if fund not in list(funds["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0019: fund " + fund + " not found, check if it is correct."
        )

    symbol = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "symbol"
    ]
    id_ = funds.loc[(funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "id"]
    name = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "name"
    ]
    fund_currency = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "currency"
    ]

    final = list()

    header = symbol + " Historical Data"

    for index in range(len(date_interval["intervals"])):
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
                            "ERR#0008: fund information unavailable or not found."
                        )
                else:
                    data_flag = True

                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.get("data-real-value"))

                if data_flag is True:
                    fund_date = datetime.strptime(
                        str(
                            datetime.fromtimestamp(
                                int(info[0]), tz=pytz.timezone("GMT")
                            ).date()
                        ),
                        "%Y-%m-%d",
                    )

                    fund_close = float(info[1].replace(",", ""))
                    fund_open = float(info[2].replace(",", ""))
                    fund_high = float(info[3].replace(",", ""))
                    fund_low = float(info[4].replace(",", ""))

                    result.insert(
                        len(result),
                        Data(
                            fund_date,
                            fund_open,
                            fund_high,
                            fund_low,
                            fund_close,
                            None,
                            fund_currency,
                            None,
                        ),
                    )

            if data_flag is True:
                if order in ["ascending", "asc"]:
                    result = result[::-1]
                elif order in ["descending", "desc"]:
                    result = result

                if as_json is True:
                    json_list = [value.fund_as_json() for value in result]

                    final.append(json_list)
                elif as_json is False:
                    df = pd.DataFrame.from_records(
                        [value.fund_to_dict() for value in result]
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


def get_fund_information(fund, country, as_json=False):
    """
    This function retrieves basic financial information from the specified fund. Retrieved information
    from the fund can be valuable as it is additional information that can be used combined with OHLC
    values, so to determine financial insights from the company which holds the specified fund.

    Args:
        fund (:obj:`str`): name of the fund to retrieve the financial information from.
        country (:obj:`str`): name of the country from where the introduced fund is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`pandas.DataFrame` or :obj:`dict`- fund_information:
            The resulting :obj:`pandas.DataFrame` contains the information fields retrieved from Investing.com
            from the specified fund; it can also be returned as a :obj:`dict`, if argument `as_json=True`.

            If any of the information fields could not be retrieved, that field/s will be filled with
            None values. If the retrieval process succeeded, the resulting :obj:`dict` will look like::

                fund_information = {
                    'Fund Name': fund_name,
                    'Rating': rating,
                    '1-Year Change': year_change,
                    'Previous Close': prev_close,
                    'Risk Rating': risk_rating,
                    'TTM Yield': ttm_yield,
                    'ROE': roe,
                    'Issuer': issuer,
                    'Turnover': turnover,
                    'ROA': row,
                    'Inception Date': inception_date,
                    'Total Assets': total_assets,
                    'Expenses': expenses,
                    'Min Investment': min_investment,
                    'Market Cap': market_cap,
                    'Category': category
                }

    """

    if not fund:
        raise ValueError(
            "ERR#0029: fund parameter is mandatory and must be a valid fund name."
        )

    if not isinstance(fund, str):
        raise ValueError("ERR#0028: fund argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

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
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    country = unidecode(country.strip().lower())

    if country not in get_fund_countries():
        raise RuntimeError(
            "ERR#0034: country " + country + " not found, check if it is correct."
        )

    funds = funds[funds["country"] == country]

    fund = unidecode(fund.strip().lower())

    if fund not in list(funds["name"].apply(unidecode).str.lower()):
        raise RuntimeError(
            "ERR#0019: fund " + fund + " not found, check if it is correct."
        )

    tag = funds.loc[
        (funds["name"].apply(unidecode).str.lower() == fund).idxmax(), "tag"
    ]

    url = "https://www.investing.com/funds/" + tag

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
            "Fund Name",
            "Rating",
            "1-Year Change",
            "Previous Close",
            "Risk Rating",
            "TTM Yield",
            "ROE",
            "Issuer",
            "Turnover",
            "ROA",
            "Inception Date",
            "Total Assets",
            "Expenses",
            "Min Investment",
            "Market Cap",
            "Category",
        ]
    )

    result.at[0, "Fund Name"] = fund

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


def get_funds_overview(country, as_json=False, n_results=100):
    """
    This function retrieves an overview containing all the real time data available for the main funds from a country,
    such as the names, symbols, current value, etc. as indexed in Investing.com. So on, the main usage of this
    function is to get an overview on the main funds from a country, so to get a general view. Note that since
    this function is retrieving a lot of information at once, by default just the overview of the Top 100 funds
    is being retrieved, but an additional parameter called n_results can be specified so to retrieve N results.

    Args:
        country (:obj:`str`): name of the country to retrieve the funds overview from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        n_results (:obj:`int`, optional): number of results to be displayed on the overview table (0-1000).

    Returns:
        :obj:`pandas.DataFrame` - funds_overview:
            The resulting :obj:`pandas.DataFrame` contains all the data available in Investing.com of the main ETFs
            from a country in order to get an overview of it.

            If the retrieval process succeeded, the resulting :obj:`pandas.DataFrame` should look like::

                country | name | symbol | last | change | total_assets
                --------|------|--------|------|--------|--------------
                xxxxxxx | xxxx | xxxxxx | xxxx | xxxxxx | xxxxxxxxxxxx

    Raises:
        ValueError: raised if there was any argument error.
        FileNotFoundError: raised when `funds.csv` file is missing.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError:
            raised either if the introduced country does not match any of the listed ones or if no overview results could be
            retrieved from Investing.com.
        ConnectionError: raised if GET requests does not return 200 status code.

    """

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

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
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    country = unidecode(country.strip().lower())

    if country not in get_fund_countries():
        raise RuntimeError("ERR#0025: specified country value is not valid.")

    funds = funds[funds["country"] == country]

    if country.lower() == "united states":
        country = "usa"
    elif country.lower() == "united kingdom":
        country = "uk"

    head = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = (
        "https://www.investing.com/funds/"
        + country.replace(" ", "-")
        + "-funds?&issuer_filter=0"
    )

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root_ = fromstring(req.text)
    table = root_.xpath(".//table[@id='etfs']/tbody/tr")

    results = list()

    if len(table) > 0:
        for row in table[:n_results]:
            id_ = row.get("id").replace("pair_", "")
            symbol = row.xpath(".//td[contains(@class, 'symbol')]")[0].get("title")

            nested = row.xpath(".//a")[0]
            name = nested.get("title").rstrip()
            full_name = nested.text.strip()

            country_flag = row.xpath(".//td[@class='flag']/span")[0].get("title")
            country_flag = unidecode(country_flag.lower())

            last_path = ".//td[@class='" + "pid-" + str(id_) + "-last" + "']"
            last = row.xpath(last_path)[0].text_content()

            if last == "":
                continue

            change_path = (
                ".//td[contains(@class, '" + "pid-" + str(id_) + "-pcp" + "')]"
            )
            change = row.xpath(change_path)[0].text_content()

            total_assets_path = change_path
            total_assets = row.xpath(total_assets_path)[0].getnext().text_content()

            if total_assets == "":
                total_assets = 0
            else:
                if total_assets.__contains__("K"):
                    total_assets = (
                        float(total_assets.replace("K", "").replace(",", "")) * 1e3
                    )
                elif total_assets.__contains__("M"):
                    total_assets = (
                        float(total_assets.replace("M", "").replace(",", "")) * 1e6
                    )
                elif total_assets.__contains__("B"):
                    total_assets = (
                        float(total_assets.replace("B", "").replace(",", "")) * 1e9
                    )
                else:
                    total_assets = float(total_assets.replace(",", ""))

            data = {
                "country": country_flag,
                "name": name,
                "full_name": full_name,
                "symbol": symbol,
                "last": float(last.replace(",", "")),
                "change": change,
                "total_assets": int(total_assets),
                "currency": funds.loc[(funds["name"] == name).idxmax(), "currency"],
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


def search_funds(by, value):
    """
    This function searches funds by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced value for the specified field which is the
    `funds.csv` column name to search in. Available fields to search funds are 'name', 'symbol', 'issuer' and 'isin'.

    Args:
        by (:obj:`str`):
            name of the field to search for, which is the column name ('name', 'symbol', 'issuer' or 'isin').
        value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
            in the specified field). If there are no results and error will be raised, but otherwise this
            `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced params is not valid or errored.
        FileNotFoundError: raised if `funds.csv` file is missing.
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
    resource_path = "/".join(("resources", "funds.csv"))
    if pkg_resources.resource_exists(resource_package, resource_path):
        funds = pd.read_csv(
            pkg_resources.resource_filename(resource_package, resource_path),
            keep_default_na=False,
        )
    else:
        raise FileNotFoundError("ERR#0057: funds file not found or errored.")

    if funds is None:
        raise IOError("ERR#0005: funds object not found or unable to retrieve.")

    funds.drop(columns=["tag", "id"], inplace=True)

    available_search_fields = funds.columns.tolist()

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError(
            "ERR#0026: the introduced field to search can either just be "
            + " or ".join(available_search_fields)
        )

    funds["matches"] = funds[by].str.contains(value, case=False)

    search_result = funds.loc[funds["matches"] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError(
            "ERR#0043: no results were found for the introduced " + str(by) + "."
        )

    search_result.drop(columns=["matches"], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
