import sqlite3
from aiogram.types import Message, CallbackQuery
from kb import *
from config import *

async def t_start(message: Message, white_list):
    if (message.from_user.username in white_list) or (message.from_user.id in admin_list):
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO users (username) VALUES (?)
            ''',
            (message.from_user.username,))
        await message.answer('Привет! Это бот для получения информации об устройстве по его IMEI.\nДля начала добавь API-ключ с сайта https://imeicheck.net/', reply_markup=kb_start)
    else:
        await message.answer('Вы не в белом списке')

async def t_start_callback(call: CallbackQuery, white_list):
    if (call.from_user.username in white_list) or (call.from_user.id in admin_list):
        with sqlite3.connect('db.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO users (username) VALUES (?)
            ''',
            (call.from_user.username,))
        await call.message.answer('Привет! Это бот для получения информации об устройстве по его IMEI.\nДля начала добавь API-ключ с сайта https://imeicheck.net/', reply_markup=kb_start)
    else:
        await call.message.answer('Вы не в белом списке')

async def t_wl(message: Message):
    if message.from_user.id in admin_list:
        await message.answer('Здесь можно управлять белым списком', reply_markup=kb_wl)
    else:
        await message.answer('Вы не администратор.')

async def t_wl_add(message: Message):
    await message.answer('Ввелите имя пользователя без @', reply_markup=kb_back)

async def t_wl_success(call: CallbackQuery):
    await call.message.edit_text('Пользователь успешно добавлен в WhiteList!', reply_markup=kb_wl)

async def t_wl_remove(call: CallbackQuery):
    await call.message.answer('Введите имя пользователя без @', reply_markup=kb_back)

async def t_wl_remove_success(message: Message):
    await message.answer('Пользователь удален из WhiteList.', reply_markup=kb_wl)

async def t_wl_show(call: CallbackQuery, context):
    await call.message.answer('WhiteList: \n'+context, reply_markup=kb_wl)

async def t_api_add(call: CallbackQuery):
    await call.message.answer('Введите API-ключ:', reply_markup=kb_back)

async def t_api_success(message: Message):
    await message.answer('API-ключ успешно добавлен!', reply_markup=kb_start)

async def t_api_remove(call: CallbackQuery):
    await call.message.answer('API-ключ удален.', reply_markup=kb_start)

async def t_imei_entry(call: CallbackQuery):
    await call.message.answer('Введите IMEI:', reply_markup=kb_back)
