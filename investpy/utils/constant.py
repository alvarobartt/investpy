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
