import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os
import openai
import sys

# Load environment variables from .env file
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = os.getenv("OPEN_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

class Reference:
    '''A class to store previous responses from OpenAI API.'''
    def __init__(self):
        self.response = ""


reference = Reference()
model_name = 'gpt-4.1-nano'

# Initialize bot and dispatcher
bot = Bot(token= TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


def clear_conversation():
    '''Clears the conversation history.'''
    reference.response = ""

@dp.message_handler(commands=['clear'])
async def clear(message: types.Message):
    '''Handles the /clear command.'''
    clear_conversation()
    await message.reply("Conversation cleared.")



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I'm your echo bot!\nCreated by Chulaxshan.\nHow can i assist you?")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):

    help_command = """
    Hi There, I'm your assistant bot created by chulaxshan Please follow the commands below to interact with me:
    /start - Start the bot
    /help - Get help
    /clear - Clear the conversation
    I hope this helps. :)
    """
    await message.reply(help_command)


##### ChatGPT API
@dp.message_handler()
async def chatgpt(message: types.Message):
    '''Handles incoming messages and responds using OpenAI API.'''
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ],
        temperature=0.7,
        max_tokens=20
    )
    reference.response = response['choices'][0]['message']['content']
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)


if __name__ == '__main__':
    # Start polling
    executor.start_polling(dp, skip_updates=True)