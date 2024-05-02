import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

API_TOKEN = '6381194434:AAHrvLJ7jlZH3eUgfL76PmtWS7NGKEaA7Aw'


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    username = State()
    surname = State()
    tel = State()
    group = State()
    time = State()


@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    await Form.username.set()
    await message.answer('Xush kelibsiz\nusername ni kiriting !')


@dp.message_handler(state=Form.username)
async def get_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await Form.next()
    await message.answer('Familiya Kiriting')


@dp.message_handler(state=Form.surname)
async def get_username(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await Form.next()
    await message.answer('Telephone number Kiriting')


@dp.message_handler(lambda msg: not msg.text.isdigit() or not len(msg.text) == 9, state=Form.tel)
async def get_email(message: Message):
    await message.answer('Telephone number togri kiriting')


# def check_email(message: Message):
#     if message.text.endswith(''):
#         return True
#     return False


@dp.message_handler(lambda msg: msg.text.isdigit() and len(msg.text) == 9, state=Form.tel)
async def get_tel(message: Message, state: FSMContext):
    await state.update_data(tel=message.text)
    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Beginner", "Intermediate")
    markup.add("Advanced")

    await message.answer('Qaysi Groupga Kirishni Xohlaysiz',reply_markup=markup)


@dp.message_handler(lambda msg: msg.text in ['Beginner','Intermediate','Advanced'],state=Form.group)
async def get_tel(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("9:00", "14:00")
    markup.add("18:00")

    await message.answer("Qaysi Vaqtda Bo'lishni Xohlaysiz",reply_markup=markup)

@dp.message_handler(lambda msg: msg.text in ["9:00","14:00","18:00"],state=Form.time)
async def get_tel(message: Message, state: FSMContext):
    # await state.update_data(group=message.text)

    markup = types.ReplyKeyboardRemove()

    async with state.proxy() as data:
        data['time'] = message.text

        username = data['username']
        surname = data['surname']
        tel = data['tel']
        group = data['group']
        time = data['time']
        text = f'Sizning malumotlaringiz\n' \
               f'username - {username}\n' \
               f'surname - {surname}\n' \
               f'tel - {tel}\n' \
               f'group  - {group}\n' \
               f'time - {time}\n'
        await message.answer(text,reply_markup=markup)

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
