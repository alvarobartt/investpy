import investpy


def main():
    # data = investpy.get_stock_financial_summary(stock='GME', country='United States')
    data = investpy.get_stock_financials(stock='AAPL', country='United States', finacials_type='BAL')

    print(data.head())

if __name__ == '__main__':
    main()

