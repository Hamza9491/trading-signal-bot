import pandas as pd

class SignalChecker:

    def check_signal(self, df, support, resistance, direction='LONG'):
        last = df.iloc[-1]
        prev = df.iloc[-2]

        price = last['close']
        reasons = []
        passed_conditions = 0
        signal = False

        # التحقق من القيم المفقودة
        required_fields = ['RSI', 'Stoch_K', 'Stoch_D', 'EMA_9', 'EMA_21', 'MACD', 'MACD_signal', 'Volatility']
        for field in required_fields:
            if pd.isna(last[field]) or pd.isna(prev[field]):
                reasons.append(f"❌ Missing data: {field}")
                return False, reasons

        volatility = last['Volatility']
        buffer = volatility * 2.5  # معامل التحكم في القرب من الدعم/المقاومة

        # --- شرط RSI (إجباري) ---
        rsi_pass = False
        if direction == 'LONG':
            if 30 <= last['RSI'] <= 50 and last['RSI'] > prev['RSI']:
                rsi_pass = True
                reasons.append('✅ RSI valid (rising in 30-50)')
            else:
                reasons.append('❌ RSI not between 30-50 or not rising')

        elif direction == 'SHORT':
            if 50 <= last['RSI'] <= 70 and last['RSI'] < prev['RSI']:
                rsi_pass = True
                reasons.append('✅ RSI valid (falling in 70-50)')
            else:
                reasons.append('❌ RSI not between 50-70 or not falling')

        # إذا لم يتحقق RSI نرفض الإشارة فورًا
        if not rsi_pass:
            return False, reasons

        # --- باقي الشروط (نحتاج 2 على الأقل منها) ---
        if direction == 'LONG':
            if last['Stoch_K'] > last['Stoch_D']:
                passed_conditions += 1
                reasons.append('✅ Stoch_K > Stoch_D')
            else:
                reasons.append('❌ Stoch_K not above Stoch_D')

            if price > last['EMA_9'] > 0 and price > last['EMA_21'] > 0:
                passed_conditions += 1
                reasons.append('✅ Price above EMA 9 and 21')
            else:
                reasons.append('❌ Price not above EMA 9 and 21')

            if abs(price - support) <= buffer:
                passed_conditions += 1
                reasons.append(f'✅ Price near support (Δ ≤ {round(buffer, 6)})')
            else:
                reasons.append(f'❌ Price not close to support (Δ > {round(buffer, 6)})')

            if last['MACD'] > last['MACD_signal']:
                passed_conditions += 1
                reasons.append('✅ MACD is above Signal')
            else:
                reasons.append('❌ MACD not above Signal')

        elif direction == 'SHORT':
            if last['Stoch_K'] < last['Stoch_D']:
                passed_conditions += 1
                reasons.append('✅ Stoch_K < Stoch_D')
            else:
                reasons.append('❌ Stoch_K not below Stoch_D')

            if price < last['EMA_9'] and price < last['EMA_21']:
                passed_conditions += 1
                reasons.append('✅ Price below EMA 9 and 21')
            else:
                reasons.append('❌ Price not below EMA 9 and 21')

            if abs(price - resistance) <= buffer:
                passed_conditions += 1
                reasons.append(f'✅ Price near resistance (Δ ≤ {round(buffer, 6)})')
            else:
                reasons.append(f'❌ Price not close to resistance (Δ > {round(buffer, 6)})')

            if last['MACD'] < last['MACD_signal']:
                passed_conditions += 1
                reasons.append('✅ MACD is below Signal')
            else:
                reasons.append('❌ MACD not below Signal')

        # --- القرار النهائي ---
        if passed_conditions >= 2:
            signal = True
            reasons.append(f"✅ Passed {passed_conditions} optional conditions + RSI")

            # تقييم الإشارة بناءً على عدد الشروط
            if passed_conditions == 2:
                reasons.append("📊 Signal Strength: ⭐ (ضعيفة)")
            elif passed_conditions == 3:
                reasons.append("📊 Signal Strength: ⭐⭐ (متوسطة)")
            elif passed_conditions >= 4:
                reasons.append("📊 Signal Strength: ⭐⭐⭐ (قوية)")
        else:
            reasons.append(f"❌ Only {passed_conditions} optional conditions passed (need at least 2)")

        return signal, reasons