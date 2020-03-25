# Copyright 2018-2020 Alvaro Bartolome @ alvarobartt in GitHub
# See LICENSE for details.


PRODUCT_FILTERS = {
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

PAIR_FILTERS = {
    'indice': 'indices', 
    'equities': 'stocks', 
    'etf': 'etfs', 
    'fund': 'funds', 
    'commodity': 'commodities', 
    'currency': 'currencies', 
    'crypto': 'cryptos', 
    'bond': 'bonds', 
    'certificate': 'certificates', 
    'fxfuture': 'fxfutures'
}

FLAG_FILTERS = {
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

COUNTRY_FILTERS = {
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

CATEGORY_FILTERS = {
    'credit': '_credit',
    'employment': '_employment',
    'economic_activity': '_economicActivity',
    'inflation': '_inflation',
    'central_banks': '_centralBanks',
    'confidence': '_confidenceIndex',
    'balance': '_balance',
    'bonds': '_Bonds'
}

IMPORTANCE_RATINGS = {
    1: 'low',
    2: 'medium',
    3: 'high'
}

COUNTRY_ID_FILTERS = {
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

TIME_FILTERS = {
    'time_remaining': 'timeRemain',
    'time_only': 'timeOnly'
}

TIMEZONES = {
    'GMT -11:00': [2, 35], 'GMT -10:00': [3], 'GMT -9:00': [4], 'GMT -8:00': [36, 5], 'GMT -7:00': [37, 38, 6], 
    'GMT -6:00': [39, 7, 40, 41], 'GMT -5:00': [42, 8, 43], 'GMT -4:00': [10, 9, 45, 46], 
    'GMT -3:30': [11], 'GMT -3:00': [44, 12, 48, 49, 50, 51, 47], 'GMT -1:00': [14, 53], 'GMT': [55, 15, 56],
    'GMT +1:00': [16, 57, 58, 54, 166, 59, 60], 'GMT +2:00': [62, 64, 65, 66, 68, 17, 67, 61], 'GMT +3:00': [71, 63, 70, 18, 72], 
    'GMT +3:30': [19], 'GMT +4:00': [20, 73], 'GMT +4:30': [21], 'GMT +5:00': [22, 77], 'GMT +5:30': [23, 79], 'GMT +5:45': [24], 
    'GMT +6:00': [25], 'GMT +6:30': [26], 'GMT +7:00': [27], 'GMT +8:00': [178, 28, 113], 'GMT +9:00': [29, 88], 'GMT +9:30': [90], 
    'GMT +10:30': [30], 'GMT +11:00': [31, 32], 'GMT +12:00': [1], 'GMT +13:00': [33]
}

PRODUCT_TYPE_FILES = {
    'certificate': 'certificates/certificates.csv',
    'commodity': 'commodities/commodities.csv',
    'currency_cross': 'currency_crosses/currency_crosses.csv',
    'etf': 'etfs/etfs.csv',
    'fund': 'funds/funds.csv',
    'index': 'indices/indices.csv',
    'stock': 'stocks/stocks.csv',
    'bond': 'bonds/bonds.csv'
}

INTERVAL_FILTERS = {
    '5mins': 60*5,
    '15mins': 60*15,
    '30mins': 60*30,
    '1hour': 60*60,
    '5hours': 60*60*5,
    'daily': 60*60*24,
    'weekly': 'week',
    'monthly': 'month'
}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2",
    "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
    "Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
    "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5",
    "Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
    "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
    "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
    "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
    "Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
    "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
    "Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14",
    "Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
]

# TODO: read csv files and transform them into dicts, procedure: csv into pandas and pandas to_dict()
BOND_COUNTRIES = {}

CERTIFICATE_COUNTRIES = {}

CURRENCIES = {}

ETF_COUNTRIES = {}

FUND_COUNTRIES = {}

STOCK_COUNTRIES = {}

INDEX_COUNTRIES = {}
