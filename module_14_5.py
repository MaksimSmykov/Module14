from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
btn_calculate = KeyboardButton(text='Рассчитать')
btn_info = KeyboardButton(text='Информация')
btn_buy = KeyboardButton(text='Купить')
btn_registration = KeyboardButton(text='Регистрация')
start_menu.add(btn_calculate)
start_menu.add(btn_info)
start_menu.add(btn_buy)
start_menu.add(btn_registration)

inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inline_kb.add(button)
inline_kb.add(button1)

products_kb = InlineKeyboardMarkup(resize_keyboard=True)
product1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
product2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
product3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
product4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
products_kb.add(product1)
products_kb.add(product2)
products_kb.add(product3)
products_kb.add(product4)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=start_menu)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Информация о боте!')

@dp.message_handler(text='Рассчитать')
async def calculate(message):
    await message.answer(text='Выберите опцию:', reply_markup=inline_kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    get_all_products()
    products = cursor.fetchall()
    print(type(products))
    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        with open(f'{product[0]}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer(text='Выберите продукт для покупки:', reply_markup=products_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    norma = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()

@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer(f"Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer(f"Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer(f"Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer(f"Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=int(message.text))
    await RegistrationState.age.set()
    data = await state.get_data()
    print(data)
    add_user(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer(f"Регистрация прошла успешно")

@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    get_all_products()
