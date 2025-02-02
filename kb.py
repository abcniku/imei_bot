from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_imei = InlineKeyboardButton(text='IMEI', callback_data = 'IMEI')
kb_start = InlineKeyboardMarkup(inline_keyboard=[[btn_imei]])

btn_wl_add = InlineKeyboardButton(text='Добавить', callback_data='wl_add')
btn_wl_remove = InlineKeyboardButton(text='Убрать', callback_data='wl_remove')
btn_wl_show = InlineKeyboardButton(text='Все WL', callback_data='wl_show')
kb_wl = InlineKeyboardMarkup(inline_keyboard=[[btn_wl_add, btn_wl_remove], [btn_wl_show]])

kb_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='back')]])
