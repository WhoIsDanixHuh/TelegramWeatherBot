import requests
import logging

from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, OPENWEATHER_API_TOKEN, WEATHER_INFORMATION_FORMAT

logging.basicConfig(level=logging.INFO)

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

def getCardinalDirection(angle: int) -> str:
    directions = ["↑ N", "↗ NE", "→ E", "↘ SE", "↓ S", "↙ SW", "← W", "↖ NW"]
    return directions[round(angle / 45) % 8]

@dp.message_handler(commands=["start", "help"])
async def start_handler(message: types.Message):
    await message.reply("Hello! I am weather bot which gives weather information for any city. Just type name of the city and I will send you the information.")

@dp.message_handler()
async def weather_information_request_handler(message: types.Message):
    req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric&appid={OPENWEATHER_API_TOKEN}")
    result = req.json()
    
    if result["cod"] == "404":
        await message.reply(f"Failed to get weather information: {result['message']}")
        return

    city_name = result["name"]
    country_code = result["sys"]["country"]

    weather = result["weather"][0]["main"]
    weather_description = result["weather"][0]["description"]

    temp = result["main"]["temp"]
    feels_like = result["main"]["feels_like"]
    temp_min = result["main"]["temp_min"]
    temp_max = result["main"]["temp_max"]
    pressure = round(result["main"]["pressure"] * 0.75006375541921)
    humidity = result["main"]["humidity"]

    wind_speed = result["wind"]["speed"]
    wind_direction = getCardinalDirection(result["wind"]["deg"])
    wind_gust = result["wind"].get("gust", "(unknown)")

    visibility = round(result["visibility"] / 1000)
    cloudiness = result["clouds"]["all"]

    rain_volume_1h = "(unknown)"
    rain_volume_3h = "(unknown)"

    if "rain" in result:
        rain_volume_1h = result["rain"]["1h"]
        
        if "3h" in result["rain"]:
            rain_volume_3h = result["snow"]["3h"]

    snow_volume_1h = "(unknown)"
    snow_volume_3h = "(unknown)"

    if "snow" in result:
        snow_volume_1h = result["snow"]["1h"]

        if "3h" in result["snow"]:
            snow_volume_3h = result["snow"]["3h"]

    sea_level = round(result["main"]["sea_level"] * 0.75006375541921) if ("sea_level" in result["main"]) else "(unknown)"
    grnd_level = round(result["main"]["grnd_level"] * 0.75006375541921) if ("grnd_level" in result["main"]) else "(unknown)"

    sunrise = datetime.fromtimestamp(result["sys"]["sunrise"]).strftime("%H:%M:%S")
    sunset = datetime.fromtimestamp(result["sys"]["sunset"]).strftime("%H:%M:%S")

    await message.reply(WEATHER_INFORMATION_FORMAT.format(
        city_name,
        country_code,

        weather,
        weather_description,

        temp,
        feels_like,
        temp_min,
        temp_max,
        pressure,
        humidity,

        wind_speed,
        wind_direction,
        wind_gust,

        visibility,
        cloudiness,

        rain_volume_1h,
        rain_volume_3h,

        snow_volume_1h,
        snow_volume_3h,

        sea_level,
        grnd_level,

        sunrise,
        sunset,
    ))

def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()