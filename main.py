#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request as ur
import ssl
import telebot


# рейтинг:
#   https://kzn.quizplease.ru/rating?QpRaitingSearch%5Btext%5D=%D0%BC%D0%BE%D0%B6%D0%BD%D0%BE+%D0%BF%D0%BE%D1%82%D0%B8%D1%88%D0%B5&QpRaitingSearch%5Bgeneral%5D=0&QpRaitingSearch%5Bleague%5D=1
#       за сезон
#   https://kzn.quizplease.ru/rating?QpRaitingSearch%5Btext%5D=%D0%BC%D0%BE%D0%B6%D0%BD%D0%BE+%D0%BF%D0%BE%D1%82%D0%B8%D1%88%D0%B5&QpRaitingSearch%5Bgeneral%5D=1&QpRaitingSearch%5Bleague%5D=1
#       за все время

def get_page():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    page = ur.urlopen('https://kzn.quizplease.ru/schedule', context=ssl_context).read()
    return BeautifulSoup(page, 'html.parser')


def get_game_time(soup):
    info = soup.findAll('div', {'class': 'schedule-info'})
    return BeautifulSoup(str(info[1]), 'html.parser').find('div', {'class': 'techtext'}).string.split(' ')[1]


def get_game_link(soup):
    tmp = soup.find('div', {'class': 'schedule-block-top'}).find('a').get('href')
    return 'https://kzn.quizplease.ru' + tmp


def get_info(gi):
    games = get_page().find_all('div', {'class': 'schedule-column'})
    for game in games:
        soup = BeautifulSoup(str(game), 'html.parser')
        gi['date'].append(soup.find('div', {'class': 'h3 h3-green h3-mb10'}).string)
        gi['place'].append(soup.find('div', {'class': 'schedule-block-info-bar'}).string.replace('\t', ''))
        gi['name'].append(soup.find('div', {'class': 'h2 h2-game-card h2-left'}).string)
        gi['price'].append(soup.find('div', {'class': 'text'}).string)
        gi['time'].append(get_game_time(soup))
        gi['description'].append(soup.find('div', {'class': 'techtext techtext-mb30'}).string)
        gi['link'].append(get_game_link(soup))
    return gi


def print_gi(gi):
    for i in range(len(gi['date'])):
        print('---------------------')
        print(gi['date'][i])
        print(gi['name'][i])
        print(gi['place'][i])
        print(gi['time'][i])
        print(gi['price'][i])
        print(gi['description'][i])
        print(gi['link'][i])
        print('---------------------')


def get_games_schedule():
    games_info = {'date': [], 'place': [], 'name': [], 'description': [], 'time': [], 'price': [], 'link': []}
    games_info = get_info(games_info)
    # print_gi(games_info)
    return games_info


def convert_game_to_text(info, i):
    return 'Игра ' + str(i + 1) + '\n' \
           + info['name'][i] + '\n' \
           + info['date'][i] + ' ' + info['time'][i] + '\n' \
           + info['place'][i] + '\n' \
           + info['price'][i]


def menu_buttons():
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_summary = telebot.types.InlineKeyboardButton(text='Все игры', callback_data='all_games')
    keyboard.add(key_summary)
    return keyboard


def game_info_buttons(data):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # keys_row = []
    for i in range(len(data['date'])):
        keyboard.add(telebot.types.InlineKeyboardButton(text=str(i + 1), callback_data='game'+str(i + 1)))
    # keyboard.row(keys_row)
    return keyboard


def start_bot(info):
    token = '2002394082:AAG-jp-egUtYG-DaP62oYwbM1AYxdN2sxqQ'
    bot = telebot.TeleBot(token)
    msg = ''
    for i in range(len(info['date'])):
        msg += convert_game_to_text(info, i)
        if i != len(info['date']):
            msg += '\n------------\n'

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        bot.send_message(message.from_user.id, "Лови игры:", reply_markup=menu_buttons())

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "all_games":
                bot.send_message(call.message.chat.id, msg, reply_markup=game_info_buttons(info))
            else:
                for j in range(len(info['date'])):
                    if call.data == 'game'+str(j + 1):
                        bot.send_message(
                            message.from_user.id,
                            info['name'][i] + '\n'
                            + info['date'][i] + ' ' + info['time'][i] + '\n'
                            + info['description'][i] + '\n'
                            + info['place'][i] + '\n'
                            + info['price'][i] + '\n'
                            + 'Ссылка на регистрацию: ' + info['link'][i]
                        )

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    start_bot(get_games_schedule())
