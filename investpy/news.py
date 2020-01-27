#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from datetime import datetime
from time import strftime, gmtime
from random import choice
import unidecode

import pandas as pd

from investpy.utils.user_agent import get_random

import requests
from lxml.html import fromstring


def get_calendar(time_zone=None, time_filter='time_only', countries=None, importances=None, categories=None, from_date=None, to_date=None):
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
        >>> investpy.get_calendar()
                id        date     time         zone currency importance                         event actual forecast previous
            0  323  27/01/2020  All Day    singapore     None       None  Singapore - Chinese New Year   None     None     None
            1    9  27/01/2020  All Day    hong kong     None       None    Hong Kong - New Year's Day   None     None     None
            2   71  27/01/2020  All Day    australia     None       None     Australia - Australia Day   None     None     None
            3  750  27/01/2020  All Day        china     None       None       China - Spring Festival   None     None     None
            4  304  27/01/2020  All Day  south korea     None       None  South Korea - Market Holiday   None     None     None

    """

    time_zones = {
        'GMT -11:00': [2, 35], 'GMT -10:00': [3], 'GMT -9:00': [4], 'GMT -8:00': [36, 5], 'GMT -7:00': [37, 38, 6], 
        'GMT -6:00': [39, 7, 40, 41, 169], 'GMT -5:00': [42, 8, 43, 173, 170, 171, 172], 'GMT -4:00': [10, 9, 45, 46, 101, 102, 103, 104], 
        'GMT -3:30': [11], 'GMT -3:00': [198, 44, 12, 48, 105, 49, 106, 50, 51, 47, 168], 'GMT -1:00': [14, 53], 'GMT': [197, 55, 201, 15, 200, 56],
        'GMT +1:00': [196, 190, 184, 182, 187, 188, 189, 166, 183, 186, 193, 167, 16, 57, 58, 54, 59, 60], 
        'GMT +2:00': [162, 192, 199, 194, 191, 195, 160, 165, 67, 185, 62, 98, 64, 99, 65, 66, 107, 68, 17, 108, 61], 
        'GMT +3:00': [174, 179, 180, 161, 164, 71, 63, 70, 109, 18, 72], 'GMT +3:30': [19], 'GMT +4:00': [20, 73, 74, 75, 76, 175], 
        'GMT +4:30': [21], 'GMT +5:00': [22, 77, 78], 'GMT +5:30': [23, 79, 177], 'GMT +5:45': [24], 'GMT +6:00': [80, 25], 'GMT +6:30': [26], 
        'GMT +7:00': [110, 27, 111, 82, 81, 176], 'GMT +8:00': [181, 178, 28, 83, 112, 85, 113, 86, 87], 'GMT +9:00': [29, 88, 89], 'GMT +9:30': [90], 
        'GMT +10:00': [91, 114, 94, 115], 'GMT +10:30': [30], 'GMT +11:00': [31, 93, 117, 116, 32, 100], 'GMT +12:00': [1, 96], 'GMT +13:00': [33, 97]
    }

    if time_zone is not None and not isinstance(time_zone, str):
        raise ValueError("ERR#0107: the introduced time_zone must be a string unless it is None.")

    if time_zone is None:
        time_zone = 'GMT'

        hour_diff = int(strftime('%H')) - int(strftime('%H', gmtime()))
        min_diff = int(strftime('%M')) - int(strftime('%M', gmtime()))

        if hour_diff != 0:
            time_zone = "GMT " + ('-' if hour_diff < 0 else '+') + str(hour_diff) + ":" + ('00' if min_diff == 0 else str(min_diff))
    else:
        if time_zone not in time_zones:
            raise ValueError("ERR#0108: the introduced time_zone does not exist, please consider passing time_zone as None.")

    time_filters = {
        'time_remaining': 'timeRemain',
        'time_only': 'timeOnly'
    }

    if not isinstance(time_filter, str):
        raise ValueError("ERR#0109: the introduced time_filter is not valid since it must be a string.")

    if time_filter not in time_filters:
        raise ValueError("ERR#0110: the introduced time_filter does not exist, available ones are: time_remaining and time_only.")

    country_filters = {
        'argentina': 29, 'australia': 25, 'austria': 54, 'bahrain': 145, 'bangladesh': 47, 'belgium': 34, 'bosnia': 174,
        'botswana': 163, 'brazil': 32, 'bulgaria': 70, 'canada': 6, 'cayman islands': 232, 'chile': 27, 'china': 37, 'colombia': 122,
        'costa rica': 15, 'croatia': 113, 'cyprus': 107, 'czech republic': 55, 'denmark': 24, 'dubai': 143, 'ecuador': 121, 'egypt': 59,
        'estonia': 89, 'euro zone': 72, 'finland': 71, 'france': 22, 'germany': 17, 'greece': 51, 'hong kong': 39, 'hungary': 93, 
        'iceland': 106, 'india': 14, 'indonesia': 48, 'iraq': 66, 'ireland': 33, 'israel': 23, 'italy': 10, 'ivory coast': 78, 'jamaica': 119, 
        'japan': 35, 'jordan': 92, 'kazakhstan': 102, 'kenya': 57, 'kuwait': 94, 'latvia': 97, 'lebanon': 68, 'lithuania': 96, 'luxembourg': 103, 
        'malawi': 111, 'malaysia': 42, 'malta': 109, 'mauritius': 188, 'mexico': 7, 'mongolia': 139, 'montenegro': 247, 'morocco': 105, 
        'namibia': 172, 'netherlands': 21, 'new zealand': 43, 'nigeria': 20, 'norway': 60, 'oman': 87, 'pakistan': 44, 'palestine': 193, 
        'peru': 125, 'philippines': 45, 'poland': 53, 'portugal': 38, 'qatar': 170, 'romania': 100, 'russia': 56, 'rwanda': 80, 'saudi arabia': 52, 
        'serbia': 238, 'singapore': 36, 'slovakia': 90, 'slovenia': 112, 'south africa': 110, 'south korea': 11, 'spain': 26, 'sri lanka': 162,  
        'sweden': 9, 'switzerland': 12, 'taiwan': 46, 'tanzania': 85, 'thailand': 41, 'tunisia': 202, 'turkey': 63, 'uganda': 123, 'ukraine': 61, 
        'united kingdom': 4, 'united states': 5, 'venezuela': 138, 'vietnam': 178, 'zambia': 84, 'zimbabwe': 75
    }

    if countries is not None and not isinstance(countries, list):
        raise ValueError("ERR#0111: the introduced countries value is not valid since it must be a list of strings unless it is None.")

    importance_ratings = {
        1: 'low',
        2: 'medium',
        3: 'high'
    }

    if importances is not None and not isinstance(importances, list):
        raise ValueError("ERR#0112: the introduced importances value is not valid since it must be a list of strings unless it is None.")

    category_filters = {
        'credit': '_credit',
        'employment': '_employment',
        'economic_activity': '_economicActivity',
        'inflation': '_inflation',
        'central_banks': '_centralBanks',
        'confidence': '_confidenceIndex',
        'balance': '_balance',
        'bonds': '_Bonds'
    }

    if categories is not None and not isinstance(categories, list):
        raise ValueError("ERR#0113: the introduced categories value is not valid since it must be a list of strings unless it is None.")

    if from_date is not None and not isinstance(from_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    if to_date is not None and not isinstance(froto_datem_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    url = "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"

    headers = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    dates = [from_date, to_date]

    if any(date is None for date in dates) is True:
        data = {
            'timeZone': choice(time_zones[time_zone]),
            'timeFilter': time_filters[time_filter],
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
            'timeZone': choice(time_zones[time_zone]),
            'timeFilter': time_filters[time_filter],
            'currentTab': 'custom',
            'submitFilters': 1,
            'limit_from': 0
        }

    if countries is not None:
        def_countries = list()

        available_countries = country_filters.keys().tolist()

        for country in countries:
            country = unidecode.unidecode(country.lower())
            country = country.strip()

            if country in available_countries:
                def_countries.append(country_filters[country])

        if len(def_countries) > 0:
            data.update({
                'country[]': def_countries
            })

    if categories is not None:
        def_categories = list()

        available_categories = category_filters.keys().tolist()

        for category in categories:
            category = unidecode.unidecode(category.lower())
            category = category.strip()

            if category in available_categories:
                def_categories.append(category_filters[category])

        if len(def_categories) > 0:
            data.update({
                'category[]': def_categories
            })

    if importances is not None:
        def_importances = list()

        for importance in importances:
            importance = unidecode.unidecode(importance.lower())
            importance = importance.strip()

            for key, value in importance_ratings.items():
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
            curr_date = datetime.fromtimestamp(int(row.xpath("td")[0].get("id").replace("theDay", ""))).strftime("%d/%m/%Y")
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
                'importance': None if importance_rating == None else importance_ratings[int(importance_rating)],
                'event': event,
                'actual': None if actual == '' else actual,
                'forecast': None if forecast == '' else forecast,
                'previous': None if previous == '' else previous
            }

            results.append(result)
    
    data = pd.DataFrame(results)

    return data
