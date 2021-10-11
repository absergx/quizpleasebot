#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import parser
import config


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
        keyboard.add(types.InlineKeyboardButton(text=str(i + 1), callback_data='game'+str(i + 1)))
    # keyboard.row(keys_row)
    return keyboard


def form_message_games(data):
    msg = ''
    for i in range(len(data['date'])):
        msg += convert_game_to_text(data, i)
        if i != len(data['date']):
            msg += '\n------------\n'
    return msg


def start_bot():
    info = parser.get_games_schedule()
    bot = telebot.TeleBot(config.TOKEN)

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button1 = types.KeyboardButton('ð Список игр')
    # button2 = types.KeyboardButton('ð Рейтинг')
    # markup.add(button1, button2)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        bot.send_message(message.from_user.id, "Лови игры:", reply_markup=menu_buttons())

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "all_games":
                bot.send_message(call.message.chat.id, form_message_games(info), reply_markup=game_info_buttons(info))
            else:
                for j in range(len(info['date'])):
                    if call.data == 'game'+str(j + 1):
                        bot.send_message(
                            message.from_user.id,
                            info['name'][j] + '\n'
                            + info['date'][j] + ' ' + info['time'][j] + '\n'
                            + info['description'][j] + '\n'
                            + info['place'][j] + '\n'
                            + info['price'][j] + '\n'
                            + 'Ссылка на регистрацию: ' + info['link'][j]
                        )

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    start_bot()
