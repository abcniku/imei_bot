from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_admin_api = InlineKeyboardButton('Api-ключи', callback_data='admin_api')
btn_admin_wl = InlineKeyboardButton('WL-список', callback_data='admin_wl')
kb_admin = InlineKeyboardMarkup(inline_keyboard=[[btn_admin_api, btn_admin_wl]])

btn_wl_add = InlineKeyboardButton('Добавить', callback_data='wl_add')
btn_wl_remove = InlineKeyboardButton('Убрать', callback_data='wl_remove')
btn_wl_show = InlineKeyboardButton('Все WL', callback_data='wl_show')
kb_wl = InlineKeyboardMarkup(inline_keyboard=[[btn_wl_add, btn_wl_show, btn_wl_remove]])

btn_api_add = InlineKeyboardButton('Создать ключ', callback_data='api_add')
btn_api_remove = InlineKeyboardButton('Удалить ключ', callback_data='api_remove')
btn_api_show = InlineKeyboardButton('Все ключи', callback_data='api_show')
kb_api = InlineKeyboardMarkup(inline_keyboard=[[btn_api_add, btn_api_show, btn_api_remove]])
