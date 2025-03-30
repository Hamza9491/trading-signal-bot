from binance.client import Client
from binance.enums import HistoricalKlinesType
import pandas as pd
import numpy as np
import pandas_ta as ta
import variables_main as vars_m

class DataFetcher:
    def __init__(self):
        self.client = vars_m.client

    def get_klines(self, symbol, interval='5m', lookback=450):
        Cdata = self.client.get_historical_klines(
            symbol, interval, f"{lookback * 5} minutes ago UTC", klines_type=HistoricalKlinesType.FUTURES
        )
        df = pd.DataFrame(Cdata, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

        return df

    def add_indicators(self, df):
        df['RSI'] = ta.rsi(df['close'], length=14)
        stoch = ta.stoch(df['high'], df['low'], df['close'], k=14, d=3)
        df['Stoch_K'] = stoch['STOCHk_14_3_3']
        df['Stoch_D'] = stoch['STOCHd_14_3_3']

        df['EMA_9'] = ta.ema(df['close'], length=9)
        df['EMA_21'] = ta.ema(df['close'], length=21)
        df['EMA_200'] = ta.ema(df['close'], length=200)

        # MACD and Signal Line
        macd = ta.macd(df['close'])
        df['MACD'] = macd['MACD_12_26_9']
        df['MACD_signal'] = macd['MACDs_12_26_9']
        df['Volatility'] = (df['high'] - df['low']).rolling(window=50).mean()


        return df

    def calculate_support_resistance(self, df, highs=5, lows=5):
        max_vol_idx = df['volume'].idxmax()
        df_after_vol = df[df.index >= max_vol_idx]

        resistance = df_after_vol['high'].nlargest(highs).mean()
        support = df_after_vol['low'].nsmallest(lows).mean()

        return support, resistance

    def fetch_all(self, symbol):
        df = self.get_klines(symbol)
        df = self.add_indicators(df)
        support, resistance = self.calculate_support_resistance(df)
        return df, support, resistance
