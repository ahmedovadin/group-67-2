from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from src.keyboards import keyboard_languages, inline_help_buttons

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.first_name}! Я твой первый бот.'
        'Выберите язык программирования',
        reply_markup=keyboard_languages
    )

    print(f"Пользователь {message.from_user.full_name} отправил {message.text} в {message.date}")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - приветствие\n'
        '/help - список команд',
        reply_markup=inline_help_buttons
    )

@router.message(F.text == "Python")
async def python_info(message: Message):
    await message.answer(
        'Python — это один из самых популярных и доступных языков программирования.'
        'Благодаря простому синтаксису, похожему на обычный английский язык, он легко читается и изучается. '
        'Python универсален и применяется для создания сайтов, работы с данными, автоматизации задач и искусственного интеллекта',
        parse_mode="HTML",
    )

@router.message(F.text == "JavaScript")
async def js_info(message: Message):
    await message.answer(
        'JavaScript (JS) — это главный язык программирования для интернета'
        'Он заставляет веб-страницы «оживать». '
        'Если HTML отвечает за структуру сайта, а CSS — за его внешний вид, то JavaScript отвечает за логику и интерактивность',
        parse_mode="HTML",
    )

@router.message(F.text == "C#")
async def js_info(message: Message):
    await message.answer(
        'C# - это универсальный и мощный объектно-ориентированный язык от Microsoft.'
        'Он прост для старта благодаря понятному синтаксису, '
        'но при этом позволяет создавать профессиональные и сложные решения: от мобильных приложений до современных видеоигр и масштабных корпоративных систем',
        parse_mode="HTML",
    )


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery):
    await callback.answer('Вы готовы?', show_alert=True)
    await callback.message.answer("Начинаем тест!")

@router.callback_query(F.data == "start_learning")
async def start_learning(callback: CallbackQuery):
    await callback.answer('Начинаем обучение', show_alert=True)

@router.message(F.text == "Корзина")
async def get_group(message: Message):
    await message.answer("привет, примерно вот твоя корзина !!!!")


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")