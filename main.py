from aiogram import Bot, Dispatcher
import asyncio

from hendlers import router
from hendlers_admin import admin_router

from dotenv import load_dotenv
import os


load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())