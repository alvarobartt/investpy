# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import pandas as pd
import pkg_resources
import requests
from lxml.html import fromstring
from unidecode import unidecode

from .utils import constant as cst
from .utils.extra import random_user_agent, resource_to_data


def technical_indicators(name, country, product_type, interval="daily"):
    """
    This function retrieves the technical indicators values calculated by Investing.com for every financial product
    available (stocks, funds, etfs, indices, currency crosses, bonds, certificates and commodities) for different
    time intervals. So on, the user must provide the product_type name and the name of the product (unless product_type
    is 'stock' which name value will be the stock's symbol) and the country if required (mandatory unless product_type
    is either 'currency_cross' or 'commodity', where it must be None). Additionally, the interval can be specified
    which defines the update frequency of the calculations of the technical indicators (mainly momentum indicators).

    Args:
        name (:obj:`str`):
            name of the product to retrieve the technical indicators table from (if product_type is `stock`, its value
            must be the stock's symbol not the name).
        country (:obj:`str`):
            country name of the introduced product if applicable (if product_type is either `currency_cross` or `commodity`
            this parameter should be None, unless it can be specified just for `commodity` product_type).
        product_type (:obj:`str`):
            identifier of the introduced product, available ones are: `stock`, `fund`, `etf`, `index`, `currency_cross`,
            `bond`, `certificate` and `commodity`.
        interval (:obj:`str`):
            time interval of the resulting calculations, available values are: `5mins`, `15mins`, `30mins`, `1hour`,
            `5hours`, `daily`, `weekly` and `monthly`.

    Returns:
        :obj:`pandas.DataFrame` - technical_indicators:
            The resulting :obj:`pandas.DataFrame` contains the table with the results of the calculation of the technical
            indicators made by Investing.com for the introduced financial product. So on, if the retrieval process succeed
            its result will look like::

                 technical_indicator | value | signal
                ---------------------|-------|--------
                 xxxxxxxxxxxxxxxxxxx | xxxxx | xxxxxx

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        ConnectionError: raised if the connection to Investing.com errored or could not be established.

    Examples:
        >>> data = investpy.technical_indicators(name='bbva', country='spain', product_type='stock', interval='daily')
        >>> data.head()
            technical_indicator    value           signal
        0               RSI(14)  39.1500             sell
        1            STOCH(9,6)  33.2340             sell
        2          STOCHRSI(14)  67.7390              buy
        3           MACD(12,26)  -0.0740             sell
        4               ADX(14)  55.1150             sell
        5           Williams %R -66.6670             sell
        6               CCI(14) -77.1409             sell
        7               ATR(14)   0.0939  less_volatility
        8        Highs/Lows(14)  -0.0199             sell
        9   Ultimate Oscillator  43.0010             sell
        10                  ROC  -6.6240             sell
        11  Bull/Bear Power(13)  -0.1590             sell

    """

    if not name:
        raise ValueError(
            "ERR#0116: the parameter name must be specified and must be a string."
        )

    if not isinstance(name, str):
        raise ValueError(
            "ERR#0116: the parameter name must be specified and must be a string."
        )

    if country is not None and not isinstance(country, str):
        raise ValueError(
            "ERR#0117: this parameter can just be None or a string, if required."
        )

    if not product_type:
        raise ValueError(
            "ERR#0118: product_type value is mandatory and must be a string."
        )

    if not isinstance(product_type, str):
        raise ValueError(
            "ERR#0118: product_type value is mandatory and must be a string."
        )

    if not interval:
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    product_type = unidecode(product_type.lower().strip())

    if product_type not in cst.PRODUCT_TYPE_FILES.keys():
        raise ValueError(
            "ERR#0119: introduced product_type value does not exist. Available values"
            " are: " + ", ".join(cst.PRODUCT_TYPE_FILES.keys())
        )

    if interval:
        if interval not in cst.INTERVAL_FILTERS.keys():
            raise ValueError(
                "ERR#0120: introduced interval value does not exist. Available values"
                " are: " + ", ".join(cst.INTERVAL_FILTERS.keys())
            )

    data = resource_to_data(path_to_data=cst.PRODUCT_TYPE_FILES[product_type])

    if product_type not in ["currency_cross"]:
        if country is not None:
            country = unidecode(country.lower().strip())

            if country not in list(set(data["country"].str.lower())):
                raise ValueError(
                    "ERR#0124: introduced country does not exist or is not available."
                )

            data = data[data["country"] == country]
        else:
            if product_type != "commodity":
                raise ValueError(
                    "ERR#0123: country parameter is required with the introduced"
                    " product_type."
                )

    if product_type == "stock":
        check = "symbol"
    else:
        check = "name"

    name = unidecode(name.lower().strip())

    if name not in list(data[check].apply(unidecode).str.lower()):
        raise ValueError(
            "ERR#0122: introduced name does not exist in the introduced country (if"
            " required)."
        )

    product_id = data.loc[
        (data[check].apply(unidecode).str.lower() == name).idxmax(), "id"
    ]

    data_values = {
        "pairID": product_id,
        "period": cst.INTERVAL_FILTERS[interval],
        "viewType": "normal",
    }

    headers = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root = fromstring(req.text)
    table = root.xpath(".//table[contains(@class, 'technicalIndicatorsTbl')]/tbody/tr")

    tech_indicators = list()

    for row in table:
        for value in row.xpath("td"):
            if value.get("class").__contains__("symbol"):
                tech_ind = value.text_content().strip()
                tech_val = float(value.getnext().text_content().strip())
                tech_sig = value.getnext().getnext().text_content().strip().lower()

                tech_indicators.append(
                    {
                        "technical_indicator": tech_ind,
                        "value": tech_val,
                        "signal": tech_sig.replace(" ", "_"),
                    }
                )

    return pd.DataFrame(tech_indicators)


def moving_averages(name, country, product_type, interval="daily"):
    """
    This function retrieves the moving averages values calculated by Investing.com for every financial product
    available (stocks, funds, etfs, indices, currency crosses, bonds, certificates and commodities) for different
    time intervals. So on, the user must provide the product_type name and the name of the product (unless product_type
    is 'stock' which name value will be the stock's symbol) and the country if required (mandatory unless product_type
    is either 'currency_cross' or 'commodity', where it must be None). Additionally, the interval can be specified
    which defines the update frequency of the calculations of the moving averages (both simple and exponential). Note
    that the specified interval is not the moving average's interval, since all the available time frames used on
    the calculation of the moving averages are retrieved.

    Args:
        name (:obj:`str`):
            name of the product to retrieve the moving averages table from (if product_type is `stock`, its value
            must be the stock's symbol not the name).
        country (:obj:`str`):
            country name of the introduced product if applicable (if product_type is either `currency_cross` or `commodity`
            this parameter should be None, unless it can be specified just for `commodity` product_type).
        product_type (:obj:`str`):
            identifier of the introduced product, available ones are: `stock`, `fund`, `etf`, `index`, `currency_cross`,
            `bond`, `certificate` and `commodity`.
        interval (:obj:`str`):
            time interval of the resulting calculations, available values are: `5mins`, `15mins`, `30mins`, `1hour`,
            `5hours`, `daily`, `weekly` and `monthly`.

    Returns:
        :obj:`pandas.DataFrame` - moving_averages:
            The resulting :obj:`pandas.DataFrame` contains the table with the results of the calculation of the moving averages
            made by Investing.com for the introduced financial product. So on, if the retrieval process succeed
            its result will look like::

                 period | sma_value | sma_signal | ema_value | ema_signal
                --------|-----------|------------|-----------|------------
                 xxxxxx | xxxxxxxxx | xxxxxxxxxx | xxxxxxxxx | xxxxxxxxxx

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        ConnectionError: raised if the connection to Investing.com errored or could not be established.

    Examples:
        >>> data = investpy.moving_averages(name='bbva', country='spain', product_type='stock', interval='daily')
        >>> data.head()
          period  sma_value sma_signal  ema_value ema_signal
        0      5      4.615        buy      4.650        buy
        1     10      4.675       sell      4.693       sell
        2     20      4.817       sell      4.763       sell
        3     50      4.859       sell      4.825       sell
        4    100      4.809       sell      4.830       sell
        5    200      4.822       sell      4.867       sell

    """

    if not name:
        raise ValueError(
            "ERR#0116: the parameter name must be specified and must be a string."
        )

    if not isinstance(name, str):
        raise ValueError(
            "ERR#0116: the parameter name must be specified and must be a string."
        )

    if country is not None and not isinstance(country, str):
        raise ValueError(
            "ERR#0117: this parameter can just be None or a string, if required."
        )

    if not product_type:
        raise ValueError(
            "ERR#0118: product_type value is mandatory and must be a string."
        )

    if not isinstance(product_type, str):
        raise ValueError(
            "ERR#0118: product_type value is mandatory and must be a string."
        )

    if not interval:
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    product_type = unidecode(product_type.lower().strip())

    if product_type not in cst.PRODUCT_TYPE_FILES.keys():
        raise ValueError(
            "ERR#0119: introduced product_type value does not exist. Available values"
            " are: " + ", ".join(cst.PRODUCT_TYPE_FILES.keys())
        )

    if interval:
        if interval not in cst.INTERVAL_FILTERS.keys():
            raise ValueError(
                "ERR#0120: introduced interval value does not exist. Available values"
                " are: " + ", ".join(cst.INTERVAL_FILTERS.keys())
            )

    data = resource_to_data(path_to_data=cst.PRODUCT_TYPE_FILES[product_type])

    if product_type not in ["currency_cross"]:
        if country is not None:
            country = unidecode(country.lower().strip())

            if country not in list(set(data["country"].str.lower())):
                raise ValueError(
                    "ERR#0124: introduced country does not exist or is not available."
                )

            data = data[data["country"] == country]
        else:
            if product_type != "commodity":
                raise ValueError(
                    "ERR#0123: country parameter is required with the introduced"
                    " product_type."
                )

    if product_type == "stock":
        check = "symbol"
    else:
        check = "name"

    name = unidecode(name.lower().strip())

    if name not in list(data[check].apply(unidecode).str.lower()):
        raise ValueError(
            "ERR#0122: introduced name does not exist in the introduced country (if"
            " required)."
        )

    product_id = data.loc[
        (data[check].apply(unidecode).str.lower() == name).idxmax(), "id"
    ]

    data_values = {
        "pairID": product_id,
        "period": cst.INTERVAL_FILTERS[interval],
        "viewType": "normal",
    }

    headers = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root = fromstring(req.text)
    table = root.xpath(".//table[contains(@class, 'movingAvgsTbl')]/tbody/tr")

    moving_avgs = list()

    for row in table:
        for value in row.xpath("td"):
            if value.get("class") is not None:
                if value.get("class").__contains__("symbol"):
                    ma_period = value.text_content().strip().replace("MA", "")
                    sma_signal = (
                        value.getnext().xpath("span")[0].text_content().strip().lower()
                    )
                    sma_value = float(
                        value.getnext()
                        .text_content()
                        .lower()
                        .replace(sma_signal, "")
                        .strip()
                    )
                    value = value.getnext()
                    ema_signal = (
                        value.getnext()
                        .xpath(".//span")[0]
                        .text_content()
                        .strip()
                        .lower()
                    )
                    ema_value = float(
                        value.getnext()
                        .text_content()
                        .lower()
                        .replace(ema_signal, "")
                        .strip()
                    )

                    moving_avgs.append(
                        {
                            "period": ma_period,
                            "sma_value": sma_value,
                            "sma_signal": sma_signal,
                            "ema_value": ema_value,
                            "ema_signal": ema_signal,
                        }
                    )

    return pd.DataFrame(moving_avgs)


def pivot_points(name, country, product_type, interval="daily"):
    """
    This function retrieves the pivot points values calculated by Investing.com for every financial product
    available (stocks, funds, etfs, indices, currency crosses, bonds, certificates and commodities) for different
    time intervals. Pivot points are calculated on different levels: three support levels (S) and three resistance
    ones (R). So on, the user must provide the product_type name and the name of the product (unless product_type
    is 'stock' which name value will be the stock's symbol) and the country if required (mandatory unless product_type
    is either 'currency_cross' or 'commodity', where it must be None). Additionally, the interval can be specified
    which defines the update frequency of the calculations of the technical indicators (mainly momentum indicators).

    Args:
        name (:obj:`str`):
            name of the product to retrieve the technical indicators table from (if product_type is `stock`, its value
            must be the stock's symbol not the name).
        country (:obj:`str`):
            country name of the introduced product if applicable (if product_type is either `currency_cross` or `commodity`
            this parameter should be None, unless it can be specified just for `commodity` product_type).
        product_type (:obj:`str`):
            identifier of the introduced product, available ones are: `stock`, `fund`, `etf`, `index`, `currency_cross`,
            `bond`, `certificate` and `commodity`.
        interval (:obj:`str`):
            time interval of the resulting calculations, available values are: `5mins`, `15mins`, `30mins`, `1hour`,
            `5hours`, `daily`, `weekly` and `monthly`.

    Returns:
        :obj:`pandas.DataFrame` - pivot_points:
            The resulting :obj:`pandas.DataFrame` contains the table with the results of the calculation of the pivot
            points made by Investing.com for the introduced financial product. So on, if the retrieval process succeed
            its result will look like::

                 name | s3 | s2 | s1 | pivot_points | r1 | r2 | r3
                ------|----|----|----|--------------|----|----|----
                 xxxx | xx | xx | xx | xxxxxxxxxxxx | xx | xx | xx

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.
        ConnectionError: raised if the connection to Investing.com errored or could not be established.

    Examples:
        >>> data = investpy.pivot_points(name='bbva', country='spain', product_type='stock', interval='daily')
        >>> data.head()
                name     s3     s2     s1  pivot_points     r1     r2     r3
        0    Classic  4.537  4.573  4.620         4.656  4.703  4.739  4.786
        1  Fibonacci  4.573  4.605  4.624         4.656  4.688  4.707  4.739
        2  Camarilla  4.645  4.653  4.660         4.656  4.676  4.683  4.691
        3   Woodie's  4.543  4.576  4.626         4.659  4.709  4.742  4.792
        4   DeMark's    NaN    NaN  4.639         4.665  4.721    NaN    NaN

    """

    if not name:
        raise ValueError(
            "ERR#0116: the parameter name must be specified and must be a string."
        )

    if not isinstance(name, str):
        raise ValueError(
            "ERR#0116: the parameter name must be specified and must be a string."
        )

    if country is not None and not isinstance(country, str):
        raise ValueError(
            "ERR#0117: this parameter can just be None or a string, if required."
        )

    if not product_type:
        raise ValueError(
            "ERR#0118: product_type value is mandatory and must be a string."
        )

    if not isinstance(product_type, str):
        raise ValueError(
            "ERR#0118: product_type value is mandatory and must be a string."
        )

    if not interval:
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    if not isinstance(interval, str):
        raise ValueError("ERR#0121: interval value is mandatory and must be a string.")

    product_type = unidecode(product_type.lower().strip())

    if product_type not in cst.PRODUCT_TYPE_FILES.keys():
        raise ValueError(
            "ERR#0119: introduced product_type value does not exist. Available values"
            " are: " + ", ".join(cst.PRODUCT_TYPE_FILES.keys())
        )

    if interval:
        if interval not in cst.INTERVAL_FILTERS.keys():
            raise ValueError(
                "ERR#0120: introduced interval value does not exist. Available values"
                " are: " + ", ".join(cst.INTERVAL_FILTERS.keys())
            )

    data = resource_to_data(path_to_data=cst.PRODUCT_TYPE_FILES[product_type])

    if product_type not in ["currency_cross"]:
        if country is not None:
            country = unidecode(country.lower().strip())

            if country not in list(set(data["country"].str.lower())):
                raise ValueError(
                    "ERR#0124: introduced country does not exist or is not available."
                )

            data = data[data["country"] == country]
        else:
            if product_type != "commodity":
                raise ValueError(
                    "ERR#0123: country parameter is required with the introduced"
                    " product_type."
                )

    if product_type == "stock":
        check = "symbol"
    else:
        check = "name"

    name = unidecode(name.lower().strip())

    if name not in list(data[check].apply(unidecode).str.lower()):
        raise ValueError(
            "ERR#0122: introduced name does not exist in the introduced country (if"
            " required)."
        )

    product_id = data.loc[
        (data[check].apply(unidecode).str.lower() == name).idxmax(), "id"
    ]

    data_values = {
        "pairID": product_id,
        "period": cst.INTERVAL_FILTERS[interval],
        "viewType": "normal",
    }

    headers = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    url = "https://www.investing.com/instruments/Service/GetTechincalData"

    req = requests.post(url, headers=headers, data=data_values)

    if req.status_code != 200:
        raise ConnectionError(
            "ERR#0015: error " + str(req.status_code) + ", try again later."
        )

    root = fromstring(req.text)
    header = root.xpath(".//table[contains(@class, 'crossRatesTbl')]/thead/tr/th")

    values = dict()

    for index, column in enumerate(header):
        values[index] = column.text_content().strip().lower().replace(" ", "_")

    table = root.xpath(".//table[contains(@class, 'crossRatesTbl')]/tbody/tr")

    pivot_pts = list()

    for row in table:
        pivot_pt = dict()
        elements = row.xpath("td")

        for key, value in values.items():
            if value != "name":
                val = elements[key].text_content().strip()
                try:
                    pivot_pt[value] = float(val)
                except:
                    pivot_pt[value] = None
            else:
                pivot_pt[value] = elements[key].text_content().strip()

        pivot_pts.append(pivot_pt)

    return pd.DataFrame(pivot_pts)
