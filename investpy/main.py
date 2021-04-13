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

    data = investpy.technical_indicators(name='AAPL', country='United States', product_type='stock', interval='daily')
    print(data.head())
    print('===============================')


if __name__ == '__main__':
    main()

