## 💻 Usage

Even though some investpy usage examples are presented on the [docs](https://investpy.readthedocs.io/usage.html), 
some basic functionality will be sorted out with sample Python code blocks. Additionally, more usage examples 
can be found under [examples/](https://github.com/alvarobartt/investpy/tree/master/examples) directory, which 
contains a collection of Jupyter Notebooks on how to use investpy and handle its data.

📌 __Note that `investpy.search_quotes` is the only function that ensures that the data is updated and aligned 1:1 with
the data provided by Investing.com!__

### 📈 Recent/Historical Data Retrieval

investpy allows the user to **download both recent and historical data from any financial product indexed** 
(stocks, funds, ETFs, currency crosses, certificates, bonds, commodities, indices, and cryptos). In 
the example presented below, the historical data from the past years of a stock is retrieved. 

```python
import investpy

df = investpy.get_stock_historical_data(stock='AAPL',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')
print(df.head())
```
```
             Open   High    Low  Close     Volume Currency
Date                                                      
2010-01-04  30.49  30.64  30.34  30.57  123432176      USD
2010-01-05  30.66  30.80  30.46  30.63  150476160      USD
2010-01-06  30.63  30.75  30.11  30.14  138039728      USD
2010-01-07  30.25  30.29  29.86  30.08  119282440      USD
2010-01-08  30.04  30.29  29.87  30.28  111969192      USD
```

To get to know all the available recent and historical data extraction functions provided by 
investpy, and also, parameter tuning, please read the docs.

### 🔍 Search Live Data

**Investing.com search engine is completely integrated** with investpy, which means that any available 
financial product (quote) can be easily found. The search function allows the user to tune the parameters 
to adjust the search results to their needs, where both product types and countries from where the 
products are, can be specified. **All the search functionality can be easily used**, for example, as 
presented in the following piece of code:

```python
import investpy

search_result = investpy.search_quotes(text='apple', products=['stocks'],
                                       countries=['united states'], n_results=1)
print(search_result)
```
```
{"id_": 6408, "name": "Apple Inc", "symbol": "AAPL", "country": "united states", "tag": "/equities/apple-computer-inc", "pair_type": "stocks", "exchange": "NASDAQ"}

```

Retrieved search results will be a `list` of `investpy.utils.search_obj.SearchObj` class instances, unless
`n_results` is set to 1, when just a single `investpy.utils.search_obj.SearchObj` class instance will be returned.
To get to know which are the available functions and attributes of the returned search results, please read the related 
documentation at [Search Engine Documentation](https://investpy.readthedocs.io/search_api.html). So on, those 
search results let the user retrieve both recent and historical data, its information, the technical indicators,
the default currency, etc., as presented in the pieces of code below:

#### Recent Data

```python
recent_data = search_result.retrieve_recent_data()
print(recent_data.head())
```
```
              Open    High     Low   Close     Volume  Change Pct
Date
2021-05-13  124.58  126.15  124.26  124.97  105861000        1.79
2021-05-14  126.25  127.89  125.85  127.45   81918000        1.98
2021-05-17  126.82  126.93  125.17  126.27   74245000       -0.93
2021-05-18  126.56  126.99  124.78  124.85   63343000       -1.12
2021-05-19  123.16  124.92  122.86  124.69   92612000       -0.13

```

#### Historical Data

```python
historical_data = search_result.retrieve_historical_data(from_date='01/01/2019', to_date='01/01/2020')
print(historical_data.head())
```
```
             Open   High    Low  Close     Volume  Change Pct
Date
2020-01-02  74.06  75.15  73.80  75.09  135647008        2.28
2020-01-03  74.29  75.14  74.13  74.36  146536000       -0.97
2020-01-06  73.45  74.99  73.19  74.95  118579000        0.80
2020-01-07  74.96  75.22  74.37  74.60  111511000       -0.47
2020-01-08  74.29  76.11  74.29  75.80  132364000        1.61

```

#### Information

```python
information = search_result.retrieve_information()
print(information)
```
```json
{"prevClose": 126.11, "dailyRange": "126.1-127.44", "revenue": 325410000000, "open": 126.53, "weekRange": "83.14-145.09", "eps": 4.46, "volume": 53522373, "marketCap": 2130000000000, "dividend": "0.88(0.70%)", "avgVolume": 88858729, "ratio": 28.58, "beta": 1.2, "oneYearReturn": "50.35%", "sharesOutstanding": 16687631000, "nextEarningDate": "03/08/2021"}

```

#### Currency

```python
default_currency = search_result.retrieve_currency()
print(default_currency)
```
```
'USD'

```

#### Technical Indicators

```python
technical_indicators = search_result.retrieve_technical_indicators(interval="daily")
print(technical_indicators)
```
```
              indicator           signal     value
0               RSI(14)          neutral   52.1610
1            STOCH(9,6)              buy   63.7110
2          STOCHRSI(14)       overbought  100.0000
3           MACD(12,26)             sell   -0.6700
4               ADX(14)          neutral   21.4750
5           Williams %R              buy  -20.9430
6               CCI(14)              buy   67.1057
7               ATR(14)  less_volatility    1.7871
8        Highs/Lows(14)              buy    0.4279
9   Ultimate Oscillator             sell   47.3620
10                  ROC              buy    1.5150
11  Bull/Bear Power(13)              buy    1.3580

```

### 💸 Crypto Currencies Data Retrieval

Cryptocurrencies support has recently been included, to let the user retrieve data and information from any 
available crypto at Investing.com. Please note that some cryptocurrencies do not have available data indexed 
at Investing.com so that it can not be retrieved using investpy either, even though they are just a few, 
consider it.

As already presented previously, **historical data retrieval using investpy is really easy**. The piece of code 
presented below shows how to retrieve the past years of historical data from Bitcoin (BTC).

```python
import investpy

data = investpy.get_crypto_historical_data(crypto='bitcoin',
                                           from_date='01/01/2014',
                                           to_date='01/01/2019')

print(data.head())
```
```
             Open    High    Low   Close  Volume Currency
Date                                                     
2014-01-01  805.9   829.9  771.0   815.9   10757      USD
2014-01-02  815.9   886.2  810.5   856.9   12812      USD
2014-01-03  856.9   888.2  839.4   884.3    9709      USD
2014-01-04  884.3   932.2  848.3   924.7   14239      USD
2014-01-05  924.7  1029.9  911.4  1014.7   21374      USD
```
