from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.parser_olx import*
import app.database.requests as rq

from yarl import URL

import app.keybords as kb

router = Router()


class Reg(StatesGroup):
    name = State()
    number = State()

class ParseOLX(StatesGroup):
    waiting_for_link = State()
    get_link = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await state.set_state(Reg.number)
    await message.reply(f"{message.from_user.first_name}, вітаю! Для продовження користування ботом, необхідно пройти реєстрацію. Натисніть кнопку 'Поділитися контаком'.",
                        reply_markup=kb.keyboard)
    




@router.message(Reg.number, F.contact)
async def reg_number(message: Message, state: FSMContext):
    contact = message.contact
    if contact and contact.user_id == message.from_user.id:
        await state.update_data(number=contact.phone_number)
        data = await state.get_data()
        await message.answer(
            f"Дякуємо за реєстрацію.\n"
            f"Ім'я: {message.from_user.first_name}\n"
            f"Номер: {data['number']}", reply_markup=kb.main
        )
        await state.clear()
    else:
        await message.answer("Не вдалося отримати ваш контакт спробуйте ще раз")
    

@router.message(Command('help'))
async def get_help(message: Message):
   await message.answer('Список команд  /help, '
   '/reg')
   

@router.callback_query(F.data == 'pars_link')
async def handle_pars_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Надішліть посилання на сторінку з товарами.")
    await state.set_state(ParseOLX.get_link)
    await callback.answer()


@router.message(ParseOLX.waiting_for_link)
async def handle_link(message: Message, state: FSMContext):
    text = message.text.strip()
    try:
        u = URL(text)
        if 'olx.ua' not in u.host:
            raise ValueError()
    except Exception:
        return await message.answer("Це не посилання OLX. Спробуйте ще раз.")
    
    status = await message.answer("Паршу...")

    try:
        file_path = parser_olx(text)
    except Exception as e:
        await status.edit_text(f"Сталася помилка: {e}")
        await state.clear()
        return
    
    await status.edit_text("Готово! Ось ваш файл:")
    await message.answer_document(FSInputFile(file_path))
    await state.clear()


@router.message(ParseOLX.get_link)
async def handle_get_link(message: Message, state: FSMContext):
    text = message.text.strip()
    try:
        u = URL(text)
        if 'olx.ua' not in u.host:
            raise ValueError()
    except Exception:
        return await message.answer("Це не посилання OLX. Спробуйте ще раз.")
    
    status = await message.answer("Паршу сторінку з товарами...")
    
    try:
        file_path = parser_olx(text)
        await status.edit_text("Готово! Ось ваш файл:")
        await message.answer_document(FSInputFile(file_path))
    except Exception as e:
        await status.edit_text(f"Сталася помилка: {e}")
        await state.clear()
        return
    
    await state.clear()


@router.callback_query(F.data == 'settings')
async def settings(callback: CallbackQuery):
    await callback.message.answer('Налаштування', reply_markup=kb.settings)
    await callback.answer()


@router.callback_query(F.data == 'back_to_main')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Головне меню",
        reply_markup=kb.main
    )
    await callback.answer()


@router.message()
async def handle_message(message: Message):
    text = message.text.strip()
    try:
        u = URL(text)
        await rq.set_link(text)
        await message.answer("Посилання збережено в базу даних!")
    except Exception:
        pass



