import asyncio
import logging

from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from src.handlers import router
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # обработчик входящих обновлений

async def main():
    # await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)  # отправляет запросы на тг-сервер

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()) # для запуска асинк функции