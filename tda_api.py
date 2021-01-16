import requests
import pandas as pd
from config import TDA_TOKEN

base_url = 'https://api.tdameritrade.com/v1/marketdata/'

def priceHistory(symbol, 
                periodType = 'year',
                period = '1',
                frequencyType = 'daily',
                frequency = '1',
                startDate = "",
                endDate = "",
                needExtendedHoursData = 'false'
                ):
    """
    periodType : Valid values are day, month, year, or ytd (year to date). Default is day.
    period : Valid periods by periodType (defaults marked with an asterisk):
            day: 1, 2, 3, 4, 5, 10*
            month: 1*, 2, 3, 6
            year: 1*, 2, 3, 5, 10, 15, 20
            ytd: 1*
    frequencyType : 
            day: minute*
            month: daily, weekly*
            year: daily, weekly, monthly*
            ytd: daily, weekly*
    frecuency:
            minute: 1*, 5, 10, 15, 30
            daily: 1*
            weekly: 1*
            monthly: 1*
    """
    url = f'{base_url}{symbol}/pricehistory'
    params = {'apikey': TDA_TOKEN, 'periodType' : periodType, 'period' : period, 'frequencyType' : frequencyType,
             'frequency': frequency, 'needExtendedHoursData': needExtendedHoursData}

    r = requests.get(url, params=params)
    candles = r.json()['candles']
    df = pd.DataFrame(candles)
    df['date'] = pd.to_datetime(df.datetime, unit = 'ms')
    df.set_index('date', inplace=True)
    df.drop('datetime', inplace=True, axis=1)

    return df

def quote(symbol):
    url = f'{base_url}/quotes'
    params = {'apikey': TDA_TOKEN, 'symbol': symbol}

    r = requests.get(url, params=params)
    data = r.json()
    close = data[symbol]['regularMarketLastPrice']
    change = data[symbol]['regularMarketNetChange']
    pctChange = data[symbol]['regularMarketPercentChangeInDouble']
    
    return close, change, pctChange
