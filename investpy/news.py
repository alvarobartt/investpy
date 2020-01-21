#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from datetime import datetime
import pandas as pd

from investpy.utils.user_agent import get_random

import requests
from lxml.html import fromstring


def get_calendar():
    """
    from_date, to_date, countries, time_zone, categories, remaining_time
    importance[]: 1(low), 2(medium), 3(high)
    currentTab 'today' -> 'custom', dateFrom and dateTo (YYYY-MM-DD)
    timeFilter 'timeRemain' or 'timeOnly'
    category[]: _credit, _employment, _economicActivity, _inflation, _centralBanks, _confidenceIndex, _balance, _Bonds
    """

    importance_ratings = {
        'low': 1,
        'medium': 2,
        'high': 3
    }

    categories = {
        'credit': '_credit',
        'employment': '_employment',
        'economic_activity': '_economicActivity',
        'inflation': '_inflation',
        'central_banks': '_centralBanks',
        'confidence': '_confidenceIndex',
        'balance': '_balance',
        'bonds': '_Bonds'
    }

    url = "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"

    headers = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    data = {
        'timeZone': 8,
        'timeFilter': 'timeRemain',
        'currentTab': 'today',
        'submitFilters': 1, # Does not change
        'limit_from': 0  # Does not change
    }

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
                            sentiment = None
                        else:
                            sentiment = value.get('data-img_key').replace('bull', '')
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
                'sentiment': sentiment,
                'event': event,
                'actual': None if actual == '' else actual,
                'forecast': None if forecast == '' else forecast,
                'previous': None if previous == '' else previous
            }

            results.append(result)
    
    data = pd.DataFrame(results)

    return data
