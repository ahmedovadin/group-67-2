import asyncio

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command

BOT_TOKEN = "1234567890:AABBccDDeeFFggHHiiJJkkLLmmNNooPPqqRR"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()  # обработчик входящих обновлений

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я твой первый бот.')

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - приветствие\n'
        '/help - список команд\n'
        '/about - о боте'
    )

@dp.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer(
        'Я твой учебный бот, '
        'созданный для практики работы с aiogram '
        'Умею отвечать на команды /start, /help и /about'
    )

async def main():
    await dp.start_polling(bot)  # отправляет запросы на тг-сервер

if __name__ == '__main__':
    asyncio.run(main()) # для запуска асинк функции