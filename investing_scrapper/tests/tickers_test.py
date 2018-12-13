import pandas as pd

tickers = pd.read_csv('../resources/tickers.csv')
print(tickers)

for row in tickers.itertuples():
    print(row.name)