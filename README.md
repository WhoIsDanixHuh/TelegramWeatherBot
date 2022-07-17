# Telegram Weather Bot
Simple Telegram bot which gives weather information for any city using OpenWeather API.

![example_of_bot](https://user-images.githubusercontent.com/108881004/179398843-979dbd73-2c55-4e0c-a6d5-7bb979e39c62.png)

## Installation
Clone this repository to your PC and install all requirements.
```bat
git clone https://github.com/WhoIsDanixHuh/TelegramWeatherBot
cd TelegramWeatherBot
py -m pip install -r requirements.txt
```


Then you will be able to run the bot.
```bat
py main.py
```

## Configuration
Before actually running the bot, you need to modify config.py file.

In config.py you have 3 variables:


**TELEGRAM_BOT_TOKEN** - Your telegram bot token (you can get it from BotFather bot)


**OPENWEATHER_API_TOKEN** - OpenWeather API token (get it on [OpenWeather](https://openweathermap.org) by creating account)


**WEATHER_INFORMATION_FORMAT** - Weather information format, you can modify it as you want
