from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.questions import (
    get_all_questions,
    add_question,
    delete_question
)
from src.questions import QUESTIONS
from src.keyboards import (
    keyboard_languages,
    inline_help_buttons,
    inline,
    keyboard_quiz_replay
)
from db.users import get_user, create_user
from db.results import get_score, save_result


router = Router()


class Quiz(StatesGroup):
    waiting_answer = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "Аноним"
    )

    await message.answer(
        f'Привет {message.from_user.first_name}! Я твой первый бот. \n{user}'
        'Выберите язык программирования',
        reply_markup=keyboard_languages
    )

    print(f"Пользователь {message.from_user.full_name} отправил {message.text} в {message.date}")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
         "/start - приветствие\n"
        "/help - список команд\n"
        "/game - начать викторину\n"
        "/list - список вопросов\n"
        "/add <текст> <ответ> - добавить вопрос\n"
        "/del <ID> - удалить вопрос",
        reply_markup=inline_help_buttons
    )

@router.message(Command('game'))
async def cmd_game(message: Message):
    await message.answer("Выберите один пункт", reply_markup=inline)


@router.callback_query(F.data == "my_score")
async def my_score(callback: CallbackQuery):
    user = get_user(
        telegram_id=callback.from_user.id
    )

    if not user:
        await callback.answer('User Not Found', show_alert=True)
        return

    data = get_score(
        user_id=user["id"]
    )
    await callback.answer('')
    await callback.message.answer(f'Твой счет: {data["correct"] or 0}/{data["total"] or 0}', show_alert=True)

@router.message(Command('list'))
async def cmd_help(message: Message):
    questions = get_all_questions()
    if not questions:
        await message.answer("Вопросов пока нет")
        return

    lines = ["Список вопросов:"]
    for question in questions:
        lines.append(
            f"{question['id']}. {question['question_text']}"
        )

    await message.answer("\n".join(lines))

@router.message(Command('add'))
async def cmd_help(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(
            "Некорректный формат вопроса\n"
            "Пример: /add Столица Франции? Париж"
        )
        return

    parts = command.args.rsplit(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Некорректный формат вопроса, укажите и вопрос, и ответ\n"
            "Пример: /add Столица Франции? Париж"
        )
        return

    question, answer = parts
    question_text = question.strip()
    correct_answer = answer.strip().lower()
    new_id = add_question(question_text, correct_answer)
    if new_id is None:
        await message.answer(f"Такой вопрос уже есть")
    else:
        await message.answer(f'Вопрос добавлен id {new_id}')

@router.message(Command('del'))
async def cmd_help(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(
            "Некорректный формат удаления вопроса по id\n"
            "Пример: /del <ID>"
        )
        return

    try:
        question_id = int(command.args.strip())
    except ValueError:
        await message.answer('id должен быть числом')
        return

    deleted = delete_question(question_id)
    if deleted:
        await message.answer(f"Вопрос {question_id} удалён")
    else:
        await message.answer(f"Вопрос {question_id} не найден")

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
    questions = get_all_questions()  # Тянем из БД
    if not questions:
        await callback.message.answer('Вопросы нет в базе(')
        return

    await state.update_data(questions=questions, index=0, score=0)
    await state.set_state(Quiz.waiting_answer)  # переходим в состояние waiting_answer
    await callback.message.answer(f"Вопрос 1: {questions[0]["question_text"]}")

 # Принимаем ответ - хендлер сработает ТОЛЬКО в состоянии witing_anwser

@router.message(Quiz.waiting_answer)
async def handle_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    questions = data["questions"]
    score = data["score"]

    user = get_user(message.from_user.id)
    q = questions[index]

    is_correct = message.text.lower() == q["correct_answer"]
    save_result(
        user_id=user["id"],
        question_id=q["id"],
        is_correct=is_correct
    )


    if is_correct:
        score += 1
        await message.answer("Правильно! +1")
    else:
        await message.answer(f"Неверно! Правильынй ответ: {q["correct_answer"]}")

    index += 1
    if index >= len(questions):
        await message.answer(f"Конец! Счет: {score}/{len(questions)}", reply_markup=keyboard_quiz_replay)
        await state.clear()
    else:
        await state.update_data(index=index, score=score)
        await message.answer(f"Вопрос {index + 1}: {questions[index]["question_text"]}")

@router.callback_query(F.data == "start_learning")
async def start_learning(callback: CallbackQuery):
    await callback.answer('Начинаем обучение', show_alert=True)

@router.message(F.text == "Корзина")
async def get_group(message: Message):
    await message.answer("привет, примерно вот твоя корзина !!!!")


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")