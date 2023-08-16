from tabulate import tabulate
from telebot import types
from config import bot
from handlers import handlers


def get_contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_contact = types.KeyboardButton("Share Contact", request_contact=True)
    keyboard.add(button_contact)
    return keyboard



# Foydalanuvchi malumotlarini faylga saqlash
def save_to_file(chat_id):
    if chat_id in handlers.users:
        user_data = handlers.users[chat_id]
        with open("data.txt", "a", encoding="utf-8") as file:
            file.write(
                f"Chat ID: {chat_id}, Ism: {user_data['name']}, Telefon: {user_data['phone']}\n"
            )

