import finnhub
import time
import asyncio
from telegram import Bot
from deep_translator import GoogleTranslator

import os  # Buni eng tepaga qo'shing

# --- SOZLAMALAR (Yashirin usul) ---
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')


finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
translator = GoogleTranslator(source='en', target='uz')

last_news_time = int(time.time())

async def fetch_and_post_news():
    global last_news_time
    try:
        news = finnhub_client.general_news('general', min_id=0)
        for item in reversed(news):
            news_time = item['datetime']
            if news_time > last_news_time:
                headline = item['headline']
                summary = item['summary']
                source = item['source']
                url = item['url']

                uz_headline = translator.translate(headline)
                uz_summary = translator.translate(summary)

                flag = "🌍"
                h_low = headline.lower()
                if 'usa' in h_low or 'fed' in h_low: flag = "🇺🇸"
                elif 'japan' in h_low or 'yen' in h_low: flag = "🇯🇵"
                elif 'euro' in h_low or 'ecb' in h_low: flag = "🇪🇺"
                elif 'gold' in h_low: flag = "🟡"

                                # Post dizaynini optimallashtirish
                # Agar sarlavha va mazmun bir xil bo'lsa, takrorlamaslik uchun:
                if uz_headline.strip() == uz_summary.strip():
                    body_text = f"📢 {uz_headline}"
                else:
                    body_text = f"📢 *{uz_headline}*\n\n📝 {uz_summary}"

                                # Post dizayni (Diqqat: har bir qator boshida f harfi bo'lishi shart!)
                                # Post dizayni (Diqqat: har bir qator boshida f harfi bo'lishi shart!)
                message = (
                    f"{flag} <b>{uz_headline}</b>\n\n"
                    f"📝 {uz_summary}\n\n"
                    f"🏛 <i>Manba: {source}</i>\n"
                    f"🔗 <a href='{url}'>Batafsil o'qish</a>\n\n"
                    f"📡 @InvestRadar_UZ"
                )




                await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
                print(f"Yangi xabar kanalga joylandi: {headline}")
                last_news_time = news_time
                await asyncio.sleep(2)
    except Exception as e:
        print(f"Xatolik: {e}")

async def main():
    print("InvestRadar Bot ishga tushdi...")
    while True:
        await fetch_and_post_news()
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
