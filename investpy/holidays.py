# Copyright 2018-2021 Alvaro Bartolome, alvarobartt @ GitHub
# See LICENSE for details.
# Colaboration of Alejandro Varela

from datetime import datetime
from time import strftime, localtime, gmtime

from random import choice
from unidecode import unidecode

import pandas as pd

from .utils import constant as cst
from .utils.extra import random_user_agent

import requests
from lxml.html import fromstring


def holiday_calendar(time_zone=None, time_filter='time_only', country=None, from_date=None, to_date=None):
    """
    This function retrieves the holiday_calendar

    Args:
        time_zone (:obj:`str`, optional):
            time zone in GMT +/- hours:minutes format, which will be the reference time, if None, the local GMT time zone will be used.
        time_filter (:obj:`str`, optional):
            it can be `time_only` or `time_remain`, so that the calendar will display the time when the event will occurr according to
            the time zone or the remaining time until an event occurs.
        countries (:obj:`list` of :obj:`str`, optional):
            list of countries from where the events of the economic calendar will be retrieved, all contries will be taken into consideration
            if this parameter is None.
        from_date (:obj:`str`, optional):
            date from when the economic calendar will be retrieved in dd/mm/yyyy format, if None just current day's economic calendar will be retrieved.
        to_date (:obj:`str`, optional):
            date until when the economic calendar will be retrieved in dd/mm/yyyy format, if None just current day's economic calendar will be retrieved.

    Returns:
        :obj:`pandas.DataFrame` - economic_calendar:
            The resulting :obj:`pandas.DataFrame` will contains the holiday_calendar

    Raises:
        ValueError: raised if any of the introduced parameters is not valid or errored.

    Examples:
        >>> data = investpy.holiday_calendar()
        >>> data.head()


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

    if country is not None and country not in cst.COUNTRY_ID_FILTERS.keys():
        raise ValueError("ERR#0111: the introduced countries value is not valid since it must be a list of strings unless it is None.")

    if from_date is not None and not isinstance(from_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    if to_date is not None and not isinstance(to_date, str):
        raise ValueError("ERR#0114: the introduced date value must be a string unless it is None.")

    url = "https://www.investing.com/holiday-calendar/Service/getCalendarFilteredData"
# curl 'https://www.investing.com/holiday-calendar/Service/getCalendarFilteredData' \
#      -H 'Connection: keep-alive' \
#         -H 'sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' \
#            -H 'Accept: */*' \
#               -H 'X-Requested-With: XMLHttpRequest' \
#                  -H 'sec-ch-ua-mobile: ?0' \
#                     -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36' \
#                        -H 'Content-Type: application/x-www-form-urlencoded' \
#                           -H 'Origin: https://www.investing.com' \
#                              -H 'Sec-Fetch-Site: same-origin' \
#                                 -H 'Sec-Fetch-Mode: cors' \
#                                    -H 'Sec-Fetch-Dest: empty' \
#                                       -H 'Referer: https://www.investing.com/holiday-calendar/' \
#                                          -H 'Accept-Language: en-US,en;q=0.9' \
#                                             -H 'Cookie: adBlockerNewUserDomains=1615562071; udid=7cb82bce2c2eec7c9e4d070e9ef1ad89; protectedMedia=2; _ga=GA1.2.154860154.1615562073; G_ENABLED_IDPS=google; _fbp=fb.1.1615562073750.949092910; OptanonAlertBoxClosed=2021-03-12T15:14:34.799Z; eupubconsent-v2=CPC8zV-PC8zV-AcABBENBRCsAP_AAH_AAChQHmNf_X__b3_j-_59_9t0eY1f9_7_v-0zjhfds-8N2f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrTPsbk2Mr7NKJ7PEinMbe2dYGH9_n93TuZKY7__s___z__-__v__7_f_r-3_3_vp9X---_e_V399xLv9QPKAJMNS-AizEscCSaNKoUQIQriQ6AUAFFCMLRNYQMrgp2VwEeoIGACA1ARgRAgxBRiwCAAACAJKIgJADwQCIAiAQAAgBUgIQAEbAILACwMAgAFANCxAigCECQgyOCo5TAgIkWignkrAEou9jDCEMosAKBR_RUYCJQggWAAA.f_gAD_gAAAAA; usprivacy=1YNN; __gads=ID=696ee8c4bb002eef:T=1615562075:S=ALNI_MaQbExUiYP93ESkZW0bjVX2C80KcQ; r_p_s_n=1; OB-USER-TOKEN=06bd0299-f49e-4017-a998-5b00777bd614; _pbjs_userid_consent_data=8323447842724566; editionPostpone=1615562589205; PHPSESSID=ag83iiur1e5vkcv9nmrvr1b6vs; StickySession=id.23687413726.091_www.investing.com; smd=7cb82bce2c2eec7c9e4d070e9ef1ad89-1615814925; geoC=ES; logglytrackingsession=bc19e830-6746-4d47-8b4f-375b57c5a5f5; _gid=GA1.2.1900944855.1615814944; SKpbjs-id5id=%7B%22created_at%22%3A%222021-03-12T15%3A21%3A09Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5-ZHMOejwabXkhjWtLfvOnbcj81zOyvxoyuKtz4-3vqg%22%2C%22universal_uid%22%3A%22ID5-ZHMOhFa9GTfYjp1XuOU6c_xjx46qOYgJ8S7yy488YQ%22%2C%22signature%22%3A%22ID5_AfcN3Z_OqZxyn2jgrZTgox-nXhC6JjwEnFK_DbQWq1dmzhzbEz1EZK6v6DhBHookHb7TQULOKtZRNJDCGH-t1E8%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%7D; SKpbjs-id5id_last=Mon%2C%2015%20Mar%202021%2013%3A29%3A08%20GMT; SKpbjs-unifiedid=%7B%22TDID%22%3A%22f51a25fe-4bfe-43ef-bf64-6da99b9b147c%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-02-15T13%3A28%3A51%22%7D; SKpbjs-unifiedid_last=Mon%2C%2015%20Mar%202021%2013%3A29%3A08%20GMT; gtmFired=OK; adsFreeSalePopUp=3; _gat_allSitesTracker=1; id5id.1st_212_nb=3; _gat=1; OptanonConsent=isIABGlobal=false&datestamp=Mon+Mar+15+2021+15%3A40%3A00+GMT%2B0100+(Central+European+Standard+Time)&version=6.12.0&hosts=&consentId=2a8f5d16-0adc-4efa-bba4-01bfcc3f2dd0&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CSTACK42%3A1&geolocation=ES%3BMD&AwaitingReconsent=false; outbrain_cid_fetch=true; nyxDorf=Z2pjODN7MGQ0fD4zM2k2PT9wM2ljYDIy; firstUdid=0' \
#                                                --data-raw 'country=&currentTab=today&limit_from=0' \
#                                                           --compressed
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
            'country': '',
            'currentTab': 'today',
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

    if country is not None:
        data.update({
            'country': cst.COUNTRY_ID_FILTERS[country]
        })



    results = list()

    bind_scroll_handler = True

    while bind_scroll_handler:
        req = requests.post(url, headers=headers, data=data)
        json_value = req.json()
        bind_scroll_handler = json_value['bind_scroll_handler']
        root = fromstring(json_value['data'])
        table = root.xpath(".//tr")

        id = 0
        curr_date = ""
        for row in table:

            elements = row.xpath('td')
            curr_date_raw = elements[0].text

            if curr_date_raw is not None:
                curr_date = datetime.strptime(curr_date_raw, '%b %d, %Y').strftime('%Y-%m-%d')
            if len(elements[1].xpath('a')) == 0:
                country = elements[1].xpath('span')[0].text
            else:
                country = elements[1].xpath('a')[0].text
            exchange_name = elements[2].text
            desc = elements[3].text


            results.append({
                'id': id,
                'date': curr_date,
                'country': country,
                'exchange_name': exchange_name,
                'desc':  desc
            })
            id = id+1

        if bind_scroll_handler:
            data['last_time_scope'] = json_value['last_time_scope']
            data['showMore'] = True
        data['limit_from'] += 1

    return pd.DataFrame(results)
