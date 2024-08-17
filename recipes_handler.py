import asyncio
import aiohttp

from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.formatting import (
	Bold, as_list, as_marked_section
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from aiogram.types import Message
import random
from utils import translate, get_categories, get_meals, get_recipes, formatting


class OrderRecipes(StatesGroup):
	waiting_for_meals = State()
	waiting_for_recipes = State()


router = Router()


@router.message(Command('category_search_random'))
async def category_search_random(message: Message, command: CommandObject, state: FSMContext):
	if command.args is None:
		await message.answer('Не введено количество рецептов')
		return
	try:
		number = int(command.args)
	except ValueError:
		await message.answer('Введенное значение не является числом')
		return

	await state.set_data({'number': number})

	async with aiohttp.ClientSession() as session:
		categories = (await get_categories(session))['meals']

	builder = ReplyKeyboardBuilder()

	for category in categories:
		builder.add(types.KeyboardButton(text=category['strCategory']))

	builder.adjust(3)
	await message.answer('Выберете категорию:', reply_markup=builder.as_markup(keyboard_resize=True))

	await state.set_state(OrderRecipes.waiting_for_meals.state)


@router.message(OrderRecipes.waiting_for_meals)
async def get_list_of_categories(message: Message, state: FSMContext):
	number = (await state.get_data())['number']
	category = message.text.strip()

	async with aiohttp.ClientSession() as session:
		meals = (await get_meals(session, category))['meals']

	meals_for_user = random.sample(meals, k=number)

	ids = [meal['idMeal'] for meal in meals_for_user]
	meal_names = [translate(meal['strMeal']) for meal in meals_for_user]

	await state.set_data({'ids_list': ids})

	response = as_list(as_marked_section(Bold('Я могу вам предложить:'), *meal_names))
	button = ReplyKeyboardBuilder()
	button.add(types.KeyboardButton(text='Покажи рецепты'))

	await message.answer(**response.as_kwargs(), reply_markup=button.as_markup())

	await state.set_state(OrderRecipes.waiting_for_recipes.state)


@router.message(OrderRecipes.waiting_for_recipes)
async def get_list_of_recipes(message: Message, state: FSMContext):
	ids = (await state.get_data())['ids_list']
	async with aiohttp.ClientSession() as session:
		request = [get_recipes(session, ID) for ID in ids]
		all_recipes = await asyncio.gather(*request)

		for recipe in all_recipes:
			text = formatting(recipe)
			await message.reply(**text.as_kwargs())
