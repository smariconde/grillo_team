import pandas as pd
import requests
from bs4 import BeautifulSoup

def dolar():
    agents = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) '
    agents += 'Chrome/87.0.4280.141 Safari/537.36'
    header = {"User-Agent": agents, "X-Requested-With": "XMLHttpRequest"}

    url = "https://www.infodolar.com/"
    data = requests.get(url, params=header)
    print(data)
    print(data.text)
    table = pd.read_html(data.text)
    return table.to_string(index=False, header=False, max_colwidth=1)
