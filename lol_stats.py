import requests, json, asyncio

api_key = 'RGAPI-a1bf9814-7e29-4ad2-b525-f36e4e5f819b'

def get_puuid(player_name, tag='EUW', region='europe'):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player_name}/{tag}'

    result = requests.get(url + f'?api_key={api_key}')
    res_dict = json.loads(result.text)
    puuid = res_dict['puuid']
    return puuid


def get_matches(puuid, region='europe', number=5):
    if number > 20:
        number = 20

    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}'
    params = f'/ids?start=0&count={number}&api_key={api_key}'
    result = requests.get(url + params)
    matches = json.loads(result.text)

    return matches


def get_match(puuid, match_id, region='europe'):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'
    result = requests.get(url)
    data = json.loads(result.text)

    return parse_data(data, puuid)


def parse_data(data, puuid):
    player_index = data['metadata']['participants'].index(puuid)
    player_info = data['info']['participants'][player_index]

    result = {
        #'name': player_info['summonerName'],
        'role': player_info['teamPosition'],
        'champion': player_info['championName'],
        'lvl': player_info['champLevel'],
        'kills': player_info['kills'],
        'deaths': player_info['deaths'],
        'assists': player_info['assists']
    }
    result['KDA'] = format((result['kills'] + result['assists']) / result['deaths'], '.2f')

    if player_info['win']:
        result['win'] = 'Win'
    else:
        result['win'] = 'Lose'

    for id in queue_ids:
        if id['queueId'] == data['info']['queueId']:
            result['gamemode'] = id['description']

    return result

def get_queue_ids():
    url = 'https://static.developer.riotgames.com/docs/lol/queues.json'
    result = requests.get(url)
    ids = json.loads(result.text)
    return ids


def match_stats(player_name, player_tag, matches_number=10):
    id = get_puuid(player_name, player_tag)
    matches = get_matches(id, number=matches_number)
    player_stats = [get_match(id, match) for match in matches]

    return player_stats


queue_ids = get_queue_ids()

stats = match_stats('artishpalk', 'EUW')

for stat in stats:
    print(stat)