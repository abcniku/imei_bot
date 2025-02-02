import asyncio
import aiohttp
import logging
import sqlite3 
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import *
from texts import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class User(StatesGroup):
    remove = State()
    add = State()

class Imei(StatesGroup):
    imei = State()

# Подключение к базе данных SQLite
with sqlite3.connect('db.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY
        )
        ''')

async def send_post_request(url, headers, body):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=body) as response:
            if response:
                return await response.json()
            else:
                return None

async def get_wl_list():
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users
        ''')
        white_list = cursor.fetchall()

        return white_list
    
#Start
@dp.message(Command('start'))
async def start(message: Message):
    white_list = await get_wl_list()
    await t_start(message, white_list)

@dp.callback_query(F.data == 'back')
async def start_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    white_list = await get_wl_list()
    await t_start_callback(call, white_list)

#WL
@dp.message(Command('wl'))
async def wl(message: Message):
    await t_wl(message)

@dp.callback_query(F.data == 'wl_add')
async def wl_add(call: CallbackQuery, state: FSMContext):
    await state.set_state(User.add)
    await t_wl_add(call)

@dp.message(User.add)
async def wl_add_success(message: Message, state: FSMContext):
    await state.clear()
    username = message.text

    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (username) VALUES (?)
        ''',
        (username,))
    await t_wl_success(message)

@dp.callback_query(F.data == 'wl_remove')
async def wl_remove(call: CallbackQuery, state: FSMContext):
    await state.set_state(User.remove)
    await t_wl_remove(call)

@dp.message(User.remove)
async def wl_remove_success(message: Message, state: FSMContext):
    await state.clear()
    username = message.text

    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM users WHERE username = ?
        ''',
        (username,))
    await t_wl_remove_success(message)

@dp.callback_query(F.data == 'wl_show')
async def wl_show(call: CallbackQuery):
    users = await get_wl_list()
    context = ''
    for user in users:
        context += f'@{user[0]}\n'
    await t_wl_show(call, context)

#IMEI
@dp.callback_query(F.data == 'IMEI')
async def imei_entry(call: CallbackQuery, state: FSMContext):
    await state.set_state(Imei.imei)
    await t_imei_entry(call)

@dp.message(Imei.imei)
async def imei_final(message: Message, state: FSMContext):
    await state.clear()
    imei = message.text

    url = "https://api.imeicheck.net/v1/checks"
    api_key = api_key

    headers = {
    'Authorization': f'Bearer {api_key[1]}',
    'Content-Type': 'application/json'
    }

    body =  json.dumps({
    "deviceId": f'{imei}',
    "serviceId": 12
    })

    data = await send_post_request(url, headers, body)
    data = data['properties']
    if data:
        await message.answer(f"Данные получены: \nДевайс: {data['deviceName']}\nОписание: {data['modelDesc']}\nIMEI: {data['imei']}\nMEID: {data['meid']}\nСерийный номер: {data['serial']}", reply_markup=kb_start)
    else:
        await message.answer("Не удалось получить данные.", reply_markup=kb_start)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
