# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.

from datetime import datetime
from time import strftime, localtime, gmtime
import pytz

from random import choice
from unidecode import unidecode

import pandas as pd

from .utils import constant as cst
from .utils.extra import random_user_agent

import requests
from lxml.html import fromstring


def economic_calendar(time_zone=None, time_filter='time_only', countries=None, importances=None, categories=None, from_date=None, to_date=None):
    """
    This function retrieves the economic calendar, which covers financial events and indicators from all over the world
    updated in real-time. By default, the economic calendar of the currrent day from you local timezone will be retrieved, but
    note that some parameters can be specified so that the economic calendar to retrieve can be filtered.

    Args:
        time_zone (:obj:`str`): 
            time zone in GMT +/- hours:minutes format, which will be the reference time, if None, the local GMT time zone will be used.
        time_filter (:obj:`str`):
            it can be `time_only` or `time_remain`, so that the calendar will display the time when the event will occurr according to 
            the time zone or the remaining time until an event occurs.
        countries (:obj:`list` of :obj:`str`):
            list of countries from where the events of the economic calendar will be retrieved, all contries will be taken into consideration 
            if this parameter is None.
        importances (:obj:`list` of :obj:`str`):
            list of importances of the events to be taken into consideration, can contain: high, medium and low; if None all the importance 
            ratings will be taken into consideration including holidays.
        categories (:obj:`list` of :obj:`str`):
            list of categories to which the events will be related to, if None all the available categories will be taken into consideration.
        from_date (:obj:`str`):
            date from when the economic calendar will be retrieved in dd/mm/yyyy format, if None just current day's economic calendar will be retrieved.
        to_date (:obj:`str`):
            date until when the economic calendar will be retrieved in dd/mm/yyyy format, if None just current day's economic calendar will be retrieved.

    Returns:
        :obj:`pandas.DataFrame` - economic_calendar:
            The resulting :obj:`pandas.DataFrame` will contain the retrieved information from the economic calendar with the specified parameters
            which will include information such as: date, time, zone or country of the event, event's title, etc. Note that some of the retrieved fields
            may be None since Investing.com does not provides that information.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored. 

    Examples:
        >>> data = investpy.economic_calendar()
        >>> data.head()
            id        date     time         zone currency importance                         event actual forecast previous
        0  323  27/01/2020  All Day    singapore     None       None  Singapore - Chinese New Year   None     None     None
        1    9  27/01/2020  All Day    hong kong     None       None    Hong Kong - New Year's Day   None     None     None
        2   71  27/01/2020  All Day    australia     None       None     Australia - Australia Day   None     None     None
        3  750  27/01/2020  All Day        china     None       None       China - Spring Festival   None     None     None
        4  304  27/01/2020  All Day  south korea     None       None  South Korea - Market Holiday   None     None     None

    """

    if time_zone is not None and not isinstance(time_zone, str):
        raise ValueError("ERR#0107: the introduced time_zone must be a string unless it is None.")

    if time_zone is None:
        time_zone = 'GMT'

        diff = datetime.strptime(strftime('%d/%m/%Y %H:%M', localtime()), '%d/%m/%Y %H:%M') - \
            datetime.strptime(strftime('%d/%m/%Y %H:%M', gmtime()), '%d/%m/%Y %H:%M')

        hour_diff = int(diff.total_seconds() / 3600)
        min_diff = int(diff.total_seconds() % 3600) * 60

        if hour_diff != 0:
            time_zone = "GMT " + ('+' if hour_diff > 0 else '') + str(hour_diff) + ":" + ('00' if min_diff < 30 else '30')
    else:
        if time_zone not in cst.TIMEZONES.keys():
            raise ValueError("ERR#0108: the introduced time_zone does not exist, please consider passing time_zone as None.")

    if not isinstance(time_filter, str):
        raise ValueError("ERR#0109: the introduced time_filter is not valid since it must be a string.")

    if time_filter not in cst.TIME_FILTERS.keys():
        raise ValueError("ERR#0110: the introduced time_filter does not exist, available ones are: time_remaining and time_only.")

    if countries is not None and not isinstance(countries, list):
        raise ValueError("ERR#0111: the introduced countries value is not valid since it must be a list of strings unless it is None.")

    if importances is not None and not isinstance(importances, list):
        raise ValueError("ERR#0112: the introduced importances value is not valid since it must be a list of strings unless it is None.")

    if categories is not None and not isinstance(categories, list):
        raise ValueError("ERR#0113: the introduced categories value is not valid since it must be a list of strings unless it is None.")

    if from_date is not None and not isinstance(from_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    if to_date is not None and not isinstance(to_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    url = "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"

    headers = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    dates = [from_date, to_date]

    if any(date is None for date in dates) is True:
        data = {
            'timeZone': choice(cst.TIMEZONES[time_zone]),
            'timeFilter': cst.TIME_FILTERS[time_filter],
            'currentTab': 'today',
            'submitFilters': 1,
            'limit_from': 0
        }
    else:
        try:
            datetime.strptime(from_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'.")

        start_date = datetime.strptime(from_date, '%d/%m/%Y')

        try:
            datetime.strptime(to_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

        end_date = datetime.strptime(to_date, '%d/%m/%Y')

        if start_date >= end_date:
            raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

        data = {
            'dateFrom': datetime.strptime(from_date, '%d/%m/%Y').strftime('%Y-%m-%d'),
            'dateTo': datetime.strptime(to_date, '%d/%m/%Y').strftime('%Y-%m-%d'),
            'timeZone': choice(cst.TIMEZONES[time_zone]),
            'timeFilter': cst.TIME_FILTERS[time_filter],
            'currentTab': 'custom',
            'submitFilters': 1,
            'limit_from': 0
        }

    if countries is not None:
        def_countries = list()

        available_countries = list(cst.COUNTRY_ID_FILTERS.keys())

        # TODO: improve loop using lambda
        for country in countries:
            country = unidecode(country.lower())
            country = country.strip()

            if country in available_countries:
                def_countries.append(cst.COUNTRY_ID_FILTERS[country])

        if len(def_countries) > 0:
            data.update({
                'country[]': def_countries
            })

    if categories is not None:
        def_categories = list()

        available_categories = list(cst.CATEGORY_FILTERS.keys())

        # TODO: improve loop using lambda
        for category in categories:
            category = unidecode(category.lower())
            category = category.strip()

            if category in available_categories:
                def_categories.append(cst.CATEGORY_FILTERS[category])

        if len(def_categories) > 0:
            data.update({
                'category[]': def_categories
            })

    if importances is not None:
        def_importances = list()

        # TODO: improve loop using lambda
        for importance in importances:
            importance = unidecode(importance.lower())
            importance = importance.strip()

            for key, value in cst.IMPORTANCE_RATINGS.items():
                if value == importance:
                    if key not in def_importances:
                        def_importances.append(key)
                    break

        if len(def_importances) > 0:
            data.update({
                'importance[]': def_importances
            })

    req = requests.post(url, headers=headers, data=data)

    root = fromstring(req.json()['data'])
    table = root.xpath(".//tr")

    results = list()

    for row in table:
        id_ = row.get("id")
        if id_ == None:
            curr_date = datetime.fromtimestamp(int(row.xpath("td")[0].get("id").replace("theDay", "")), tz=pytz.utc).strftime("%d/%m/%Y")
        else:
            id_ = id_.replace('eventRowId_', '')

            time = zone = currency = sentiment = event = actual = forecast = previous = None

            if row.get("id").__contains__("eventRowId_"):
                for value in row.xpath("td"):
                    if value.get("class").__contains__('first left'):
                        time = value.text_content()
                    elif value.get("class").__contains__('flagCur'):
                        zone = value.xpath('span')[0].get('title').lower()
                        currency = value.text_content().strip()
                    elif value.get("class").__contains__('sentiment'):
                        if value.get("data-img_key") == None:
                            importance_rating = None
                        else:
                            importance_rating = value.get('data-img_key').replace('bull', '')
                    elif value.get("class") == 'left event':
                        event = value.text_content().strip()
                    elif value.get("id") == 'eventActual_' + id_:
                        actual = value.text_content().strip()
                    elif value.get("id") == 'eventForecast_' + id_:
                        forecast = value.text_content().strip()
                    elif value.get("id") == 'eventPrevious_' + id_:
                        previous = value.text_content().strip()

            result = {
                'id': id_,
                'date': curr_date,
                'time': time,
                'zone': zone,
                'currency': None if currency == '' else currency,
                'importance': None if importance_rating == None else cst.IMPORTANCE_RATINGS[int(importance_rating)],
                'event': event,
                'actual': None if actual == '' else actual,
                'forecast': None if forecast == '' else forecast,
                'previous': None if previous == '' else previous
            }

            results.append(result)

    return pd.DataFrame(results)


def earnings_calendar(time_zone=None, time_filter='time_only', countries=None, importances=None, sectors=None, from_date=None, to_date=None):
    """
    This function retrieves the earnings calendar, which covers financial earnings results and forecasts from all over the world
    updated in real-time. By default, the earnings calendar of the currrent day from you local timezone will be retrieved, but
    note that some parameters can be specified so that the economic calendar to retrieve can be filtered.

    Args:
        time_zone (:obj:`str`):
            time zone in GMT +/- hours:minutes format, which will be the reference time, if None, the local GMT time zone will be used.
        time_filter (:obj:`str`):
            it can be `time_only` or `time_remain`, so that the calendar will display the time when the event will occurr according to
            the time zone or the remaining time until an event occurs.
        countries (:obj:`list` of :obj:`str`):
            list of countries from where the events of the economic calendar will be retrieved, all contries will be taken into consideration
            if this parameter is None.
        importances (:obj:`list` of :obj:`str`):
            list of importances of the events to be taken into consideration, can contain: high, medium and low; if None all the importance
            ratings will be taken into consideration including holidays.
        sectors (:obj:`list` of :obj:`str`):
            list of sectors to which the events will be related to, if None all the available categories will be taken into consideration.
        from_date (:obj:`str`):
            date from when the economic calendar will be retrieved in dd/mm/yyyy format, if None just current day's economic calendar will be retrieved.
        to_date (:obj:`str`):
            date until when the economic calendar will be retrieved in dd/mm/yyyy format, if None just current day's economic calendar will be retrieved.

    Returns:
        :obj:`pandas.DataFrame` - earnings_calendar:
            The resulting :obj:`pandas.DataFrame` will contain the retrieved information from the earnings calendar with the specified parameters
            which will include information such as: date, company, symbol or eps_actual, market_cap, etc. Note that some of the retrieved fields
            may be None since Investing.com does not provides that information.

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.

    Examples:
        >>> data = investpy.earnings_calendar()
        >>> data.head()

            date        company         symbol  eps_actual   eps_forecast    revenue_actual  revenue_forecast    market_cap  earnings_time
        0  24/11/2020   Medtronic       MDT        1.02          0.8024         7.65B               7.07B           153.93B      None
        1  24/11/2020   Autodesk        ADSK       None          0.96           None                942.5M          56.49B       None
        2  24/11/2020   Analog Devices  ADI        1.44          1.33           1.53B               1.45B           50.01B       None
        3  24/11/2020   Best Buy        BBY        2.06          1.7            11.85B              10.97B          29.59B       None
        4  24/11/2020   HP Inc          HPQ        None          0.5228         None                14.61B          29.54B       None

    """

    # TODO: would it be better to extract the shared logic with economic_calendar instead of the duplicated code?
    if time_zone is not None and not isinstance(time_zone, str):
        raise ValueError("ERR#0107: the introduced time_zone must be a string unless it is None.")

    if time_zone is None:
        time_zone = 'GMT'

        diff = datetime.strptime(strftime('%d/%m/%Y %H:%M', localtime()), '%d/%m/%Y %H:%M') - \
               datetime.strptime(strftime('%d/%m/%Y %H:%M', gmtime()), '%d/%m/%Y %H:%M')

        hour_diff = int(diff.total_seconds() / 3600)
        min_diff = int(diff.total_seconds() % 3600) * 60

        if hour_diff != 0:
            time_zone = "GMT " + ('+' if hour_diff > 0 else '') + str(hour_diff) + ":" + ('00' if min_diff < 30 else '30')
    else:
        if time_zone not in cst.TIMEZONES.keys():
            raise ValueError("ERR#0108: the introduced time_zone does not exist, please consider passing time_zone as None.")

    if not isinstance(time_filter, str):
        raise ValueError("ERR#0109: the introduced time_filter is not valid since it must be a string.")

    if time_filter not in cst.TIME_FILTERS.keys():
        raise ValueError("ERR#0110: the introduced time_filter does not exist, available ones are: time_remaining and time_only.")

    if countries is not None and not isinstance(countries, list):
        raise ValueError("ERR#0111: the introduced countries value is not valid since it must be a list of strings unless it is None.")

    if importances is not None and not isinstance(importances, list):
        raise ValueError("ERR#0112: the introduced importances value is not valid since it must be a list of strings unless it is None.")

    if sectors is not None and not isinstance(sectors, list):
        raise ValueError("ERR#0113: the introduced sectors value is not valid since it must be a list of strings unless it is None.")

    if from_date is not None and not isinstance(from_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    if to_date is not None and not isinstance(to_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    url = "https://www.investing.com/earnings-calendar/Service/getCalendarFilteredData"

    headers = {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    dates = [from_date, to_date]

    if any(date is None for date in dates) is True:
        data = {
            'timeZone': choice(cst.TIMEZONES[time_zone]),
            'timeFilter': cst.TIME_FILTERS[time_filter],
            'currentTab': 'today',
            'submitFilters': 1,
            'limit_from': 0
        }
    else:
        try:
            datetime.strptime(from_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("ERR#0011: incorrect from_date date format, it should be 'dd/mm/yyyy'.")

        start_date = datetime.strptime(from_date, '%d/%m/%Y')

        try:
            datetime.strptime(to_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError("ERR#0012: incorrect to_date format, it should be 'dd/mm/yyyy'.")

        end_date = datetime.strptime(to_date, '%d/%m/%Y')

        if start_date >= end_date:
            raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

        data = {
            'dateFrom': datetime.strptime(from_date, '%d/%m/%Y').strftime('%Y-%m-%d'),
            'dateTo': datetime.strptime(to_date, '%d/%m/%Y').strftime('%Y-%m-%d'),
            'timeZone': choice(cst.TIMEZONES[time_zone]),
            'timeFilter': cst.TIME_FILTERS[time_filter],
            'currentTab': 'custom',
            'submitFilters': 1,
            'limit_from': 0
        }

    if countries is not None:
        def_countries = list()

        available_countries = list(cst.COUNTRY_ID_FILTERS.keys())

        # TODO: improve loop using lambda
        for country in countries:
            country = unidecode(country.lower())
            country = country.strip()

            if country in available_countries:
                def_countries.append(cst.COUNTRY_ID_FILTERS[country])

        if len(def_countries) > 0:
            data.update({
                'country[]': def_countries
            })

    # TODO: sectors don't work yet, need to check investing.com API for the exact sectors definitions
    if sectors is not None:
        def_sectors = list()

        available_sectors = list(cst.SECTOR_FILTERS.keys())

        # TODO: improve loop using lambda
        for sector in sectors:
            sector = unidecode(sector.lower())
            sector = sector.strip()

            if sector in available_sectors:
                def_sectors.append(cst.SECTOR_FILTERS[sector])

        if len(def_sectors) > 0:
            data.update({
                'sector[]': def_sectors
            })

    if importances is not None:
        def_importances = list()

        # TODO: improve loop using lambda
        for importance in importances:
            importance = unidecode(importance.lower())
            importance = importance.strip()

            for key, value in cst.IMPORTANCE_RATINGS.items():
                if value == importance:
                    if key not in def_importances:
                        def_importances.append(key)
                    break

        if len(def_importances) > 0:
            data.update({
                'importance[]': def_importances
            })

    req = requests.post(url, headers=headers, data=data)

    root = fromstring(req.json()['data'])
    table = root.xpath(".//tr")

    results = list()

    for row in table:
        if row.get("tablesorterdivider") == '':
            curr_date = datetime.strptime(row.xpath("td")[0].text_content(), '%A, %B %d, %Y').strftime("%d/%m/%Y")
        else:
            # TODO: missing the earnings_time parser (BMO, AMC), seems to be inconsistent in investing.com
            company = symbol = eps_actual = eps_forecast = revenue_actual = revenue_forecast = market_cap = earnings_time = None

            for idx, val in enumerate(row.xpath("td")):
                if not val.get("class"):
                    continue

                if val.get("class").__contains__('earnCalCompany'):
                    company_full = val.text_content().strip().split('(')
                    company = company_full[0][:-1]
                    symbol = company_full[1][:-1]
                elif val.get("class").__contains__('eps_actual'):
                    eps_actual = val.text_content().strip()
                    eps_forecast_split = row.xpath("td")[idx + 1].text_content().split('/')
                    eps_forecast = eps_forecast_split[1].strip() if len(eps_forecast_split) > 0 else ''
                elif val.get("class").__contains__('rev_actual'):
                    revenue_actual = val.text_content().strip()
                    revenue_forecast_split = row.xpath("td")[idx + 1].text_content().split('/')
                    revenue_forecast = revenue_forecast_split[1].strip() if len(revenue_forecast_split) > 0 else ''
                elif val.get("class") == 'right':
                    market_cap = val.text_content().strip()

            result = {
                'date': curr_date,
                'company': None if company == '' else company,
                'symbol': None if symbol == '' else symbol,
                'eps_actual': None if eps_actual == '--' else eps_actual,
                'eps_forecast': None if eps_forecast == '--' else eps_forecast,
                'revenue_actual': None if revenue_actual == '--' else revenue_actual,
                'revenue_forecast': None if revenue_forecast == '--' else revenue_forecast,
                'market_cap': None if market_cap == '--' else market_cap,
                'earnings_time': None if earnings_time == '' else earnings_time
            }

            results.append(result)

    return pd.DataFrame(results)
