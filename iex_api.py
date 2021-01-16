import requests
from config import IEX_TOKEN
from pprint import pprint

def getQuote(symbol):

    url = f"https://cloud.iexapis.com/v1/stock/{symbol}/quote?"
    params = {'token' : IEX_TOKEN}

    r = requests.get(url, params=params).json()
    name = r['companyName']
    market = r['isUSMarketOpen']
    last_price = r['latestPrice']
    change = r['change']
    pct_change = r['changePercent'] * 100
    ext_last_price = r['extendedPrice']
    ext_change = r['extendedChange']
    ext_pct_change = r['extendedChangePercent'] * 100
    marketCap = round(r['marketCap'] / 10**9, 2)
    peRatio = r['peRatio']
    relVolume = round(r['avgTotalVolume'] / r['volume'], 2)
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
