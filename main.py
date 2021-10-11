#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import telebot
from telebot import types
import parser
import config


game_list_name = '🎰 Список игр'
rating_name = '📈 Рейтинг'
feedback_name = '✍️ Предложения'


def convert_game_to_text(info, i):
    return 'Игра ' + str(i + 1) + '\n' \
           + info['name'][i] + '\n' \
           + info['date'][i] + ' ' + info['time'][i] + '\n' \
           + info['place'][i] + '\n' \
           + info['price'][i]


def menu_buttons():
    keyboard = types.InlineKeyboardMarkup()
    key_summary = types.InlineKeyboardButton(text='Все игры', callback_data='all_games')
    keyboard.add(key_summary)
    return keyboard


def game_info_buttons(data):
    keyboard = types.InlineKeyboardMarkup()
    # keys_row = []
    for i in range(len(data['date'])):
        keyboard.add(types.InlineKeyboardButton(text=str(i + 1), callback_data='game' + str(i + 1)))
    # keyboard.row(keys_row)
    return keyboard


def form_message_games(data):
    msg = ''
    for i in range(len(data['date'])):
        msg += convert_game_to_text(data, i)
        if i != len(data['date']):
            msg += '\n------------\n'
    return msg


info = parser.get_games_schedule()
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def main_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(game_list_name)
    button2 = types.KeyboardButton(rating_name)
    button3 = types.KeyboardButton(feedback_name)
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Кнопки - хуепки', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private':
        if message.text == game_list_name:
            bot.send_message(message.chat.id, form_message_games(info), reply_markup=game_info_buttons(info))
        elif message.text == rating_name:
            bot.send_message(message.chat.id, 'Скоро научусь считать рейтинг')
        elif message.text == feedback_name:
            bot.send_message(message.chat.id, 'Напиши, что бы ты хотел(а) добавить или изменить:')
        else:
            with open('history.txt', 'a') as f:
                f.write(message.from_user.username + ': ' + message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.message:
            for j in range(len(info['date'])):
                if call.data == 'game' + str(j + 1):
                    bot.send_message(
                        call.message.chat.id,
                        info['name'][j] + '\n'
                        + info['date'][j] + ' ' + info['time'][j] + '\n'
                        + info['description'][j] + '\n'
                        + info['place'][j] + '\n'
                        + info['price'][j] + '\n'
                        + 'Ссылка на регистрацию: ' + info['link'][j]
                    )
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True, interval=0)
