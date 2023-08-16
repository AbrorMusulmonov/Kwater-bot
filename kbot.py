import requests
from tabulate import tabulate
from config import bot,weather_url
from handlers import handlers



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

# ... (rest of your code)


# Botni ishga tushirish

if __name__ == "__main__":
    bot.polling(none_stop=True)
