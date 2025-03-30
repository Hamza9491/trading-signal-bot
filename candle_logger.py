import pandas as pd
import os
from datetime import datetime

class CandleLogger:
    def __init__(self, save_path='logs'):
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def log(self, df, symbol, signal_type, support, resistance):
        df = df.copy()
        df['Symbol'] = symbol
        df['Signal'] = signal_type
        df['Support'] = support
        df['Resistance'] = resistance
        df['Logged_At'] = datetime.now()

        df.index.name = 'timestamp'

        file_path = os.path.join(self.save_path, f"{symbol}_candles.csv")

        # محاولة حفظ البيانات مع إعادة المحاولة إذا الملف كان تالف
        for attempt in range(2):
            try:
                if os.path.exists(file_path):
                    existing_df = pd.read_csv(file_path, parse_dates=['timestamp'])
                    last_logged_time = existing_df['timestamp'].max()
                    df = df[df.index > last_logged_time]

                if not df.empty:
                    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path))
                    print(f"✅ Logged candles for {symbol} ({len(df)} rows)")
                else:
                    print(f"⚠️ No new candles to log for {symbol}")
                break  # إذا نجحت المحاولة، نخرج من الحلقة

            except Exception as e:
                print(f"❌ Error reading or writing log for {symbol}: {e}")
                if attempt == 0:
                    print(f"🧹 Deleting corrupted log file for {symbol} and retrying...")
                    os.remove(file_path)
                else:
                    print(f"❌ Failed again after deleting log for {symbol}. Skipping...")
