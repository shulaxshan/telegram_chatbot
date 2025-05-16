import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token= TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I'm your echo bot. Send me any message and I'll echo it back!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    

if __name__ == '__main__':
    # Start polling
    executor.start_polling(dp, skip_updates=True)