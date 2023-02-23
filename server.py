import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, executor, types

import exceptions, expenses
from categories import Categories
from middlewares import AccessMiddleware


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PROXY_URL = os.getenv("TELEGRAM_PROXY_URL")
PROXY_AUTH = aiohttp.BasicAuth(
    login=os.getenv("TELEGRAM_PROXY_LOGIN"),
    password=os.getenv("TELEGRAM_PROXY_PASSWORD")
)
TG_ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(TG_ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def show_welcome_screen(message: types.Message):
    await message.answer(
        "Expense tracker bot\n\n"
        "Add expense: 20 taxi\n"
        "Today spending stats: /today\n"
        "Current month spent: /month\n"
        "Previous expenses: /expenses\n"
        "Expense categories: /categories")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def delete_expense_record(message: types.Message):
    '''Deletes one expense record by its ID'''
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Deleted"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def show_categories(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Expense categories:\n\n* " +\
        ("\n* ".join([category.name+' ('+", ".join(category.aliases)+')' for category in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def show_today_expenses(message: types.Message):
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def show_month_expenses(message: types.Message):
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def show_last_expenses(message: types.Message):
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("No expense recorded")
        return

    last_expenses_rows = [
        f"{expense.amount} EUR. {expense.category_name} — tap "
        f"/del{expense.id} to delete"
        for expense in last_expenses]
    answer_message = "Last expense records:\n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as error:
        await message.answer(str(error))
        return
    answer_message = (
        f"Expense record added for {expense.amount} EUR: {expense.category_name}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
