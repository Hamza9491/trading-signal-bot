from data_fetcher import DataFetcher
from candle_logger import CandleLogger
from signal_checker import SignalChecker
from plot_chart import plot_candles_with_levels
from telegram_alert import send_telegram_message
import time

symbols = ["ETHUSDT", "BTCUSDT","SOLUSDT","XRPUSDT","DOGEUSDT","SUIUSDT","1000PEPEUSDT","BNBUSDT","ADAUSDT","TUTUSDT","VINEUSDT"]
fetcher = DataFetcher()
logger = CandleLogger()
checker = SignalChecker()

while True:
    for symbol in symbols:
        try:
            df, support, resistance = fetcher.fetch_all(symbol)

            for direction in ['LONG', 'SHORT']:
                signal, reasons = checker.check_signal(df, support, resistance, direction=direction)
                print(f"\n--- {symbol} ({direction}) ---")
                for r in reasons:
                    print(r)

                # نسجل دائمًا البيانات، حتى لو لم تتحقق الإشارة
                logger.log(df, symbol=symbol, signal_type=direction if signal else 'NO_SIGNAL', support=support, resistance=resistance)

                # إرسال إشعار تيليجرام إذا تحققت الإشارة
                if signal:
                    message = f"🚨 <b>{symbol} - {direction} Signal</b>\n" + "\n".join(reasons)
                    print(f"📤 Sending Telegram message for {symbol}:\n{message}")
                    send_telegram_message(message)

            plot_candles_with_levels(symbol)  # عرض الرسم البياني دائمًا

        except Exception as e:
            print(f"❌ Error with {symbol}: {e}")

    print("\n⏳ Waiting 5 minutes before next scan...\n")
    time.sleep(200)  # 5 دقائق