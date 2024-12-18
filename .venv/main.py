#Library import
import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Token initialization and Temporary lang variable (will be changed to lang choise)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
lang = "ru"
msgIds = []

def emojiChoice(description):
    # 🌥🌦🌧⛈🌨🌤
    if "дожд" in description:
        return "🌨"
    elif "метель" in description or "снег" in description:
        return "❄"
    elif "ясно" in description:
        return "☀️"
    elif "облач" in description:
        return "⛅️"
    elif "пасмурно" in description:
        return "☁️"
    elif "гроза" in description:
        return "🌩"
    elif "туман" in description:
        return "😶‍🌫️"
    
# start command reaction
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    kb = [
        [
        types.KeyboardButton(text="Передать локацию", request_location=True)
        ],
    ] 
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Пробиваем ваш IP"
    )
    msgIds.append(msg.message_id)
    message = await msg.answer("🐉Good morning, Weather Hackers!🐉 \n Перед началом работы отправь мне свою геолокацию", reply_markup=keyboard)
    msgIds.append(message.message_id)

# getting location data and mode choice
@dp.message(F.location)
async def location_get(msg: types.Message):
    global lat 
    lat = msg.location.latitude
    global lon 
    lon = msg.location.longitude
    print(lat, lon)
    kb = [
        [
        types.KeyboardButton(text="🌄Узнать погоду сейчас"),
        types.KeyboardButton(text="🌆Узнать погоду на 5 дней"),
        ],
        [types.KeyboardButton(text="🧽Очистить и вернуться к началу🧽")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Шаманы колдуют погоду"
    )
    msgIds.append(msg.message_id)
    message = await msg.answer("Выбери интересующий вариант: ", reply_markup=keyboard)
    msgIds.append(message.message_id)

# get weather data at the moment 
@dp.message(F.text == "🌄Узнать погоду сейчас")
async def weather_at_the_moment(msg: types.Message):
    result = await asyncio.to_thread(requests.get, f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.WEATHER_TOKEN}&lang={lang}&units=metric")
    data = result.json()
    nearby_location = data["name"]
    cur_temp = data["main"]["temp"]
    feels = data['main']['feels_like']
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    desc = data["weather"][0]["description"]
    msgIds.append(msg.message_id)
    message = await msg.reply(f"""Погода сегодня
🌐Район: {nearby_location}🌐
Краткое описание: {desc}{emojiChoice(desc)}
🤒Температура: {cur_temp}°C🤒
🌡Ощущается как {feels}°C🌡
🧱Атмосферное давление: {pressure}Па🧱
💨Скорость ветра  {wind} м/с💨
🫧Влажность: {humidity}%🫧
Короче, на пары можно не идти""")
    msgIds.append(message.message_id)

# get weather data for 5 days
@dp.message(F.text == "🌆Узнать погоду на 5 дней")
async def weather_at_the_moment(msg: types.Message):
    result = await asyncio.to_thread(requests.get, f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={config.WEATHER_TOKEN}&lang={lang}&units=metric")
    data = result.json()
    nearby_location = data["city"]["name"]
    prev_date = ""
    for date in data["list"]:
        if prev_date != date["dt_txt"][:10]:
            cur_temp = date["main"]["temp"]
            feels = date['main']['feels_like']
            humidity = date["main"]["humidity"]
            pressure = date["main"]["pressure"]
            wind = date["wind"]["speed"]
            desc = date["weather"][0]["description"]
            date_today = date["dt_txt"][:10]
            msgIds.append(msg.message_id)
            message = await msg.reply(f"""Погода {date_today}
🌐Район: {nearby_location}🌐
Краткое описание: {desc}{emojiChoice(desc)}
🤒Температура: {cur_temp}°C🤒
🌡Ощущается как {feels}°C🌡
🧱Атмосферное давление: {pressure}Па🧱
💨Скорость ветра  {wind} м/с💨
🫧Влажность: {humidity}%🫧""")
            prev_date = date_today
            msgIds.append(message.message_id)

# get weather data for 5 days
@dp.message(F.text == "🧽Очистить и вернуться к началу🧽")
async def clearing(msg: types.Message):
    index = msg.chat.id    
    msgIds.append(msg.message_id)
    await bot.delete_messages(index, msgIds)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":  
    asyncio.run(main())
