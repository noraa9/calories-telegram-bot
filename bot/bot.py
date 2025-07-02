import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from handlers import register_handlers

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

register_handlers(dp)

if __name__ == "__main__":
    print("🤖 Бот запущен...")
    asyncio.run(dp.start_polling(bot))
