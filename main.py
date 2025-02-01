import asyncio
import aiohttp
import logging
import sqlite3 
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import *
from texts import *
from db import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Auth(StatesGroup):
    api_token = (State)

@dp.message(Command('start'))
async def start(message: Message):
    await (t_start)

@dp.message(Command('admin'))
async def admin(message:Message):
    if message.from_user.id in admin_list:
        await (t_admin)

@dp.callback_query(F.data == 'admin_api')
async def api(call: CallbackQuery):
    await (t_api)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
