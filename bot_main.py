from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.utils.formatting import Bold, as_list, as_marked_section
import asyncio
import logging
from token_data import TOKEN
import sys
from recipes_handler import router

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    kb = [[types.KeyboardButton(text='Инструкция'), types.KeyboardButton(text='Описание')]]
    keyboard = types.ReplyKeyboardMarkup(
          keyboard=kb,
          resize_keyboard=True,
    )
    await message.answer(f'Привет! С чего начнём?', reply_markup=keyboard)


@dp.message(F.text.lower() == "описание")
async def description(message: types.Message):
    await message.answer("Этот бот предоставляет информацию о рецептах, ингредиентах и категориях блюд.")


@dp.message(F.text.lower() == 'инструкция')
async def commands(message: Message):
    response = as_list(Bold('Инструкция'), '/category_search_random - предоставляет определенное количество случайных рецептов какой-то категории\n', Bold('Пример использования:'), '/category_search_random 4')
    await message.answer(**response.as_kwargs())


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
