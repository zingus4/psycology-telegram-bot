import logging
import os

from aiogram import types
from aiogram.types import ParseMode

from keyboards.menu import main_menu, smr_keyboard
from loader import dp
from states import BotStates

smr_list = [file.split('.')[0] for file in os.listdir('data/smr')]


@dp.message_handler(lambda message: message.text in ["Подсказки по СМР"], state=BotStates.start)
async def select_hint(message: types.Message):
    text = "Какую подсказску хотели бы получить?"
    await BotStates.smr.set()
    await message.reply(text, reply_markup=smr_keyboard)


@dp.message_handler(lambda message: message.text in smr_list, state=BotStates.smr)
async def show_hint(message: types.Message):
    text = 'К сожалению, такой подсказки у нас нет. Выберите, пожалуйста, подсказку из меню.'
    try:
        with open(f'data/smr/{message.text}.txt', "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        logging.error(message.text)
    await message.answer(text, reply_markup=smr_keyboard, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=BotStates.smr)
async def hint_is_missing_message(message: types.Message):
    logging.error(message.text)
    text = "К сожалению, такой подсказки нет, выберите, пожалуйста, подсказку из меню."
    await message.answer(text, reply_markup=smr_keyboard, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=BotStates.start)
async def choice_not_from_menu(message: types.Message):
    logging.error(message.text)
    text = "Выберите, пожалуйста, из предложенных в *меню*."
    await message.answer(text, reply_markup=main_menu, parse_mode=ParseMode.MARKDOWN)
