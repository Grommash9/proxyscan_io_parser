import asyncio
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import file_path
import proxy_list
import socks5_getter

bot = Bot(token='1975741586:AAGas0xP-Iwlh3uT3TYaxRSvewL3lkjxkU0')
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, loop=loop)

button_dict = {
    'get_proxy': InlineKeyboardButton(text='5 - HTTP/HTTPS', callback_data='get_proxy'),
    'get_socks': InlineKeyboardButton(text='5 - SOCKS 4/5', callback_data='get_socks'),
    'about': InlineKeyboardButton(text='О боте', callback_data='about')
}

inline_kb_full = InlineKeyboardMarkup()
inline_kb_full.row(button_dict['get_proxy'], button_dict['get_socks'])
inline_kb_full.add(button_dict['about'])


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    file_path.work_on_new_user(message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать в бота @free_prox!', reply_markup=inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'get_proxy')
async def handle_get_proxy_command(callback_query: types.CallbackQuery):
    if proxy_list.get_proxy_q() >= 5:
        message_to_send = ''
        for proxy in proxy_list.get_proxy():
            message_to_send += f'{proxy[0]}\n'
        #Проверен {round((time.time() - proxy[1]) / 60, 2)} минут назад\n\n
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=message_to_send, reply_markup=inline_kb_full)
        file_path.parse_success()
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Сейчас в боте нет прокси, нужно немного подождать",
                               reply_markup=inline_kb_full)
        await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'about')
async def handle_about_button(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Ботом уже воспользовалось *{file_path.get_users_count()}* человек и получили *{file_path.parse_count()}* прокси.\n"
                                f"На данный момент в боте:\n"
                                f"*{proxy_list.get_proxy_q()}* свежих HTTP/HTTPS прокcи\n"
                                f"{proxy_list.get_socks_q()} свежих SOCKS 4/5\n"
                                f"Автор бота - @grommash9\n\n"
                                f"Добровольное давание денег:\n\n"
                                f"*bitcoin*: _bc1qld7c86vpcssxashzu5hfguegkegae393p4w8fj_", reply_markup=inline_kb_full, parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'get_socks')
async def handle_get_proxy_command(callback_query: types.CallbackQuery):
    if proxy_list.get_socks_q() >= 5:
        message_to_send = ''
        for proxy in proxy_list.get_socks():
            message_to_send += f'{proxy[0]}\n'
            #                   f'Проверен {round((time.time() - proxy[1]) / 60, 2)} минут назад\n\n'
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=message_to_send, reply_markup=inline_kb_full)
        file_path.parse_success()
        await bot.answer_callback_query(callback_query.id)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Сейчас в боте нет socks, нужно немного подождать",
                               reply_markup=inline_kb_full)
        await bot.answer_callback_query(callback_query.id)


@dp.message_handler()
async def any_message_answer(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Я не знаю что ответить, вот кнопочки:', reply_markup=inline_kb_full)


if __name__ == '__main__':
    #dp.loop.create_task(grabber_free_proxy.working_on_proxy())
    dp.loop.create_task(socks5_getter.start_parsing())
    executor.start_polling(dp, skip_updates=True)



