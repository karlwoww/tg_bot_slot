from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Слот-машина'),
            KeyboardButton(text='Обновить баланс'),
            KeyboardButton(text='Баланс'),
            KeyboardButton(text='TOP'),
        ]
    ],
    resize_keyboard=True,
)



kb_slot_bet = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='8', callback_data='slot_button_8'),
            InlineKeyboardButton(text='16', callback_data='slot_button_16'),
            InlineKeyboardButton(text='20', callback_data='slot_button_20'),
            InlineKeyboardButton(text='32', callback_data='slot_button_32'),
            InlineKeyboardButton(text='50', callback_data='slot_button_50'),
        ],
        [
            InlineKeyboardButton(text='75', callback_data='slot_button_75'),
            InlineKeyboardButton(text='100', callback_data='slot_button_100'),
            InlineKeyboardButton(text='150', callback_data='slot_button_150'),
            InlineKeyboardButton(text='200', callback_data='slot_button_200'),
            InlineKeyboardButton(text='300', callback_data='slot_button_300'),
        ],
[
            InlineKeyboardButton(text='400', callback_data='slot_button_400'),
            InlineKeyboardButton(text='500', callback_data='slot_button_500'),
            InlineKeyboardButton(text='600', callback_data='slot_button_600'),
            InlineKeyboardButton(text='700', callback_data='slot_button_700'),
            InlineKeyboardButton(text='800', callback_data='slot_button_800'),
        ],
        [
            InlineKeyboardButton(text='1000', callback_data='slot_button_1000'),
            InlineKeyboardButton(text='1500', callback_data='slot_button_1500'),
            InlineKeyboardButton(text='2500', callback_data='slot_button_2500'),
            InlineKeyboardButton(text='5000', callback_data='slot_button_5000'),
            InlineKeyboardButton(text='10000', callback_data='slot_button_10000'),
        ],

    ]
)

kb_slot_play = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='GO', callback_data='slot_play_go'),
            InlineKeyboardButton(text='Поменять ставку', callback_data='slot_play_bet'),

        ],
        [
            InlineKeyboardButton(text='Информация о слоте', callback_data='slot_play_info'),
            InlineKeyboardButton(text='Выйти', callback_data='slot_play_exit')
        ]
    ]
)

kb_admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Обновить баланс игрока', callback_data='refresh_balance_admin'),
            InlineKeyboardButton(text='Добавить админа', callback_data='add_admin'),
        ]
    ]
)