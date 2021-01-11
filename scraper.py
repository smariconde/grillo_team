import pandas as pd
import requests

def dolar():
    agents = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    agents += 'Chrome/50.0.2661.75 Safari/537.36'
    header = {"User-Agent": agents, "X-Requested-With": "XMLHttpRequest"}

    url = "https://www.dolarhoy.com/"
    data = requests.get(url, params=header)

    table = pd.read_html(data.text)[0]

    return table.to_string(index=False, header=False, max_colwidth=1)
