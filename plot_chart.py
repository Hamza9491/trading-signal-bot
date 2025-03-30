import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime


def plot_candles_with_levels(symbol, logs_path='logs'):
    file_path = os.path.join(logs_path, f"{symbol}_candles.csv")
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    df = pd.read_csv(file_path, parse_dates=['timestamp'])
    df.set_index('timestamp', inplace=True)

    # استخدم آخر 300 شمعة فقط للرسم
    df = df.tail(400)

    fig, ax = plt.subplots(figsize=(12, 6))

    # رسم الشموع
    for idx, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        ax.plot([idx, idx], [row['low'], row['high']], color=color)
        ax.plot([idx, idx], [row['open'], row['close']], linewidth=6, color=color)

    # رسم خطوط الدعم والمقاومة
    support = df['Support'].iloc[-1]
    resistance = df['Resistance'].iloc[-1]
    ax.axhline(support, color='blue', linestyle='--', label=f'Support ({support:.2f})')
    ax.axhline(resistance, color='orange', linestyle='--', label=f'Resistance ({resistance:.2f})')

    # تنسيق المحور الزمني
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=45)
    plt.title(f"{symbol} Candlestick Chart with Support/Resistance")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()


# مثال تشغيل مباشر:
# plot_candles_with_levels("ETHUSDT")
