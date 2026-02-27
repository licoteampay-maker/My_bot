import telebot
import os
import google.generativeai as genai
from PIL import Image
import io

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من روی سرور Render بیدار شدم. 🚀 عکسی بفرست تا تحلیلش کنم!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "در حال تحلیل تصویر... 🪄")
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        image = Image.open(io.BytesIO(downloaded_file))
        
        response = model.generate_content([message.caption or "این تصویر را به فارسی تحلیل کن", image])
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")

print("Bot is starting on Render...")
bot.infinity_polling()
