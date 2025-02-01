from aiogram.types import Message, CallbackQuery
from kb import *

async def t_start(message: Message):
    message.answer('Вызван START')

async def t_admin(message:Message):
    message.anwer('Вы в админ панели', kb_admin)

async def t_api(call: CallbackQuery):
    call.message.edit_reply_markup(kb_api)

async def t_wl(call: CallbackQuery):
    call.message.edit_reply_markup(kb_wl)

async def t_api(call: CallbackQuery):
    call.message.edit_text()