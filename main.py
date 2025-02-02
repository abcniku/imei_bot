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
    username = State()
    api_key = State()

class Imei(StatesGroup):
    imei = State()

# Подключение к базе данных SQLite
with sqlite3.connect('db.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        api_key TEXT DEFAULT NULL
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
    
async def get_api_key(username):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE username = ?
        ''', (username,))
        api_key = cursor.fetchone()
        return api_key
    
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
    await state.set_state(User.username)
    await t_wl_add(call)

@dp.message(User.username)
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
    await state.set_state(User.username)
    await t_wl_remove(call)

@dp.message(User.username)
async def wl_remove_success(message: Message, state: FSMContext):
    await state.clear()
    username = message.text

    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM user WHERE username = ?
        ''',
        (username,))
    await t_wl_remove_success(message)

@dp.callback_query(F.data == 'wl_show')
async def wl_show(call: CallbackQuery):
    users = get_wl_list()
    for user in users:
        context += f'{user[0]}\n'
    await t_wl_show(call, context)

#API
@dp.callback_query(F.data == 'api_add')
async def api_add(call: CallbackQuery, state: FSMContext):
    await state.set_state(User.api_key)
    await t_api_add(call)

@dp.message(User.api_key)
async def api_add_success(message: Message, state: FSMContext):
    await state.clear()
    api_key = message.text
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users SET api_key = ? WHERE username = ?
        ''',
        (api_key, message.from_user.username))
    await t_api_success(message)

@dp.callback_query(F.data == 'api_remove')
async def api_remove(call: CallbackQuery):
    with sqlite3.connect('db.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users SET api_key = NULL WHERE username = ?
        ''', (call.from_user.username,))
    await t_api_remove(call)

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
    api_key = await get_api_key(message.from_user.username)

    headers = {
    'Authorization': f'Bearer {api_key[1]}',
    'Content-Type': 'application/json'
    }

    body =  json.dumps({
    "deviceId": f'{imei}',
    "serviceId": 12
    })

    data = await send_post_request(url, headers, body)
    if data:
        await message.answer(f"Данные получены: \n{data}")
    else:
        await message.answer("Не удалось получить данные.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
