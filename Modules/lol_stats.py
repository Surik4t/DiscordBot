import os, requests, json
from dotenv import load_dotenv, find_dotenv

load_dotenv()

LOL_API_KEY = os.getenv("LOL_API_KEY")


def get_account_by_riot_id(name, tag="euw", region="europe"):
    URL = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    response = requests.get(URL, headers={"X-Riot-Token": LOL_API_KEY})
    if response.status_code != 200:
        error = response.json()["status"]
        raise Exception(f"{error["status_code"]}: {error["message"]}")
    return json.loads(response.text)


def get_match_ids_by_puuid(puuid, region="europe", count=1):
    URL = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={count}"
    response = requests.get(URL, headers={"X-Riot-Token": LOL_API_KEY})
    if response.status_code != 200:
        error = response.json()["status"]
        raise Exception(f"{error["status_code"]}: {error["message"]}")
    return json.loads(response.text)


def get_match_by_match_id(match_id, region="europe"):
    URL = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(URL, headers={"X-Riot-Token": LOL_API_KEY})
    if response.status_code != 200:
        error = response.json()["status"]
        raise Exception(f"{error["status_code"]}: {error["message"]}")
    return json.loads(response.text)


def save_match_stats(match_ids: list):
    for match_id in match_ids:
        if os.path.exists(f"match_stats/{match_id}.json"):
            continue
        with open(f"match_stats/{match_id}.json", "w+", encoding="utf-8") as file:
            match_stats = get_match_by_match_id(match_id)
            json.dump(match_stats, file, indent=4)


def load_match_stats(match_id):
    try:
        with open(f"match_stats/{match_id}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"match {match_id} not found")


def create_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except FileExistsError as e:
        pass


def get_table_with_stats(stats):
    names, champ_names, positions, KDAs = [], [], [], []
    players = []

    blue_result = "WON" if stats["info"]["teams"][0]["win"] else "LOST"
    red_result = "WON" if stats["info"]["teams"][1]["win"] else "LOST"

    all_players_stats = stats["info"]["participants"]

    for player in all_players_stats:
        name = f"{player["riotIdGameName"]}#{player["riotIdTagline"]}"
        names.append(name)
        champ_names.append(player["championName"])
        positions.append(
            player["individualPosition"].title()
            if player["individualPosition"] != "UTILITY"
            else "Support"
        )
        KDAs.append(f"{player["kills"]} / {player["deaths"]} / {player["assists"]}")

        total_pings = (
            player["allInPings"]
            + player["assistMePings"]
            + player["basicPings"]
            + player["commandPings"]
            + player["dangerPings"]
            + player["enemyMissingPings"]
            + player["enemyVisionPings"]
            + player["getBackPings"]
            + player["holdPings"]
            + player["needVisionPings"]
            + player["onMyWayPings"]
            + player["pushPings"]
            + player["retreatPings"]
            + player["visionClearedPings"]
        )
        players.append(
            {
                "ability_uses": player["challenges"]["abilityUses"],
                "damage_taken_percent": player["challenges"][
                    "damageTakenOnTeamPercentage"
                ],
                "damage_taken": player["totalDamageTaken"],
                "damage_to_buildings": player["damageDealtToBuildings"],
                "damage_to_champions": player["totalDamageDealtToChampions"],
                "gold_earned": player["goldEarned"],
                "largest_crit": player["largestCriticalStrike"],
                "bounty_gold": player["challenges"]["bountyGold"],
                "name": name,
                "skillshots_dodged": player["challenges"]["skillshotsDodged"],
                "time_spent_dead": player["totalTimeSpentDead"],
                "total_pings": total_pings,
            }
        )

    longest_position = len(max(positions, key=len))
    longest_name = len(max(names, key=len))
    longest_champ_name = len(max(champ_names, key=len))

    table = ""
    counter = 0
    for name, champ_name, position, kda in zip(names, champ_names, positions, KDAs):
        if counter == 0:
            table += f"Blue team - {blue_result}\n"
        if counter == 5:
            table += f"Red team - {red_result}\n"
        counter += 1
        table += f"{position.ljust(longest_position)} | {champ_name:{longest_champ_name}} | {name:{longest_name}} | {kda:>}\n"

    return (table, players)


def get_achivements(players):
    best_dd = sorted(players, key=lambda x: x["damage_to_champions"])[-1]
    best_pusher = sorted(players, key=lambda x: x["damage_to_buildings"])[-1]
    best_tank = sorted(players, key=lambda x: x["damage_taken"])[-1]
    biggest_shark = sorted(players, key=lambda x: x["gold_earned"])[-1]
    most_annoying = sorted(players, key=lambda x: x["total_pings"])[-1]
    one_punch_man = sorted(players, key=lambda x: x["largest_crit"])[-1]
    resident_sleeper = sorted(players, key=lambda x: x["time_spent_dead"])[-1]
    scripter = sorted(players, key=lambda x: x["skillshots_dodged"])[-1]

    achivements = {
        "Best Damage Dealer": f"{best_dd["name"]:25}| damage to enemy champions: {best_dd["damage_to_champions"]}",
        "Best Tank": f"{best_tank["name"]:25}| damage taken: {best_tank["damage_taken"]} (team percentage: {round(best_tank["damage_taken_percent"]*100, 2)}%)",
        "Best Pusher": f"{best_pusher["name"]:25}| damage delt to structures: {best_pusher["damage_to_buildings"]}",
        "Biggest Shark": f"{biggest_shark["name"]:25}| total gold earned: {biggest_shark["gold_earned"]}",
        "One Punch Man": f"{one_punch_man["name"]:25}| largest crit: {one_punch_man["largest_crit"]}",
        "Scripter": f"{scripter["name"]:25}| skillshots dodged: {scripter["skillshots_dodged"]}",
        "Resident Sleeper": f"{resident_sleeper["name"]:25}| time spent dead: {resident_sleeper["time_spent_dead"]} seconds",
        "Most Annoying": f"{most_annoying["name"]:25}| total pings: {most_annoying["total_pings"]}",
    }

    return achivements


def parse_message(message):
    if " " in message:
        split_message = message.split()
        name, tag = split_message[0].split("#")
        region = split_message[1]
        return (name, tag, region)
    elif "#" in message:
        name, tag = message.split("#")
        return (name, tag)
    else:
        return (message,)


async def get_game_stats(message): 
    try:
        args = parse_message(message)
        account = get_account_by_riot_id(*args)
        match_ids = get_match_ids_by_puuid(account["puuid"], count=1)
    except Exception as e:
        return e

    create_dir("match_stats")
    save_match_stats(match_ids)

    stats = load_match_stats(match_ids[0])
    result, players_stats = get_table_with_stats(stats)

    result += "\n"
    for achivement, achiver in get_achivements(players_stats).items():
        result += f"{achivement:20}: {achiver}\n"
    #print(result)
    return "```" + result + "```"
