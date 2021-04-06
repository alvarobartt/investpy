import investpy


def main():

    data = investpy.get_stock_financials(stock='AAPL', country='United States')
    print(data.head())


if __name__ == '__main__':
    main()


