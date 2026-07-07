from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton
                           )


keyboard_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Корзина")],
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Каталог")]
], resize_keyboard=True, input_field_placeholder="Выберите один пункт")


inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg")],
    [InlineKeyboardButton(text="Начать викторину", callback_data="quiz_start")],
])

keyboard_languages = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Python'),
            KeyboardButton(text='JavaScript'),
            KeyboardButton(text='C#')
        ]
    ],
    resize_keyboard=True,
    input_field_placehodler='Выберите язык программирования'
)

inline_help_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text='Python official doc', url="https://docs.python.org/3/")],
        [InlineKeyboardButton(text='JavaScript official doc', url="https://developer.mozilla.org/ru/docs/Web/JavaScript")],
        [InlineKeyboardButton(text='C# official doc', url="https://learn.microsoft.com/ru-ru/dotnet/csharp/")],
        [InlineKeyboardButton(text="Начать обучение", callback_data="start_learning")],

    ]
)

keyboard_quiz_replay = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Сыграть снова', callback_data='quiz_start')],
    ]
)