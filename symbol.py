import pandas as pd
import requests
import mplfinance as mpf
import tda_api


class Symbol():
    """Crea un gráfico del ticker que se le pase y lo devuelve como .png"""

    def __init__(self, symbol):
        self.symbol = symbol
        self.close = float
        self.change = float
        self.pct_change = float

    def _addMACD(self, data, slow=26, fast=12, suavizado=9):
        df = data.copy()
        df['ema_fast'] = df.close.ewm(span=fast).mean()
        df['ema_slow'] = df.close.ewm(span=slow).mean()
        data['macd'] = df.ema_fast - df.ema_slow
        data['signal'] = data.macd.ewm(span=suavizado).mean()
        data['histograma'] = data.macd - data.signal
        data = data.dropna().round(2)

        return data

    def _data(self):
        try:
            df = tda_api.priceHistory(self.symbol, period=2)
        except:
            return False

        self._addMACD(df)
        df['ema_20'] = df.close.ewm(span=20).mean()
        df['sma_50'] = df.close.rolling(50).mean()
        df['sma_200'] = df.close.rolling(200).mean()
        df['vol_avg'] = df.volume.rolling(100).mean()
        df = df.dropna().round(4)
        df = df.iloc[55:]
        
        return df

    def getQuote(self):
        quotes = tda_api.quote(self.symbol)
        self.close = quotes[0]
        self.change = quotes[1]
        self.pct_change = round(quotes[2], 2)
        if self.pct_change > 0:
            caption = f'📈 {self.symbol} ${self.close} {self.change}\n🔼 {self.pct_change}%'
        else:
            caption = f'📉 {self.symbol} ${self.close} {self.change}\n🔽 {self.pct_change}%'
        
        return caption

    def chart(self):
        df = self._data()
        if df is False:
            return False
        else:
            ap2 = [ mpf.make_addplot(df.vol_avg,panel=1,color='grey',secondary_y=True),
                    mpf.make_addplot(df.ema_20,panel=0,color='pink',secondary_y=False),
                    mpf.make_addplot(df.sma_50,panel=0,color='orange',secondary_y=False),
                    mpf.make_addplot(df.sma_200,panel=0,color='grey',secondary_y=False),
                    mpf.make_addplot(df.macd,panel=2,color='fuchsia',secondary_y=True),
                    mpf.make_addplot(df.signal,panel=2,color='b',secondary_y=True),
                    mpf.make_addplot(df.histograma,panel=2,type='bar',width=0.7,color='dimgray',alpha=0.5,secondary_y=False) ]

            mpf.plot(df, type = 'candle', style = 'yahoo', volume=True,savefig='chart.png',addplot=ap2,
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

