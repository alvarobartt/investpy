import requests
import datetime
import pandas as pd
from model import Data
from bs4 import BeautifulSoup

url = "https://es.investing.com/equities/bbva-historical-data"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
}

req = requests.get(url, headers=headers)

status = req.status_code
html = BeautifulSoup(req.text, 'html.parser')

selection = html.select('div#results_box > table#curr_table > tbody > tr')

result = list()

for element in selection:
    info = element.getText().strip().split('\n')
    stock_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
    stock_close = info[1].replace(',', '.')
    stock_open = info[2].replace(',', '.')
    result.insert(len(result), Data(stock_date, stock_close, stock_open))

result = result[::-1]

df = pd.DataFrame.from_records([data.to_dict() for data in result])
df.set_index('Date', inplace=True)

print(df.head())
