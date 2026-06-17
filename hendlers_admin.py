from aiogram import Router, types, F
from aiogram.filters import Command, Filter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os

import keyboard
from db import set_user_balance, user_exists

admin_router = Router()


class Refresh(StatesGroup):
    id = State()
    balance_player = State()


class AddAdmin(StatesGroup):
    id = State()

class IsAdmin(Filter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in self.admin_ids

load_dotenv()

ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADM_IDS", "865322059").split(",") if id.strip()]

admin_router.message.filter(IsAdmin(ADMIN_IDS))

@admin_router.message(Command('admin'))
async def admin_menu(message: types.Message):
    await message.answer("Вы вошли в панель администратора.", reply_markup=keyboard.kb_admin_menu)


@admin_router.callback_query(F.data == 'refresh_balance_admin')
async def refresh_balance_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Refresh.id)
    await callback_query.message.answer(f'Введите id игрока')

@admin_router.message(Refresh.id)
async def id_player(message: types.Message, state: FSMContext):
    if user_exists(message.text):
        await state.update_data(id=message.text)
        await state.set_state(Refresh.balance_player)
        await message.answer(f'Введите какой баланс поставить игроку')
    else:
        await message.answer(f'Такого пользователя нет в базе данных, Перепроверьте id.')

@admin_router.message(Refresh.balance_player)
async def balance_player(message: types.Message, state: FSMContext):
    await state.update_data(balance_player=message.text)
    data = await state.get_data()
    set_user_balance(data['id'], data['balance_player'])
    await message.answer(f'Успешно')
    await state.clear()


@admin_router.callback_query(F.data == 'add_admin')
async def add_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddAdmin.id)
    await callback_query.message.answer(f'Введите id нового админа')

@admin_router.message(AddAdmin.id)
async def add_admin1(message: types.Message, state: FSMContext):
    if int(message.text) in ADMIN_IDS:
        await message.answer(f'Этот пользователь уже администратор.')
        await state.clear()

    elif user_exists(message.text):
        await state.update_data(id=message.text)
        data = await state.get_data()
        id = data['id']
        ADMIN_IDS.append(int(id))
        await message.answer(f'Администартор добавлен')
        await state.clear()
    else:
        await message.answer('Такого пользователя нет в базе данных, Перепроверьте id.')