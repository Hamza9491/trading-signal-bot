import requests

token = '6160408785:AAGu-P60zjpk_Iby14RhZ67kaFL5r_J9SC0'
chat_id = '1041600176'

def send_telegram_message(text):
    # تقطيع النص لو طويل جدًا
    if len(text) > 4000:
        text = text[:4000] + "... (truncated)"

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        # 'parse_mode': 'HTML'  # تم تعطيله مؤقتًا لتجنب مشاكل التنسيق
    }
    try:
        response = requests.get(url, params=payload)
        print(f"✅ Telegram message sent (status: {response.status_code})")
        print("Response:", response.text)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")