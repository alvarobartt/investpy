import investpy


def main():
    # Old stuff
    # data = investpy.get_stock_financial_summary(stock='GME', country='United States')

    # Potential second presentable
    # data = investpy.get_stock_financials(stock='GME', country='United States', finacials_type='BAL', period='quarterly')
    # print(data)

    # First presentable
    tester = investpy.get_stock_historical_data(stock='AAPL', country='United States')
    print(tester)


if __name__ == '__main__':
    main()

