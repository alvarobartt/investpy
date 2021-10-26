# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

import json
from datetime import date, datetime, timedelta
from random import randint

import pandas as pd
import pytz
import requests
from lxml.html import fromstring

from .constant import FUNDS_INTERVAL_FILTERS, INTERVAL_FILTERS, OUTDATED2UPDATED
from .data import Data
from .extra import random_user_agent


class SearchObj(object):
    """Class which contains each search result when searching data in Investing.com.

    This class contains the search results of the Investing.com search made with the function
    call `investpy.search_quotes(text, products, countries, n_results)` which returns a :obj:`list`
    of instances of this class with the formatted retrieved information. Additionally, data can
    either be retrieved or not including both recent and historical data, which will be included
    in the `SearchObj.data` attribute when calling either `SearchObj.retrieve_recent_data()` or
    `SearchObj.retrieve_historical_data(from_date, to_date)`, respectively.

    Attributes:
        id_ (:obj:`int`): ID value used by Investing.com to retrieve data.
        name (:obj:`str`): name of the retrieved financial product.
        symbol (:obj:`str`): symbol of the retrieved financial product.
        tag (:obj:`str`): tag (which is the Investing.com URL) of the retrieved financial product.
        country (:obj:`str`): name of the country from where the retrieved financial product is.
        pair_type (:obj:`str`): type of retrieved financial product (stocks, funds, etfs, etc.).
        exchange (:obj:`str`): name of the stock exchange of the retrieved financial product.

    Extra Attributes:
        data (:obj:`pandas.DataFrame`):
            recent or historical data to retrieve from the current financial product, generated
            after calling either self.retrieve_recent_data or self.retrieve_historical_data().
        info (:obj:`dict`):
            contains the information of the current financial product, generated after calling the
            self.retrieve_information() function.

    """

    def __init__(self, id_, name, symbol, tag, country, pair_type, exchange):
        self.id_ = id_
        self.name = name
        self.symbol = symbol
        self.country = country
        self.tag = tag
        self.pair_type = pair_type
        self.exchange = exchange

    def __str__(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return self.id_

    def retrieve_recent_data(self):
        """Class method used to retrieve the recent data from the class instance of any financial product.

        This method retrieves the recent data from Investing.com of the financial product of the current class
        instance, so it fills the `SearchObj.data` attribute with the retrieved :obj:`pandas.DataFrame`. This method
        uses the previously filled data from the `investpy.search_quotes(text, products, countries, n_results)` function
        search results to build the request that it is going to be sent to Investing.com so to retrieve and parse the data.

        Returns:
            :obj:`pandas.DataFrame` - data:
                This method retrieves the recent data from the current class instance of a financial product
                from Investing.com. This method both stores retrieved data in self.data attribute of the class
                instance and it also returns it as a normal function will do.

        """

        if self.pair_type in ["stocks", "funds", "etfs", "currencies", "certificates"]:
            header = f"{self.symbol} Historical Data"
            headers, params = self._prepare_request(header)
        elif self.pair_type in ["bonds"]:
            header = f"{self.name} Bond Yield Historical Data"
            headers, params = self._prepare_request(header)
        elif self.pair_type in ["indices", "commodities", "cryptos", "fxfutures"]:
            header = f"{self.name} Historical Data"
            headers, params = self._prepare_request(header)

        self.data = self._data_retrieval(
            product=self.pair_type, headers=headers, params=params
        )
        self._convert2df()
        return self.data

    def retrieve_historical_data(self, from_date, to_date):
        """Class method used to retrieve the historical data from the class instance of any financial product.

        This method retrieves the historical data from Investing.com of the financial product of the current class
        instance on the specified date range, so it fills the `SearchObj.data` attribute with the retrieved
        :obj:`pandas.DataFrame`. This method uses the previously filled data from the
        `investpy.search_quotes(text, products, countries, n_results)` function search results to build the request
        that it is going to be sent to Investing.com so to retrieve and parse the data.

        Args:
            from_date (:obj:`str`): date from which data will be retrieved, specified in dd/mm/yyyy format.
            to_date (:obj:`str`): date until data will be retrieved, specified in dd/mm/yyyy format.

        Returns:
            :obj:`pandas.DataFrame` - data:
                This method retrieves the historical data from the current class instance of a financial product
                from Investing.com. This method both stores retrieved data in self.data attribute of the class
                instance and it also returns it as a normal function will do.

        Raises:
            ValueError: raised if any of the introduced parameters was not valid or errored.
            RuntimeError: raised if there was any error while retrieving the data from Investing.com.

        """

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

        from_date = datetime.strptime(from_date, "%d/%m/%Y")
        to_date = datetime.strptime(to_date, "%d/%m/%Y")

        if from_date >= to_date:
            raise ValueError(
                "ERR#0032: to_date should be greater than from_date, both formatted as"
                " 'dd/mm/yyyy'."
            )

        if self.pair_type in ["stocks", "funds", "etfs", "currencies", "certificates"]:
            header = f"{self.symbol} Historical Data"
        elif self.pair_type in ["bonds"]:
            header = f"{self.name} Bond Yield Historical Data"
        elif self.pair_type in ["indices", "commodities", "cryptos", "fxfutures"]:
            header = f"{self.name} Historical Data"

        if to_date.year - from_date.year > 19:
            intervals = self._calculate_intervals(from_date, to_date)

            self.data = list()

            for interval in intervals:
                headers, params = self._prepare_historical_request(
                    header=header, from_date=interval["from"], to_date=interval["to"]
                )
                try:
                    self.data += self._data_retrieval(
                        product=self.pair_type, headers=headers, params=params
                    )
                except:
                    continue

            if len(self.data) < 1:
                raise IndexError("ERR#0033: information unavailable or not found.")
        else:
            headers, params = self._prepare_historical_request(
                header=header,
                from_date=from_date.strftime("%m/%d/%Y"),
                to_date=to_date.strftime("%m/%d/%Y"),
            )
            self.data = self._data_retrieval(
                product=self.pair_type, headers=headers, params=params
            )

        self._convert2df()
        return self.data

    def retrieve_information(self):
        """Class method used to retrieve the information from the class instance of any financial product.

        This method retrieves the information from Investing.com of the financial product of the current class
        instance, so it fills the `SearchObj.info` attribute with the retrieved :obj:`dict`. This method uses the
        previously retrieved data from the `investpy.search_quotes(text, products, countries, n_results)`
        function search results to build the request that it is going to be sent to Investing.com so to retrieve and
        parse the information, since the product tag is required.

        Returns:
            :obj:`dict` - info:
                This method retrieves the information from the current class instance of a financial product
                from Investing.com. This method both stores retrieved information in self.information attribute of the class
                instance and it also returns it as a normal function will do.

        Raises:
            ConnectionError: raised if connection to Investing.com could not be established.
            RuntimeError: raised if there was any problem while retrieving the data from Investing.com.

        """

        url = f"https://www.investing.com{self.tag}"

        headers = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        req = requests.get(url, headers=headers)

        if req.status_code != 200:
            raise ConnectionError(
                f"ERR#0015: error {req.status_code}, try again later."
            )

        # Just change this list once the update is included for all the other products
        updated_for = ["stocks"]
        outdated_for = [
            "etfs",
            "commodities",
            "currencies",
            "funds",
            "bonds",
            "cryptos",
            "certificates",
            "indices",
            "fxfutures",
        ]

        root_ = fromstring(req.text)
        updated_path = root_.xpath("//dl[@data-test='key-info']/div")
        outdated_path = root_.xpath("//div[contains(@class, 'overviewDataTable')]/div")

        if not updated_path and not outdated_path:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

        path_, investing_updated = (
            (updated_path, True) if updated_path else (outdated_path, False)
        )

        self.information = dict()

        for elements_ in path_:
            if investing_updated:
                element = elements_.xpath(".//dd")[0]
                title = element.get("data-test")
            else:
                element = elements_.xpath(".//span[@class='float_lang_base_1']")[0]
                title = element.text_content().strip()
                title = OUTDATED2UPDATED[title]
                element = element.getnext()
            try:
                value = float(element.text_content().replace(",", ""))
                if isinstance(value, float):
                    if value.is_integer() is True:
                        value = int(value)
                self.information[title] = value if value != "N/A" else None
                continue
            except:
                pass
            try:
                text = element.text_content().strip()
                in_format = "%b %d, %Y" if investing_updated else "%m/%d/%Y"
                text = datetime.strptime(text, in_format).strftime("%d/%m/%Y")
                self.information[title] = text if text != "N/A" else None
                continue
            except:
                pass
            try:
                text = element.text_content().strip()
                if text.__contains__("1 = "):
                    text = text.replace("1 = ", "")
                    self.information[title] = text if text != "N/A" else None
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
                if isinstance(value, float):
                    if value.is_integer() is True:
                        value = int(value)
                self.information[title] = value if value != "N/A" else None
                continue
            except:
                pass

        return self.information

    def retrieve_technical_indicators(self, interval="daily"):
        """Class method used to retrieve the technical indicators from the class instance of any financial product.

        This method retrieves the technical indicators from Investing.com for the financial product of the current
        class instance, to later put in into the `SearchObj.technical_indicators` attribute. This method uses the
        previously retrieved data from the `investpy.search_quotes(text, products, countries, n_results)`
        function search results to build the request that it is going to be sent to Investing.com so to retrieve and
        parse the technical indicators, since the product id is required.

        Args:
            interval (:obj:`str`, optional):
                time interval of the technical indicators' calculations, available values are: `5mins`, `15mins`,
                `30mins`, `1hour`, `5hours`, `daily`, `weekly` and `monthly`. Note that for funds just the intervals:
                `daily`, `weekly` and `monthly` are available.

        Returns:
            :obj:`pd.DataFrame` - technical_indicators:
                This method retrieves the technical indicators from the current class instance of a financial product
                from Investing.com. This method not just stores retrieved technical indicators table into self.technical_indicators
                but it also returns it as a normal function will do.

        Raises:
            ValueError: raised if any of the input parameters is not valid.
            ConnectionError: raised if connection to Investing.com could not be established.
            RuntimeError: raised if there was any problem while retrieving the data from Investing.com.

        """

        if self.pair_type in []:
            raise ValueError(
                "Investing.com does not provide technical indicators for"
                f" {self.pair_type}."
            )

        if self.pair_type != "funds" and interval not in INTERVAL_FILTERS:
            raise ValueError(
                "Investing.com just provides the following intervals for"
                f" {self.pair_type}' technical indicators:"
                f" {', '.join(list(INTERVAL_FILTERS.keys()))}"
            )

        if self.pair_type == "funds" and interval not in FUNDS_INTERVAL_FILTERS:
            raise ValueError(
                "Investing.com just provides the following intervals for funds'"
                " technical indicators:"
                f" {', '.join(list(FUNDS_INTERVAL_FILTERS.keys()))}"
            )

        params = {
            "pairID": self.id_,
            "period": INTERVAL_FILTERS[interval],
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

        req = requests.post(url, headers=headers, data=params)

        if req.status_code != 200:
            raise ConnectionError(
                f"ERR#0015: error {req.status_code}, try again later."
            )

        root_ = fromstring(req.text)
        table_ = root_.xpath(
            ".//table[contains(@class, 'technicalIndicatorsTbl')]/tbody/tr"
        )

        if not table_:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

        self.technical_indicators = pd.DataFrame()

        for row in table_:
            for value in row.xpath("td"):
                if value.get("class").__contains__("symbol"):
                    self.technical_indicators = self.technical_indicators.append(
                        {
                            "indicator": value.text_content().strip(),
                            "value": float(value.getnext().text_content().strip()),
                            "signal": (
                                value.getnext().getnext().text_content().strip().lower()
                            ).replace(" ", "_"),
                        },
                        ignore_index=True,
                    )

        return self.technical_indicators

    def retrieve_currency(self):
        """Class method used to retrieve the default currency from the class instance of any financial product.

        This method retrieves the default currency from Investing.com of the financial product of the current class
        instance. This method uses the data previously retrieved from the `investpy.search_quotes(text, products, countries, n_results)`
        function search results to build the request that it is going to be sent to Investing.com so to retrieve and
        parse the information, since the product tag is required.

        Returns:
            :obj:`str` - default_currency:
                This method retrieves the default currency from the current class instance of a financial product
                from Investing.com.

        Raises:
            ConnectionError: raised if connection to Investing.com could not be established.
            RuntimeError: raised if there was any problem while retrieving the data from Investing.com.

        """

        url = f"https://www.investing.com{self.tag}"

        headers = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        req = requests.get(url, headers=headers)

        if req.status_code != 200:
            raise ConnectionError(
                f"ERR#0015: error {req.status_code}, try again later."
            )

        # Just change this list once the update is included for all the other products
        updated_for = ["stocks"]
        outdated_for = [
            "etfs",
            "commodities",
            "currencies",
            "funds",
            "bonds",
            "cryptos",
            "certificates",
            "indices",
            "fxfutures",
        ]

        root_ = fromstring(req.text)
        updated_path = root_.xpath(
            "//div[contains(@class, 'instrument-metadata_currency')]/span"
        )
        outdated_path = root_.xpath(
            "//div[@id='quotes_summary_current_data']/div/div/div[contains(@class,"
            " 'bottom')]/span[@class='bold']"
        )

        if not updated_path and not outdated_path:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

        path_, investing_updated = (
            (updated_path, True) if updated_path else (outdated_path, False)
        )

        self.default_currency = path_[-1].text_content().strip()
        return self.default_currency

    def _prepare_request(self, header):
        headers = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        params = {
            "curr_id": self.id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data",
        }

        return headers, params

    def _prepare_historical_request(self, header, from_date, to_date):
        headers = {
            "User-Agent": random_user_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        params = {
            "curr_id": self.id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": from_date,
            "end_date": to_date,
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data",
        }

        return headers, params

    def _calculate_intervals(self, from_date, to_date):
        intervals = list()

        while True:
            diff = to_date.year - from_date.year

            if diff > 19:
                intervals.append(
                    {
                        "from": from_date.strftime("%m/%d/%Y"),
                        "to": from_date.replace(year=from_date.year + 19).strftime(
                            "%m/%d/%Y"
                        ),
                    }
                )

                from_date = from_date.replace(year=from_date.year + 19) + timedelta(
                    days=1
                )
            else:
                intervals.append(
                    {
                        "from": from_date.strftime("%m/%d/%Y"),
                        "to": to_date.strftime("%m/%d/%Y"),
                    }
                )

                break

        return intervals

    def _data_retrieval(self, product, headers, params):
        has_volume = (
            True
            if product
            in ["stocks", "etfs", "indices", "cryptos", "commodities", "fxfutures"]
            else False
        )
        has_change_pct = True  # Every financial product has it

        url = "https://www.investing.com/instruments/HistoricalDataAjax"

        req = requests.post(url, headers=headers, data=params)

        if req.status_code != 200:
            raise ConnectionError(
                f"ERR#0015: error {req.status_code}, try again later."
            )

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")

        if not path_:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

        results = list()

        for elements_ in path_:
            info = []

            for nested_ in elements_.xpath(".//td"):
                val = (
                    nested_.get("data-real-value")
                    if nested_.get("data-real-value") is not None
                    else nested_.text_content()
                )
                if val == "No results found":
                    raise IndexError("ERR#0033: information unavailable or not found.")
                info.append(val)

            result = {
                "Date": datetime.strptime(
                    str(
                        datetime.fromtimestamp(
                            int(info[0]), tz=pytz.timezone("GMT")
                        ).date()
                    ),
                    "%Y-%m-%d",
                ),
                "Open": float(info[2].replace(",", "")),
                "High": float(info[3].replace(",", "")),
                "Low": float(info[4].replace(",", "")),
                "Close": float(info[1].replace(",", "")),
            }

            if has_volume and has_change_pct:
                result["Volume"] = int(info[5])
                result["Change Pct"] = float(info[6].replace(",", "").replace("%", ""))

            if not has_volume and has_change_pct:
                result["Change Pct"] = float(info[5].replace(",", "").replace("%", ""))

            results.append(result)

        return results[::-1]

    def _convert2df(self):
        self.data = pd.DataFrame(self.data)
        self.data.set_index("Date", inplace=True)
