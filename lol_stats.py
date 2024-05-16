import requests, json, asyncio

api_key = 'RGAPI-a1bf9814-7e29-4ad2-b525-f36e4e5f819b'

async def get_puuid(player_name, tag, region='europe'):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player_name}/{tag}'

    result = requests.get(url + f'?api_key={api_key}')
    res_dict = json.loads(result.text)
    puuid = res_dict['puuid']
    return puuid


async def get_matches(puuid, region='europe', number=5):
    if number > 20:
        number = 20

    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}'
    params = f'/ids?start=0&count={number}&api_key={api_key}'
    result = requests.get(url + params)
    matches = json.loads(result.text)

    return matches


async def get_match(puuid, match_id, region='europe'):
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
    if result['deaths'] == 0:
        result['KDA'] = 'Perfect'
    else:
        result['KDA'] = format((result['kills'] + result['assists']) / result['deaths'], '.2f')

    if player_info['win']:
        result['game_result'] = 'Win'
    else:
        result['game_result'] = 'Lose'

    for id in queue_ids:
        if id['queueId'] == data['info']['queueId']:
            result['gamemode'] = id['description']

    return result

def get_queue_ids():
    url = 'https://static.developer.riotgames.com/docs/lol/queues.json'
    result = requests.get(url)
    ids = json.loads(result.text)
    return ids

def make_readable(history):
    result = ''
    for match in history:
        result += f"- **{match['game_result']}** | {match['gamemode']} | {match['role']} {match['champion']} lvl: {match['lvl']} || {match['kills']}/{match['deaths']}/{match['assists']} **KDA : {match['KDA']}**\n"
    return result


async def match_history(player_name, player_tag='EUW', matches_number=5, *args):
    id = await get_puuid(player_name, player_tag)
    matches = await get_matches(id, number=int(matches_number))
    history = [await get_match(id, match) for match in matches]
    stats = make_readable(history)

    return stats

queue_ids = get_queue_ids()
