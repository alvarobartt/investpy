import investpy


def main():
    data = investpy.get_stock_financial_summary(stock='AAPL', country='United States', summary_type='income_statement',
                                                period='annual')
    print(data.head())


if __name__ == '__main__':
    main()