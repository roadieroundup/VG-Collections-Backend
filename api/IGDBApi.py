from datetime import datetime
import os

import requests

#! ENV VARIABLES

AUTHORIZATION = os.environ["AUTHORIZATION"]
CLIENT_ID = os.environ["CLIENT_ID"]

HEADERS = {"Client-ID": CLIENT_ID,
           "Authorization": AUTHORIZATION}

GAMES_URL = "https://api.igdb.com/v4/games/"

IMG_URL = "https://images.igdb.com/igdb/image/upload/t_720p/"
SCREEN_URL = "https://images.igdb.com/igdb/image/upload/t_screenshot_big/"


def get_recent_games_ids():
    today = datetime.now()

    today = int(today.timestamp())

    data = f'sort first_release_date desc;where aggregated_rating_count != 0 & first_release_date != null & first_release_date < {today} & cover != null & screenshots != null;limit 15;'

    ids = requests.post(GAMES_URL, headers=HEADERS, data=data).json()

    ids_tuple = tuple([value for dic in ids for value in dic.values()])

    return ids_tuple


def recent_games():

    ids = get_recent_games_ids()

    data = f'fields id,name,summary,cover.*,screenshots.*,first_release_date; where id = {ids}; limit 6;'

    games_request = requests.post(GAMES_URL, headers=HEADERS, data=data).json()

    games = []

    for game in games_request:
        game_obj = {
            "id": game['id'],
            "name": game['name'],
            "cover": IMG_URL + game['cover']['image_id'] + '.png',
            "bgImage": SCREEN_URL + game['screenshots'][0]['image_id'] + '.png',
        }
        games.append(game_obj)

    return games


def search_games(game_title):

    data = f'search "{game_title}";fields id,name,cover.*,release_dates.*;where release_dates.human != null & release_dates.date != null & cover != null; limit 40;'

    games_request = requests.post(GAMES_URL, headers=HEADERS, data=data).json()

    games = []

    #! CHANGE IMAGE SIZE
    for game in games_request:
        game_obj = {
            "id": game['id'],
            "title": game['name'],
            "image_url": IMG_URL + game['cover']['image_id'] + '.webp',
            "date": game['release_dates'][0]['human'],
            # "bgImage": SCREEN_URL + game['screenshots'][0]['image_id'] + '.png',
        }
        games.append(game_obj)

    return games


def update_list(list):

    for game in list:

        data = f'fields summary, release_dates.*; where id = {game["id"]};'

        games_request = requests.post(
            GAMES_URL, headers=HEADERS, data=data).json()[0]

        description = games_request["summary"].split('.')[0]

        if len(description) > 200:
            description = description[:200] + '...'

        try:
            lowest_timestamp = min(
                games_request["release_dates"], key=lambda x: x['date'])['date']


            year = datetime.fromtimestamp(lowest_timestamp).year
        except:
            year = 0

        game.update({"description": description, "year": year})
        game.pop('id')
        game.pop('date')


def update_game(game_id):

    data = f'fields summary, release_dates.*; where id = {game_id};'

    games_request = requests.post(
        GAMES_URL, headers=HEADERS, data=data).json()[0]

    description = games_request["summary"].split('.')[0]

    if len(description) > 200:
        description = description[:200] + '...'

    try:

        lowest_timestamp = min(
            games_request["release_dates"], key=lambda x: x['date'])['date']


        year = datetime.fromtimestamp(lowest_timestamp).year

    except:
        year = 0

    game = {"description": description, "year": year}

    return game
