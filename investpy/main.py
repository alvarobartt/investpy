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

    # data = investpy.technical_indicators(name='bbva', country='spain', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='aapl', country='united states', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='daily')
    # data = investpy.technical_indicators(name='U.S. 10Y', country='united states', product_type='bond', interval='daily')
    # data = investpy.technical_indicators(name='gme', country='united states', product_type='stock', interval='weekly')

    # print(data)

    data = investpy.get_index_historical_data(index='DJ US',
                                              country='united states',
                                              interval='Daily',
                                              from_date='01/01/1996',
                                              to_date='17/12/2020',
                                              order='descending',
                                              as_json=True)
    print(data.head())

    # data = investpy.get_indices_list(country='United States')
    # print(data)



if __name__ == '__main__':
    main()
