from bs4 import BeautifulSoup
import urllib.request as ur
import ssl
import re


def get_page(url):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    page = ur.urlopen(url, context=ssl_context).read()
    return BeautifulSoup(page, 'html.parser')


def get_game_time(soup):
    info = soup.findAll('div', {'class': 'schedule-info'})
    time = BeautifulSoup(str(info[2]), 'html.parser').find('div', {'class': 'techtext'}).string.split(' ')[1]
    return time


def get_game_link(soup):
    tmp = soup.find('div', {'class': 'schedule-block-top'}).find('a').get('href')
    return 'https://kzn.quizplease.ru' + tmp


def get_info(gi):
    games = get_page('https://kzn.quizplease.ru/schedule').find_all('div', {'class': 'schedule-column'})
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


local_rating_url = 'https://kzn.quizplease.ru/rating?QpRaitingSearch%5Btext%5D=%D0%BC%D0%BE%D0%B6%D0%BD%D0%BE+%D0%BF%D0%BE%D1%82%D0%B8%D1%88%D0%B5&QpRaitingSearch%5Bgeneral%5D=0&QpRaitingSearch%5Bleague%5D=1'
global_rating_url = 'https://kzn.quizplease.ru/rating?QpRaitingSearch%5Btext%5D=%D0%BC%D0%BE%D0%B6%D0%BD%D0%BE+%D0%BF%D0%BE%D1%82%D0%B8%D1%88%D0%B5&QpRaitingSearch%5Bgeneral%5D=1&QpRaitingSearch%5Bleague%5D=1'


def get_rating_by_url(url):
    rating = {'place': 0, 'games': 0, 'points': 0}
    row = get_page(url).find('div', {'class': 'rating-table-row flex-row flex-align-items-center'})
    soup = BeautifulSoup(str(row), 'html.parser')
    rating['place'] = int(soup.find('strong').string)
    rating['points'] = float(re.search(r'\d{2,}.\d',
                                       str(soup.find('div', {'class': 'rating-table-row-td3 rating-table-points'})))
                             .group(0))
    rating['games'] = int(re.search(r' \d+',
                                    str(soup.find('div', {'class': 'rating-table-kol-game'}))).group(0).strip(' '))
    return rating


def get_rating():
    return [get_rating_by_url(global_rating_url)]
