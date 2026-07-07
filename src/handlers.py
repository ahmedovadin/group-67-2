from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.questions import QUESTIONS
from src.keyboards import (
    keyboard_languages,
    inline_help_buttons,
    inline,
    keyboard_quiz_replay
)


router = Router()


class Quiz(StatesGroup):
    waiting_answer = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.first_name}! Я твой первый бот.\n'
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

@router.message(Command('game'))
async def cmd_game(message: Message):
    await message.answer("Выберите один пункт", reply_markup=inline)

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
async def csharp_info(message: Message):
    await message.answer(
        'C# - это универсальный и мощный объектно-ориентированный язык от Microsoft.'
        'Он прост для старта благодаря понятному синтаксису, '
        'но при этом позволяет создавать профессиональные и сложные решения: от мобильных приложений до современных видеоигр и масштабных корпоративных систем',
        parse_mode="HTML",
    )


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы готовы?', show_alert=True)
    await state.update_data(index=0, score=0)
    await state.set_state(Quiz.waiting_answer)  # переходим в состояние waiting_answer
    await callback.message.answer(f"Вопрос 1: {QUESTIONS[0]['q']}")

@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]

    user_answer = message.text.strip().lower()
    if user_answer == QUESTIONS[index]['a']:
        score += 1
        await message.answer("Правильно! +1")
    else:
        await message.answer(f"Неверно! Правильный ответ: {QUESTIONS[index]['a']}")

    index += 1
    if index >= len(QUESTIONS):
        await message.answer(f"Конец! Счет: {score}/{len(QUESTIONS)}", reply_markup=keyboard_quiz_replay)
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {QUESTIONS[index]['q']}")

@router.callback_query(F.data == "start_learning")
async def start_learning(callback: CallbackQuery):
    await callback.answer('Начинаем обучение', show_alert=True)

@router.message(F.text == "Корзина")
async def get_group(message: Message):
    await message.answer("привет, примерно вот твоя корзина !!!!")


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")