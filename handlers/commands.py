from aiogram import types
from aiogram.types import ParseMode

from keyboards.menu import main_menu
from loader import dp
from states import BotStates


@dp.message_handler(commands='start')
@dp.message_handler(lambda message: message.text in ["Назад"], state='*')
async def cmd_start(message: types.Message):
    text = "Что бы вы хотели?"
    await BotStates.start.set()
    await message.answer(text, reply_markup=main_menu, parse_mode=ParseMode.MARKDOWN)
