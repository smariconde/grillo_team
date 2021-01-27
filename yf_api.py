import yfinance as yf, datetime as dt

def getHistory(symbol):
    data = yf.Ticker(symbol).history(period='2y', interval='1d')
    data = data.drop(['Dividends', 'Stock Splits'], axis=1)
    columnas_nombres = ['open', 'high', 'low', 'close', 'volume']
    data.columns = columnas_nombres
    data.index.rename('date', inplace=True)
    
    return data

def getInfo(symbol):
    info = yf.Ticker(symbol).info

def getEarnings(symbol):
    earnings = yf.Ticker(symbol).calendar
    date_earnings = earnings.iloc[0,0]
    date_earnings = date_earnings.strftime('%d %b %Y')
    
    return date_earnings