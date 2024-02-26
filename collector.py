from aiogram import Bot
from dotenv import dotenv_values
import os 

from emote_collector import dp

env = dotenv_values(".env")
for k, v in env.items():
    os.environ[k] = v

if __name__ == "__main__":
    bot = Bot(token = env["BOT_TOKEN"])

    dp.start_polling(bot)

