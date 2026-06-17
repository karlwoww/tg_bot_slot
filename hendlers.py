import asyncio

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from slot import slot_result, slot_description

from db import conn, cursor, add_balance, set_user_balance, get_balance, user_exists, get_players_sorted_by_balance

from hendlers_admin import ADMIN_IDS
from  middleware import rate_limit_button
import keyboard

router = Router()


class Slot_bet(StatesGroup):
    bet = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.full_name
    if not user_exists(user_id):
        cursor.execute('INSERT INTO users (id, username ,balance) VALUES (?, ?, ?)', (user_id, name, 1000))
        conn.commit()
        await message.answer("Привет! Ты добавлен в систему. Твой баланс: 1000 руб.",
                             reply_markup=keyboard.kb_main_menu)
    else:
        await message.answer("Привет! Ты уже зарегистрирован.", reply_markup=keyboard.kb_main_menu)


@router.message(F.text == 'TOP')
async def top(message: types.Message):
    players_list = [f'{n}: {b}' for i, n, b in sorted(get_players_sorted_by_balance(), key=lambda x: x[1])[:5]]
    r = '\n'.join([f'{i + 1}. {players_list[i]} руб.' for i in range(len(players_list))])
    await message.answer(f'{r}')



@router.message(F.text == 'Слот-машина')
async def slot_mach(message: types.Message, state: FSMContext):
    await state.set_state(Slot_bet.bet)
    await message.answer('Выберите ставку в рублях', reply_markup=keyboard.kb_slot_bet)


@router.callback_query(F.data.startswith('slot_button'))
async def slot_switch(callback_query: types.CallbackQuery, state: FSMContext):
    bet = int(callback_query.data.split('_')[-1])
    await state.update_data(bet=bet)
    await callback_query.message.answer(f'Ставка принята {bet}', reply_markup=keyboard.kb_slot_play)


@router.callback_query(F.data == 'slot_play_bet')
async def slot_new_bet(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Slot_bet.bet)
    await callback_query.message.answer('Выберите ставку в рублях', reply_markup=keyboard.kb_slot_bet)


@router.callback_query(F.data == 'slot_play_info')
async def slot_info(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f"{slot_description}"
                                        , reply_markup=keyboard.kb_slot_play)


@router.callback_query(F.data == 'slot_play_go')
@rate_limit_button(rate_limit=10.0)
async def play_slot(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    balance = get_balance(user_id)
    data = await state.get_data()
    bet = int(data['bet'])
    if bet <= balance:
        sent_dice = await callback_query.message.answer_dice(emoji='🎰')
        await asyncio.sleep(2)
        dice_value = sent_dice.dice.value
        result, txt = slot_result(dice_value, bet)
        add_balance(callback_query.from_user.id, result)
        await callback_query.message.answer(f'\n{txt}\nБаланс: {get_balance(user_id)} руб.\nCтавка: {bet} руб.',
                                            reply_markup=keyboard.kb_slot_play)
    else:
        await state.clear()
        await callback_query.message.answer(f'Куда? Ты нищий!\nМеняй ставку гой')


@router.callback_query(F.data == 'slot_play_exit')
async def exit_slot(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer('До свидания, заходи ещё', reply_markup=keyboard.kb_main_menu)


@router.message(F.text == 'Обновить баланс')
async def ref_balance(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f'Ты ещё гой для этого.\nНапишите администратору @sc5423')
    else:
        set_user_balance(message.from_user.id)
        await message.answer(f'Баланс успешно обновлён')


@router.message(F.text == 'Баланс')
async def balance_full(message: types.Message):
    balance = get_balance(message.from_user.id)
    await message.answer(f'Ваш баланс: {balance} руб.')


@router.message(Command('myid'))
async def id(message: types.Message):
    await message.answer(f'{message.from_user.id}')