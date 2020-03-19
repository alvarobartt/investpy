# Copyright 2018-2020 Alvaro Bartolome @ alvarobartt in GitHub
# See LICENSE for details.

import requests

import re
from unidecode import unidecode

from .utils.search_obj import SearchObj
from .utils.user_agent import get_random


def search(text, filters=None, countries=None, n_results=None):
    """
    This function will use the Investing search engine so to retrieve the search results of the
    introduced text. This function will create a :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj`
    class instances which will contain the search results so that they can be easily accessed and so
    to ease the data retrieval process since it can be done calling the methods `self.retrieve_recent_data()`
    or `self.retrieve_historical_data(from_date, to_date)` from the class instance, which will fill the `self.data`
    attribute of that class instance.

    Args:
        text (:obj:`str`): text to search in Investing among all its indexed data.
        filters (:obj:`list` of :obj:`str`, optional):
            list with the filter/s to be applied to the search result quotes so that the resulting quotes match
            the filters. Possible filters are: `indices`, `stocks`, `etfs`, `funds`, `commodities`, `currencies`, 
            `crypto`, `bonds`, `certificates` and `fxfutures`. Default is `None` which means that no filter will 
            be applied.
        n_results (:obj:`int`, optional): number of search results to retrieve and return from Investing.

    Returns:
        :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj`:
            The resulting :obj:`list` of :obj:`investpy.utils.search_obj.SearchObj` will contained the retrieved
            financial products matching the introduced text as indexed in Investing, if found. Note that if no
            information was found this function will raise a `ValueError` exception.

    Raises:
        ValueError: raised if either the introduced text is not valid or if no results were found for that text.
        ConnectionError: raised whenever the connection to Investing.com errored (did not return a 200 OK code).

    """

    if not text:
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if not isinstance(text, str):
        raise ValueError('ERR#0074: text parameter is mandatory and it should be a valid str.')

    if countries and not isinstance(countries, list):
        raise ValueError('ERR#0128: countries filtering parameter is optional, but if specified, it must be a list of str.')

    if n_results and not isinstance(n_results, int):
        raise ValueError('ERR#0088: n_results parameter is optional, but if specified, it must be an integer equal or higher than 1.')

    if n_results is not None:
        if n_results < 1:
            raise ValueError('ERR#0088: n_results parameter is optional, but if specified, it must be an integer higher than 0.')

    if filters and not isinstance(filters, list):
        raise ValueError('ERR#0094: filters parameter can just be a list or None if no filter wants to be applied.')

    available_filters = {
        'indices': 'indice', 
        'stocks': 'equities', 
        'etfs': 'etf', 
        'funds': 'fund', 
        'commodities': 'commodity', 
        'currencies': 'currency', 
        'cryptos': 'crypto', 
        'bonds': 'bond', 
        'certificates': 'certificate', 
        'fxfutures': 'fxfuture'
    }

    # TODO: unidecode operation and to lower case need to be done
    if filters:
        condition = set(filters).issubset(available_filters.keys())
        if condition is False:
            raise ValueError('ERR#0095: filters parameter values must be contained in ' + ', '.join(available_filters) + '.')
        else:
            filters = [available_filters[filter_] for filter_ in filters]
    else:
        filters = list(available_filters.values())

    # TODO: constant variables containing all the countries
    available_countries = {
        'Andorra': 'andorra', 'Argentina': 'argentina', 'Australia': 'australia', 'Austria': 'austria',
        'Bahrain': 'bahrain', 'Bangladesh': 'bangladesh', 'Belgium': 'belgium', 'Bermuda': 'bermuda', 
        'Bosnia': 'bosnia', 'Botswana': 'botswana', 'Brazil': 'brazil', 'Bulgaria': 'bulgaria', 
        'Canada': 'canada', 'Cayman_Islands': 'cayman islands', 'Chile': 'chile', 'China': 'china', 
        'Colombia': 'colombia', 'Costa_Rica': 'costa rica', 'Cote_dIvoire': 'ivory coast', 
        'Croatia': 'croatia', 'Cyprus': 'cyprus', 'Czech_Republic': 'czech republic', 
        'Denmark': 'denmark', 'Ecuador': 'ecuador', 'Egypt': 'egypt', 'Estonia': 'estonia', 
        'Europe': 'euro zone', 'Finland': 'finland', 'France': 'france', 'Germany': 'germany', 
        'Gibraltar': 'gibraltar', 'Greece': 'greece', 'Hong_Kong': 'hong kong', 'Hungary': 'hungary', 
        'Iceland': 'iceland', 'India': 'india', 'Indonesia': 'indonesia', 'Iraq': 'iraq', 
        'Ireland': 'ireland', 'Israel': 'israel', 'Italy': 'italy', 'Jamaica': 'jamaica', 
        'Japan': 'japan', 'Jordan': 'jordan', 'Kazakhstan': 'kazakhstan', 'Kenya': 'kenya', 
        'Kuwait': 'kuwait', 'Latvia': 'latvia', 'Lebanon': 'lebanon', 'Liechtenstein': 'liechtenstein', 
        'Lithuania': 'lithuania', 'Luxembourg': 'luxembourg', 'Malawi': 'malawi', 'Malaysia': 'malaysia', 
        'Malta': 'malta', 'Mauritius': 'mauritius', 'Mexico': 'mexico', 'Monaco': 'monaco', 
        'Mongolia': 'mongolia', 'Montenegro': 'montenegro', 'Morocco': 'morocco', 'Namibia': 'namibia', 
        'Netherlands': 'netherlands', 'New_Zealand': 'new zealand', 'Nigeria': 'nigeria', 
        'Norway': 'norway', 'Oman': 'oman', 'Pakistan': 'pakistan', 'Palestine': 'palestine', 
        'Peru': 'peru', 'Philippines': 'philippines', 'Poland': 'poland', 'Portugal': 'portugal', 
        'Qatar': 'qatar', 'Romania': 'romania', 'Russian_Federation': 'russia', 'Rwanda': 'rwanda', 
        'Saudi_Arabia': 'saudi arabia', 'Serbia': 'serbia', 'Singapore': 'singapore', 'Slovakia': 'slovakia', 
        'Slovenia': 'slovenia', 'South_Africa': 'south africa', 'South_Korea': 'south korea', 
        'Spain': 'spain', 'Sri_Lanka': 'sri lanka', 'Sweden': 'sweden', 'Switzerland': 'switzerland', 
        'Taiwan': 'taiwan', 'Tanzania': 'tanzania', 'Thailand': 'thailand', 'Tunisia': 'tunisia', 
        'Turkey': 'turkey', 'Uganda': 'uganda', 'Ukraine': 'ukraine', 'Dubai': 'dubai', 
        'UK': 'united kingdom', 'USA': 'united states', 'Venezuela': 'venezuela', 'Vietnam': 'vietnam', 
        'Zambia': 'zambia', 'Zimbabwe': 'zimbabwe'
    }

    available_flags = {
        'andorra': 'Andorra', 'argentina': 'Argentina', 'australia': 'Australia', 'austria': 'Austria', 
        'bahrain': 'Bahrain', 'bangladesh': 'Bangladesh', 'belgium': 'Belgium', 'bermuda': 'Bermuda', 
        'bosnia': 'Bosnia', 'botswana': 'Botswana', 'brazil': 'Brazil', 'bulgaria': 'Bulgaria', 
        'canada': 'Canada', 'cayman islands': 'Cayman_Islands', 'chile': 'Chile', 'china': 'China', 
        'colombia': 'Colombia', 'costa rica': 'Costa_Rica', 'ivory coast': 'Cote_dIvoire', 'croatia': 'Croatia', 
        'cyprus': 'Cyprus', 'czech republic': 'Czech_Republic', 'denmark': 'Denmark', 'ecuador': 'Ecuador', 
        'egypt': 'Egypt', 'estonia': 'Estonia', 'euro zone': 'Europe', 'finland': 'Finland', 'france': 'France', 
        'germany': 'Germany', 'gibraltar': 'Gibraltar', 'greece': 'Greece', 'hong kong': 'Hong_Kong', 
        'hungary': 'Hungary', 'iceland': 'Iceland', 'india': 'India', 'indonesia': 'Indonesia', 
        'iraq': 'Iraq', 'ireland': 'Ireland', 'israel': 'Israel', 'italy': 'Italy', 'jamaica': 'Jamaica', 
        'japan': 'Japan', 'jordan': 'Jordan', 'kazakhstan': 'Kazakhstan', 'kenya': 'Kenya', 'kuwait': 'Kuwait', 
        'latvia': 'Latvia', 'lebanon': 'Lebanon', 'liechtenstein': 'Liechtenstein', 'lithuania': 'Lithuania', 
        'luxembourg': 'Luxembourg', 'malawi': 'Malawi', 'south korea': 'South_Korea', 'spain': 'Spain', 
        'sri lanka': 'Sri_Lanka', 'sweden': 'Sweden', 'switzerland': 'Switzerland', 'taiwan': 'Taiwan', 
        'tanzania': 'Tanzania', 'thailand': 'Thailand', 'tunisia': 'Tunisia', 'turkey': 'Turkey', 'uganda': 'Uganda', 
        'ukraine': 'Ukraine', 'dubai': 'Dubai', 'united kingdom': 'UK', 'united states': 'USA', 'venezuela': 'Venezuela', 
        'vietnam': 'Vietnam', 'zambia': 'Zambia', 'zimbabwe': 'Zimbabwe', 'mauritius': 'Mauritius', 'mexico': 'Mexico', 
        'monaco': 'Monaco', 'mongolia': 'Mongolia', 'montenegro': 'Montenegro', 'morocco': 'Morocco', 'namibia': 'Namibia', 
        'netherlands': 'Netherlands', 'new zealand': 'New_Zealand', 'nigeria': 'Nigeria', 'norway': 'Norway', 'oman': 'Oman', 
        'pakistan': 'Pakistan', 'palestine': 'Palestine', 'peru': 'Peru', 'philippines': 'Philippines', 'poland': 'Poland', 
        'portugal': 'Portugal', 'qatar': 'Qatar', 'romania': 'Romania', 'russia': 'Russian_Federation', 'rwanda': 'Rwanda', 
        'saudi arabia': 'Saudi_Arabia', 'serbia': 'Serbia', 'singapore': 'Singapore', 'slovakia': 'Slovakia', 'slovenia': 'Slovenia', 
        'south africa': 'South_Africa', 'south korea': 'South_Korea', 'spain': 'Spain', 'sri lanka': 'Sri_Lanka', 'sweden': 'Sweden', 
        'switzerland': 'Switzerland', 'taiwan': 'Taiwan', 'tanzania': 'Tanzania', 'thailand': 'Thailand', 'tunisia': 'Tunisia', 
        'turkey': 'Turkey', 'uganda': 'Uganda', 'ukraine': 'Ukraine', 'dubai': 'Dubai', 'united kingdom': 'UK', 'united states': 'USA', 
        'venezuela': 'Venezuela', 'vietnam': 'Vietnam', 'zambia': 'Zambia', 'zimbabwe': 'Zimbabwe'
    }

    search_countries = list(available_countries.values())

    if countries:
        try:
            countries = [unidecode(country.lower().strip()) for country in countries]
        except:
            raise ValueError('ERR#0129: introduced countries are not valid, please validate them.')

        condition = set(countries).issubset(search_countries)
        if condition is False:
            raise ValueError('ERR#0129: introduced countries are not valid, please validate them.')
        else:
            flags = [available_flags[country] for country in countries]
    else:
        flags = list(available_countries.keys())

    print(flags)

    params = {
        'search_text': text,
        'tab': 'quotes',
        'limit': 270,
        'offset': 0
    }

    head = {
        "User-Agent": get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = 'https://www.investing.com/search/service/SearchInnerPage'

    search_results = list()

    total_results = None

    while True:
        print(params)
        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        data = req.json()

        print(data['total'])

        if data['total']['quotes'] == 0:
            raise ValueError("ERR#0093: no results found on Investing for the introduced text.")

        if total_results is None:
            total_results = data['total']['quotes']

        if n_results is None:
            n_results = data['total']['quotes']

        print(f"TOTAL QUOTES: {len(data['quotes'])}")

        for quote in data['quotes']:
            flag = quote['flag']

            tag = re.sub(r'\/(.*?)\/', '', quote['link'])

            print(quote['name'])

            # TODO: change filters dict so to include the proper filter name instead of the one provided by Investing.com
            if quote['pair_type'] in filters and flag in flags:
                search_results.append(SearchObj(id_=quote['pairId'], name=quote['name'], symbol=quote['symbol'],
                                                country=available_countries[flag], tag=tag, pair_type=quote['pair_type'],
                                                exchange=quote['exchange']))
        
        params['offset'] += 270
        
        if len(search_results) >= n_results or len(search_results) >= total_results or params['offset'] >= total_results:
            break
    
    print(len(search_results))

    return list(set(search_results))[:n_results]
