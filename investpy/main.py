import investpy


def main():
    # data = investpy.get_stock_financial_summary(stock='GME', country='United States')
    # print(data.head())

    # temppls = investpy.get_stocks("United States")
    # print(temppls)

    # data = investpy.get_stock_financials(stock='AAPL', country='United States')
    # print("Before")
    # print(data)
    # print("After")

    # tester = investpy.get_stock_historical_data(stock='AAPL', country='United States')
    # print(tester)

    # SOLO ISSUE TESTS
    data = investpy.technical_indicators(name='bbva', country='spain', product_type='stock', interval='daily')
    print(data)
    #
    # data = investpy.technical_indicators(name='aapl', country='united states', product_type='stock', interval='daily')
    # print(data)
    #
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='daily')
    # print(data)
    #
    # data = investpy.technical_indicators(name='U.S. 10Y', country='united states', product_type='bond', interval='daily')
    # print(data)
    #
    # data = investpy.technical_indicators(name='DOW 30', country='United States', product_type='index', interval='15mins')
    # print(data)
    #
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='weekly')
    # print(data)
    #
    # data = investpy.technical_indicators(name='AMZN', country='united states', product_type='stock', interval='1min')
    # data_other = investpy.technical_indicators(name='AMZN', country='united states', product_type='stock',
    #                                           interval='monthly')
    # print(data)
    # print("(-----------------------------------------------------------------------)")
    # print("|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|=|")
    # print("(-----------------------------------------------------------------------)")
    # print(data_other)



if __name__ == '__main__':
    main()

