import sqlite3
from datetime import date
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import tg_token, uprav_id, all_date,\
                   all_date_up, current_date
from parse_xlsx import get_request_to_sheet

bot = Bot(tg_token)
dp = Dispatcher(bot)

telegram_date = [all_date[current_date]]

all_task = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/menu'), KeyboardButton('/help'))

back_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/назад'))

menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/отчетность'), KeyboardButton('/админы'),
                                                             KeyboardButton('/pslogs'))

otchet_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/расходы'), KeyboardButton('/выручка'),
                                                              KeyboardButton('/назад'))


@dp.message_handler(commands=['start'])
async def questions(message: types.Message):
    if message.from_user.id in uprav_id and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, '👀 Для начала работы нажмите: menu\n'
                                                     '🤷‍♂️ Чтобы получить информацию по командама: help\n'
                                                     '👥 проект находится на стадии разработки в случае проблем'
                                                     ' писать @ilpdakz',
                               reply_markup=all_task)
    else:
        await bot.send_message(message.from_user.id, '⛔ Доступ разрешен только управляющему')
        print(message.from_user.id)


@dp.message_handler(commands=['menu', 'меню', 'назад'])
async def questions(message: types.Message):
    if message.from_user.id in uprav_id and message.chat.type == 'private':
        sum_expenses_to_menu = 0
        data = get_request_to_sheet(telegram_date[len(telegram_date) - 1])['values']
        for i in range(1, len(data)):
            sum_expenses_to_menu += int(data[i][0])
        await bot.send_message(message.from_user.id, 'Добро пожаловать в Colizeum manager\n'
                                                     f'📅 Текущий месяц проверки - '
                                                     f'{telegram_date[len(telegram_date) - 1]} \n'
                                                     f'📝 Сумма расходов за {telegram_date[len(telegram_date) - 1]}:'
                                                     f' {sum_expenses_to_menu} \n'
                                                     f'📊 Выручка на данный момент  \n'
                                                     '👥 на смене: \n'
                                                     '----------Структура бота------------\n',
                               reply_markup=menu_buttons)
        photo = open('images/projectstruct.png', 'rb')
        await bot.send_photo(message.from_user.id, photo)

    else:
        await bot.send_message(message.from_user.id, '⛔ Доступ разрешен только управляющему')
        print(message.from_user.id)


@dp.message_handler(commands='help')
async def questions(message: types.Message):
    if message.from_user.id in uprav_id and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, f'Текущий месяц проверки - {telegram_date[len(telegram_date) - 1]}\n'
                                                     f'Для того чтобы поменять месяц напишите:\n'
                                                     f'/cmo месяц\n', reply_markup=back_button)
    else:
        await bot.send_message(message.from_user.id, '⛔ Доступ разрешен только управляющему')
        print(message.from_user.id)


@dp.message_handler(commands=['cmo', 'смо'])
async def questions(message: types.Message):
    if message.from_user.id in uprav_id and message.chat.type == 'private':
        if message.text.lower().split()[1] in list(all_date_up.keys()):
            telegram_date.append(message.text.lower().split()[1])
            await bot.send_message(message.from_user.id, 'Месяц проверки успешно изменился на '
                                                         f'{message.text.lower().split()[1]}')
        else:
            await bot.send_message(message.from_user.id, '⛔ Ошибка в написании месяца\n'
                                                         f'Пример: /cmo Март {message.text.lower().split()[1]}')
    else:
        await bot.send_message(message.from_user.id, '⛔ Доступ разрешен только управляющему')
        print(message.from_user.id)


@dp.message_handler(commands=['отчетность'])
async def questions(message: types.Message):
    if message.from_user.id in uprav_id and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, '📊Вы находитесь в меню отчетности:\n'
                                                     f' Текущий месяц проверки - {telegram_date[len(telegram_date) - 1]}\n'
                                                     '🧾Здесь вы можете посмотреть расходы и'
                                                     ' выручку клуба, также есть возможность'
                                                     ' добавить или удалить расход', reply_markup=otchet_button)
    else:
        await bot.send_message(message.from_user.id, '⛔ Доступ разрешен только управляющему')
        print(message.from_user.id)


@dp.message_handler(commands='Расходы')
async def questions(message: types.Message):
    if message.from_user.id in uprav_id and message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'ждите...')
        try:
            data = get_request_to_sheet(telegram_date[len(telegram_date) - 1])['values']
            bot_response = f'-------------------------------------------\n' \
                           f'Расходы за {telegram_date[len(telegram_date) - 1]}\n' \
                           f'-------------------------------------------\n'
            bot_response += 'Сумма расхода | Причина расхода - дата  \n'
            sum_expenses = 0
            for i in range(1, len(data)):
                if not data[i]:
                    continue
                else:
                    prints_money = ' ' * (25 - len(data[i][0]))
                    if data[i][1] == '':
                        what_is_it = 'Причины нет'
                    else:
                        what_is_it = data[i][1]
                    try:
                        sum_expenses += int(data[i][0])
                    except ValueError:
                        sum_expenses += 0
                    bot_response += '-------------------------------------------\n'
                    bot_response += f'{data[i][0]}{prints_money}| {what_is_it} - {data[i][2][0:5]}\n'
            bot_response += '-------------------Итог-------------------\n'
            bot_response += f'Сумма всех расходов равна = {sum_expenses}'
            await bot.send_message(message.from_user.id, bot_response, reply_markup=back_button)
            sum_expenses = 0
        except:
            await bot.send_message(message.from_user.id, '⛔ Расходов на данный месяц нет')
    else:
        await bot.send_message(message.from_user.id, '⛔ Доступ разрешен только управляющему')
        print(message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp)