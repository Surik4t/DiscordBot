import requests, json, asyncio, os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('LoL_API_KEY')

async def current_rank(player_name, player_tag='EUW', server='euw1'):
    status, puuid_answer = await get_puuid(player_name, player_tag)
    if status != 200:
        return puuid_answer
    summoner_info = await get_summoner_info(puuid_answer, server)
    if 'status' in summoner_info:
        print(type(summoner_info['status']))
        return summoner_info['status']['message']

    league_entries = await get_league_entries(summoner_info['id'], server)
    if len(league_entries) == 0:
        return 'Нет информации'

    result = parse_league_entries(league_entries)
    return result


def parse_league_entries(entries):
    result = ''
    for entry in entries:
        result += (f"- {entry['queueType']} | **{entry['tier']} {entry['rank']} {entry['leaguePoints']} LP** | "
                   f"*wins: {entry['wins']} losses: {entry['losses']}* \n")
    return result


async def get_league_entries(id, server):
    url = f'https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/'
    params = f'{id}?api_key={api_key}'
    result = requests.get(url + params)
    entries = json.loads(result.text)
    return entries


async def get_summoner_info(puuid, server='euw1'):
    url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/'
    params = f'{puuid}?api_key={api_key}'
    result = requests.get(url + params)
    summoner_info = json.loads(result.text)
    return summoner_info


async def get_puuid(player_name, tag, region='europe'):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player_name}/{tag}'

    result = requests.get(url + f'?api_key={api_key}')
    res_dict = json.loads(result.text)
    if result.status_code != 200:
        return result.status_code, res_dict['status']['message']

    puuid = res_dict['puuid']
    return result.status_code, puuid


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
        result += (f"- **{match['game_result']}** | {match['gamemode']} | {match['role']} {match['champion']} lvl: {match['lvl']} || "
                   f"{match['kills']}/{match['deaths']}/{match['assists']} **KDA : {match['KDA']}**\n")
    return result


async def match_history(player_name, player_tag='EUW', matches_number=5, *args):
    status_code, puuid_answer = await get_puuid(player_name, player_tag)
    if status_code != 200:
        return puuid_answer
    matches = await get_matches(puuid_answer, number=int(matches_number))
    history = [await get_match(puuid_answer, match) for match in matches]
    stats = make_readable(history)

    return stats

queue_ids = get_queue_ids()
