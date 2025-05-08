from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton,)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

contact_button = KeyboardButton(text="Поділитися контактом", request_contact=True)

keyboard = ReplyKeyboardMarkup(
    keyboard=[[contact_button]],  
    resize_keyboard=True,
    one_time_keyboard=True
)


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Пропарсити силку', callback_data='pars_link')]
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Налаштування', callback_data='settings')]
])

back_to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
])
