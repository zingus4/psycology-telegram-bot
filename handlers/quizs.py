import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from core import Test, Answer, Question, Result
from keyboards.menu import tests_keyboard, back, get_inline_keyboard, main_menu
from loader import bot, dp, ADMINS
from states import BotStates


tests_list = [file.split('.')[0] for file in os.listdir('data/tests')]


@dp.callback_query_handler(lambda callback_query: True, state=BotStates.current_test)
async def show_current_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer(cache_time=60)

    async with state.proxy() as data:
        test = data['test']
        test.user_score += int(callback_query.values['data'].split(':')[1])
        test.current_question += 1

        if test.count_questions > test.current_question:
            text = test.get_question_text()
            markup = get_inline_keyboard(test.questions[test.current_question].answers)

            await bot.send_message(callback_query.from_user.id, text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)

        if test.count_questions == test.current_question + 1:
            await BotStates.end_test.set()


@dp.callback_query_handler(lambda callback_query: True, state=BotStates.end_test)
async def test_result(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user = callback_query.from_user
        test = data['test']
        test.user_score += int(callback_query.values['data'].split(':')[1])

        await BotStates.start.set()

        await bot.send_message(
            user.id, test.get_result_message(), reply_markup=main_menu, parse_mode=ParseMode.MARKDOWN
        )

        await bot.send_message(
            ADMINS, test.get_message_to_admin(user), parse_mode=ParseMode.MARKDOWN,
        )


@dp.message_handler(lambda message: message.text in ["Психологические тесты"], state=BotStates.start)
async def choose_test(message: types.Message):
    await BotStates.test.set()
    await message.reply("Какой тест хотели бы пройти?", reply_markup=tests_keyboard)


def get_test_from_file(file_name):
    try:
        with open(f'data/tests/{file_name}.txt', "r", encoding="utf-8") as f:
            lines = f.readlines()
            test = Test(file_name, lines[0])
            results = lines[1].split(';')
            for j in range(0, len(results), 3):
                result = Result(results[j], results[j+1], results[j+2])
                test.results.append(result)
            count_questions = 0
            for line in lines[2:]:
                array = line.split(';')
                answers = []
                for i in range(1, len(array), 2):
                    answers.append(Answer(array[i + 1], array[i]))
                question = Question(array[0], answers)
                test.questions.append(question)
                count_questions += 1
    except FileNotFoundError:
        test = None
    return test


@dp.message_handler(lambda message: message.text in tests_list, state=BotStates.test)
async def start_test(message: types.Message, state: FSMContext):
    builder = tests_keyboard
    text = "Такой тест не найден. Выберите, пожалуйста, тест из предложенных в меню."
    test = get_test_from_file(message.text)
    if test is not None:
        await BotStates.current_test.set()
        async with state.proxy() as data:
            data['test'] = test

        await message.answer(test.get_preview_message(), reply_markup=back, parse_mode=ParseMode.MARKDOWN)
        builder = get_inline_keyboard(test.questions[0].answers)
        text = test.get_question_text()
    await message.answer(text, reply_markup=builder, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=BotStates.test)
@dp.message_handler(state=BotStates.current_test)
async def answer_is_not_from_menu(message: types.Message, state: FSMContext):
    text = "Выберите, пожалуйста, вариант из предложенных в меню."
    keyboard = back
    user_state = await state.get_state()
    if user_state == BotStates.test.state:
        text = f'Такой тест не найден. {text}'
        keyboard = tests_keyboard
    await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
