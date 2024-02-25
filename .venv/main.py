from aiogram import Bot, Dispatcher,types
from aiogram.utils import executor
BOT_TOKEN = "6219000255:AAH83kGJuT2HtYj53nWQ5gkMLLiZVG9lMwc"
WEATHER_TOKEN = "56b30cb255.3443075"
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def cmd_start(msg: types.Message):
    await msg.answer("Good morning, Weather Hackers!")

if __name__  == "__main__":
    executor.start_polling(dp)