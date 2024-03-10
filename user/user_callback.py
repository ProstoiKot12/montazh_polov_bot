from aiogram import Bot

from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.text import *
from user.user_keyboards import main_menu_return_kb, main_menu_call_kb, choices_color_kb


class Form(StatesGroup):
    start_of_recording_count = State()
    start_of_recording_name = State()


async def sign_up_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    await call.message.answer('Введите имя и фамилию')
    await state.set_state(Form.start_of_recording_name)


async def about_info_callback(call: CallbackQuery, bot: Bot):
    await call.answer('')
    await call.message.delete()
    await call.message.answer(about_info_text, reply_markup=main_menu_return_kb)


async def contacts_callback(call: CallbackQuery):
    await call.answer('')
    await call.message.delete()
    await call.message.answer(contacts_text, reply_markup=main_menu_return_kb, disable_web_page_preview=True)


async def services_list_callback(call: CallbackQuery):
    await call.answer('')
    await call.message.delete()
    await call.message.answer(services_list_text, reply_markup=main_menu_return_kb)


async def price_list_callback(call: CallbackQuery):
    await call.answer('')
    await call.message.delete()
    await call.message.answer(price_list_text, reply_markup=main_menu_return_kb)


async def main_menu_return_callback(call: CallbackQuery, bot: Bot):
    await call.answer('')
    await call.message.delete()
    photo = FSInputFile("files/main_menu_photo.jpg")
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo, caption=start_text,
                         reply_markup=main_menu_call_kb)
