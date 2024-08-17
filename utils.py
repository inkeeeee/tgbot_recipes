from googletrans import Translator
from aiogram.utils.formatting import (
	Bold, as_list, as_marked_section
)
translator = Translator()


def translate(text):
	return translator.translate(text, dest='ru').text


def formatting(recipe):
	name = translate(recipe['strMeal'])
	instruction = translate(recipe['strInstructions'])
	positions = []
	for i in range(1, 21):
		ingredient = 'strIngredient' + str(i)
		measure = 'strMeasure' + str(i)
		if recipe[ingredient]:
			position = f'{recipe[ingredient]}: {recipe[measure]}'
			positions.append(translate(position))
		else:
			break

	text = as_list(Bold(name), Bold('Рецепт:'), instruction, as_marked_section(Bold('Ингридиенты:'), *positions),)
	return text

async def get_categories(session):
	async with session.get(url='https://www.themealdb.com/api/json/v1/1/list.php?c=list') as resp:
		return await resp.json()


async def get_meals(session, category):
	async with session.get(url=f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}') as resp:
		return await resp.json()


async def get_recipes(session, ID):
	async with session.get(url=f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={ID}') as resp:
		return (await resp.json())['meals'][0]
		name = translate(recipe['strMeal'])
		instruction = translate(recipe['strInstructions'])
		positions = []
		for i in range(1, 21):
			ingredient = 'strIngredient' + str(i)
			measure = 'strMeasure' + str(i)
			if recipe[ingredient]:
				position = f'{recipe[ingredient]}: {recipe[measure]}'
				positions.append(translate(position))
			else:
				break

		return name, instruction, positions
