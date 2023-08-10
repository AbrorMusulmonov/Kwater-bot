import telebot
import requests
import datetime
from tabulate import tabulate
from telebot import types

# Telegram bot's token
bot_token = "6424828696"

bot = telebot.TeleBot(bot_token)

# User's list
users = {}


@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id

    # Foydalanuvchilar ro'yxatida chat ID ni tekshirish
    if chat_id not in users:
        users[chat_id] = {}
        users[chat_id]["step"] = 1

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_register = types.KeyboardButton("Registration")
    keyboard.add(button_register)
    bot.send_message(
        chat_id,
        "Assalomu alaykum, Welcome to our Water-Saver bot!\nPlease, click the registration button",
        reply_markup=keyboard,
    )


@bot.message_handler(func=lambda message: message.text == "Registration")
def register(message):
    chat_id = message.chat.id
    users[chat_id]["step"] = 2
    bot.send_message(chat_id, "Enter your fullname: ")


@bot.message_handler(
    func=lambda message: users.get(message.chat.id, {}).get("step") == 2
)
def get_name(message):
    chat_id = message.chat.id
    users[chat_id]["name"] = message.text
    users[chat_id]["step"] = 3
    bot.send_message(
        chat_id,
        "Please, share your contact information:",
        reply_markup=get_contact_keyboard(),
    )


def get_contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_contact = types.KeyboardButton("Share Contact", request_contact=True)
    keyboard.add(button_contact)
    return keyboard


@bot.message_handler(
    content_types=["contact"],
    func=lambda message: users.get(message.chat.id, {}).get("step") == 3,
)
def get_contact(message):
    chat_id = message.chat.id
    contact = message.contact
    users[chat_id]["phone"] = contact.phone_number
    users[chat_id]["step"] = 4
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Weather")
    button2 = types.KeyboardButton("Useful Insights")
    button3 = types.KeyboardButton("Personal Info")
    button4 = types.KeyboardButton("Water Accident Condition")
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(
        chat_id,
        "Information is saved. Let's choose following buttons:",
        reply_markup=keyboard,
    )
    save_to_file(chat_id)


# Foydalanuvchi malumotlarini faylga saqlash
def save_to_file(chat_id):
    if chat_id in users:
        user_data = users[chat_id]
        with open("data.txt", "a", encoding="utf-8") as file:
            file.write(
                f"Chat ID: {chat_id}, Ism: {user_data['name']}, Telefon: {user_data['phone']}\n"
            )


#######################################################################################################################
# Weather API
weather_api_key = "6e790d95736387581da526f6ddf7bed2"

# Weather so'rov uchun URL
weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q=Tashkent&appid={weather_api_key}&units=metric"


# Weather API dan ob-havo ma'lumotlarini olish
def get_weather_forecast():
    try:
        response = requests.get(weather_url)
        data = response.json()
        if data["cod"] == "200":
            forecast_info = []
            for forecast in data["list"]:
                date = forecast["dt_txt"].split()[0]
                weather_description = forecast["weather"][0]["description"]
                temperature = forecast["main"]["temp"]
                forecast_info.append([date, weather_description, f"{temperature}°C"])
            return forecast_info
        else:
            return "Ob-havo ma'lumotlari olishda xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
    except Exception as e:
        return f"Xatolik yuz berdi: {e}"


# Weather tugmasi uchun javob
@bot.message_handler(func=lambda message: message.text == "Weather")
def show_weather(message):
    chat_id = message.chat.id
    weather_info = get_weather_forecast()
    if isinstance(weather_info, list):
        message_text = "Haftalik ob-havo ma'lumotlari:\n"
        message_text += "+------------+-----------------------+---------------+\n"
        message_text += "| Date       | Weather Description   | Temperature   |\n"
        message_text += "+============+=======================+===============+\n"

        for forecast in weather_info:
            date, weather_description, temperature = forecast
            message_text += f"| {date} | {weather_description} | {temperature} |\n"

        message_text += "+------------+-----------------------+---------------+\n"

        # Send the message
        bot.send_message(chat_id, message_text)
    else:
        bot.send_message(chat_id, weather_info)


#######################################################################################################################
# Useful Insight uchun ma'lumotlar
useful_insight = """ 
This information was prepared by the bot team https://t.me/kwater_competition_bot

Every people should pay attention to this information!

Top 13 ways for water saving
Link=> https://friendsoftheearth.uk/sustainable-living/13-best-ways-save-water


In Farming water-saving
1)Drip irrigation
2)Capturing and storing water
3)Irrigation scheduling
4)Crops resistant to drought
5)Dry farming
6)Rotational grazing
7)Compost and mulch
8)Conservation tillage
9)Cover crops
10)Organic farming

Link=> https://www.green.earth/blog/10-agricultural-techniques-for-water-conservation


For this information every people
- Water is vital for life. Clean fresh water is necessary for drinking and sanitation, providing for our crops, livestock and industry, and creating and sustaining the ecosystems on which all life depends.
- It takes 4070 cubic meters of water to grow enough food for an average family for a year.
- A leaky faucet can waste 340 liters a day.
- One flush of the toilet uses water.
- An average bath requires 1 liter 40 liter of water.
- We know  priori that on average, Singaporeans use almost 20 liters of water in a single shower that takes about five minutes.


You can also read about save water more information medium.com and quora.com.You can easily article about it so you can search #save_water!

Stay tuned us! We will announce next version our exploration as website!

 © Water-Saver 2023 All rights reserved.  
 """


# Useful Insight tugmasi uchun javob
@bot.message_handler(func=lambda message: message.text == "Useful Insights")
def show_useful_insight(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, useful_insight)


#######################################################################################################################


# Personal Info uchun javob
@bot.message_handler(func=lambda message: message.text == "Personal Info")
def show_personal_info(message):
    chat_id = message.chat.id
    if chat_id in users:
        user_data = users[chat_id]
        name = user_data.get("name", "N/A")
        phone = user_data.get("phone", "N/A")

        full_info = f"Full Name: {name}\nPhone: {phone}"
        bot.send_message(chat_id, full_info)
    else:
        bot.send_message(chat_id, "Hali foydalanuvchi ro'yxatdan o'tmagan")


#######################################################################################################################
# Water Accident Condition uchun javob
@bot.message_handler(func=lambda message: message.text == "Water Accident Condition")
def water_accident_condition(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Please, answer the following questions:\n1. Describe the water accident event:",
    )
    users[chat_id]["step"] = 5


@bot.message_handler(
    func=lambda message: users.get(message.chat.id, {}).get("step") == 5
)
def save_water_accident_description(message):
    chat_id = message.chat.id
    users[chat_id]["description"] = message.text
    bot.send_message(
        chat_id, "2. Please, send a picture or video related to the water accident:"
    )
    users[chat_id]["step"] = 6


@bot.message_handler(
    content_types=["photo", "video"],
    func=lambda message: users.get(message.chat.id, {}).get("step") == 6,
)
def save_water_accident_media(message):
    chat_id = message.chat.id
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    else:
        file_id = None

    users[chat_id]["media"] = file_id
    bot.send_message(chat_id, "3. Please, share your current location:")
    users[chat_id]["step"] = 7


@bot.message_handler(
    content_types=["location"],
    func=lambda message: users.get(message.chat.id, {}).get("step") == 7,
)
def save_water_accident_location(message):
    chat_id = message.chat.id
    location = message.location
    users[chat_id]["location"] = location
    bot.send_message(
        chat_id, "Thank you for sharing the information. Your data has been recorded."
    )
    send_water_accident_info(chat_id)


# User's list
water_accident_info = {}


# Group chat ID where you want to send the information
group_chat_id = -1001836247656

# ... (rest of your code)


# Sending Water Accident Information to a specific group
def send_water_accident_info(chat_id):
    if chat_id in users:
        user_data = users[chat_id]
        accident_info = f"User's Full Name: {user_data['name']}\nUser's Phone: {user_data['phone']}\n\n\n\n"
        accident_info += (
            f"Water Accident Description: {user_data.get('description', 'N/A')}\n\n"
        )
        accident_info += f"Media (Photo/Video): {user_data.get('media', 'N/A')}\n\n"

        # Check if location data exists
        location = user_data.get("location")
        if location:
            latitude = location.latitude
            longitude = location.longitude
            accident_info += f"Location: Latitude: {latitude}, Longitude: {longitude}\n"
        else:
            accident_info += "Location: N/A\n"

        # Send the information to the group chat
        bot.send_message(group_chat_id, accident_info)


# Botni ishga tushirish

if __name__ == "__main__":
    bot.polling(none_stop=True)
