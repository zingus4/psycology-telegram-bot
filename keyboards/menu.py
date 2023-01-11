from aiogram import types

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
main_menu.add("Подсказки по СМЭР", "Психологические тесты")

tests_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
tests_keyboard.add("Шкала депрессии Бека", "Опросник по депрессии PHQ-9")
tests_keyboard.add("Паническое расстройство", "Генерализованная тревога")
tests_keyboard.add("Назад")

smr_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
smr_keyboard.add("План СМЭР", "Автоматические мысли")
smr_keyboard.add("Базовые потребности", "Схема-режимы", "Ошибки мышления")
smr_keyboard.add("Назад")

back = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
back.add("Назад")


def get_inline_keyboard(buttons):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
    for button in buttons:
        keyboard.add(
            types.InlineKeyboardButton(
                text=button.answer, callback_data=f'score:{button.point}'
            )
        )
    return keyboard
