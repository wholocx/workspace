import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, types, F, utils
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
import config
from states import FSMSettings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
lang = "ru"
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    kb = [
        [
        types.KeyboardButton(text="🎯Отправить геолокацию🎯", request_location=True),
        # types.KeyboardButton(text="🌄Узнать погоду сейчас", request_location=True),
        # types.KeyboardButton(text="🌆Узнать погоду на 5 дней",  request_location=True)
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Пробиваем ваш IP"
    )
    await msg.answer("🐉Good morning, Weather Hackers!🐉 \n Перед началом работы отправь мне свою геолокацию", reply_markup=keyboard)


@dp.message(F.location, StateFilter(FSMSettings.set_location))
async def weather_at_moment(msg: types.Message, state: FSMContext):
    lat = msg.location.latitude
    lon = msg.location.longitude

    result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.WEATHER_TOKEN}&lang={lang}&units=metric")
    data = result.json()
    await msg.reply(f"""        Погода сегодня: 
Краткое описание: {data["weather"]["description"]}
Температура: {data["main"]["temp"]} градусов, ощущается как {data["main"]["feels_like"]};
Атмосферное давление: {data["main"]["pressure"]};
Скорость ветра  {data["wind"]["speed"]}
""")

@dp.message(Command("ну_сука!", prefix="%"))
async def cmd_custom1(msg: Message):
    await msg.answer("Сам сука!!")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":  
    asyncio.run(main())