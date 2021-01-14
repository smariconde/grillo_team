import pandas as pd
import requests
import mplfinance as mpf
from config import IEX_TOKEN


class Chart():
    """Crea un gráfico del ticker que se le pase y lo devuelve como .png"""

    def __init__(self, symbol):
        self.symbol = symbol

    def _addMACD(self, data, slow=26, fast=12, suavizado=9):
        df = data.copy()
        df['ema_fast'] = df.close.ewm(span=fast).mean()
        df['ema_slow'] = df.close.ewm(span=slow).mean()
        data['macd'] = df.ema_fast - df.ema_slow
        data['signal'] = data.macd.ewm(span=suavizado).mean()
        data['histograma'] = data.macd - data.signal
        data = data.dropna().round(2)

        return data

    def _iex_api(self, token=IEX_TOKEN):
        url = f"https://cloud.iexapis.com/v1/stock/{self.symbol}/intraday-prices?"
        params = {'chartIEXOnly':'True','chartInterval': '1', 'token' : token}
        try:
            data = requests.get(url, params=params).json()
        except:
            return False

        df = pd.DataFrame(data)
        df.minute = pd.to_datetime(df.minute)
        df.minute = df.minute + pd.DateOffset(hours=2)
        df.set_index('minute', inplace=True)

        self._addMACD(df)
        df['ema_20'] = df.close.ewm(span=20).mean()
        df = df.dropna().round(4)

        return df

    def chart(self):
        df = self._iex_api()
        if df is False:
            return False
        else:
            ap2 = [ mpf.make_addplot(df.macd,panel=2,color='fuchsia',secondary_y=True),
                    mpf.make_addplot(df.signal,panel=2,color='b',secondary_y=True),
                    mpf.make_addplot(df.histograma,panel=2,type='bar',width=0.7,color='dimgray',alpha=0.5,secondary_y=False) ]

            mpf.plot(df, type = 'candle', style = 'yahoo', volume=True, mav = (20),savefig='chart.png',addplot=ap2,
                    title=str(self.symbol),
                    ylabel='',
                    ylabel_lower='',
                    figratio= (30,15),
                    figscale = 2,
                    panel_ratios = (6,1,2),
                    tight_layout= True,
                    volume_panel=1,
                    scale_width_adjustment=dict(volume=0.7,candle=1.45),
                    update_width_config=dict(candle_linewidth=1.2),
                    block=False)
