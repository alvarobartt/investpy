import requests
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
    result.insert(len(result), Data(info[0], info[1], info[2]))

df = pd.DataFrame.from_records([data.to_dict() for data in result])

print(df.head())
