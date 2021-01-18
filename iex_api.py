import requests
import pandas as pd
from config import IEX_TOKEN

url_base = 'https://cloud.iexapis.com/v1'

def getQuote(symbol):

    url = url_base + f"/stock/{symbol}/quote?"
    params = {'token' : IEX_TOKEN}

    r = requests.get(url, params=params).json()
    name = r['companyName']
    market = r['isUSMarketOpen']
    last_price = r['latestPrice']
    change = r['change']
    pct_change = round(r['changePercent'] * 100, 2)
    ext_last_price = r['extendedPrice']
    ext_change = r['extendedChange']
    try:
        ext_pct_change = round(r['extendedChangePercent'] * 100, 2)
        relVolume = round(r['avgTotalVolume'] / r['volume'], 2)
    except:
        ext_pct_change = 0
        relVolume = 0
    marketCap = round(r['marketCap'] / 10**9, 2)
    peRatio = r['peRatio']
    w52high = r['week52High']
    w52low = r['week52Low']

    new_dict = {
        'name': name,
        'market': market,
        'last_price': last_price,
        'change': change,
        'pct_change': pct_change,
        'ext_last_price': ext_last_price,
        'ext_change': ext_change,
        'ext_pct_change': ext_pct_change,
        'marketCap': marketCap,
        'peRatio': peRatio,
        'relVolume': relVolume,
        'w52high': w52high,
        'w52low': w52low
    }

    return new_dict

def getNews(symbol, last = 1):
    url = url_base + f"/stock/{symbol}/news/last/{last}?"
    params = {'token' : IEX_TOKEN}

    r = requests.get(url, params=params).json()
    df = pd.DataFrame(r)
    df['fecha'] = pd.to_datetime(df.datetime, unit = 'ms').dt.strftime('%d %b %-H:%M')
    
    return df['fecha'][0], df['url'][0]