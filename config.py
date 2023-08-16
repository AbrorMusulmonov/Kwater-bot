import telebot

# Telegram bot's token
bot_token = "6424828696:AAFyKrVdSA1JGaX7wdF5PuoYp4DDsC2cE4g"

bot = telebot.TeleBot(bot_token)

# Weather API
weather_api_key = "6e790d95736387581da526f6ddf7bed2"

# Weather so'rov uchun URL
weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q=Tashkent&appid={weather_api_key}&units=metric"