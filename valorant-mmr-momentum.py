import re
import aiohttp
import asyncio
import json
import getpass
import sys
import os
import time


async def run(username, password):

    match_history_index = 0
    matches_analyzed = 0
    wins = 0
    losses = 0
    win_rr = 0
    loss_rr = 0
    current_act_rank = None
    peak_act_rank = None
    lowest_act_rank = None
    # project_act_rank = None
    ranks = {
        "0": "UNRANKED",
        "1": "Unused1",
        "2": "Unused2",
        "3": "IRON 1",
        "4": "IRON 2",
        "5": "IRON 3",
        "6": "BRONZE 1",
        "7": "BRONZE 2",
        "8": "BRONZE 3",
        "9": "SILVER 1",
        "10": "SILVER 2",
        "11": "SILVER 3",
        "12": "GOLD 1",
        "13": "GOLD 2",
        "14": "GOLD 3",
        "15": "PLATINUM 1",
        "16": "PLATINUM 2",
        "17": "PLATINUM 3",
        "18": "DIAMOND 1",
        "19": "DIAMOND 2",
        "20": "DIAMOND 3",
        "21": "IMMORTAL 1",
        "22": "IMMORTAL 2",
        "23": "IMMORTAL 3",
        "24": "RADIANT",
    }

    e4a2 = "d929bc38-4ab6-7da4-94f0-ee84f8ac141e"
    e4a1 = "573f53ac-41a5-3a7d-d9ce-d6a6298e5704"
    e3a3 = "a16955a5-4ad0-f761-5e9e-389df1c892fb"
    e3a2 = "4cb622e1-4244-6da3-7276-8daaf1c01be2"
    e3a1 = "2a27e5d2-4d30-c9e2-b15a-93b8909a442c"
    e2a3 = "52e9749a-429b-7060-99fe-4595426a0cf7"
    e2a2 = "ab57ef51-4e59-da91-cc8d-51a5a2b9b8ff"
    e2a1 = "97b6e739-44cc-ffa7-49ad-398ba502ceb0"
    e1a3 = None
    e1a2 = None
    e1a1 = None

    this_act = True

    session = aiohttp.ClientSession(
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/99.0.4844.51 Safari/537.36"}
    )
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    # print(data)
    pattern = re.compile(
        'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    #print('Access Token: ' + access_token)
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    #print('Entitlements Token: ' + entitlements_token)

    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    # user_id = "c4b0521d-89d9-42e9-b905-2347ad2ceb72"
    # print('User ID: ' + user_id)
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    headers['X-Riot-ClientVersion'] = "release-04.04-shipping-16-67925"
    headers['X-Riot-ClientPlatform'] = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQ0LjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"

    competitiveupdates = []

    async with session.get(f'https://pd.na.a.pvp.net/mmr/v1/players/{user_id}/competitiveupdates?startIndex=0&endIndex=19', headers=headers) as r:
        data = json.loads(await r.text())
        reversed_matches = data["Matches"][::-1]
        competitiveupdates += reversed_matches

    for match in competitiveupdates:
        # if (match["SeasonID"] != e4a2):
        #     this_act = False
        #     break

        if match["RankedRatingEarned"] == 0:
            continue
        else:
            match_result = None
            if current_act_rank == None:
                if int(match["TierAfterUpdate"]) > 0:
                    current_act_rank = int(match["TierAfterUpdate"])
            if peak_act_rank == None:
                if int(match["TierAfterUpdate"]) > 0:
                    peak_act_rank = int(match["TierAfterUpdate"])
            if lowest_act_rank == None:
                if int(match["TierAfterUpdate"]) > 0:
                    lowest_act_rank = int(match["TierAfterUpdate"])

            if match["RankedRatingEarned"] > 0:
                win_rr += abs(match["RankedRatingEarned"])
                wins += 1
                matches_analyzed += 1
                match_result = "Win"
            elif match["RankedRatingEarned"] < 0:
                loss_rr += abs(match["RankedRatingEarned"])
                losses += 1
                matches_analyzed += 1
                match_result = "Loss"

            if int(match["TierAfterUpdate"]) > int(peak_act_rank):
                if int(match["TierAfterUpdate"]) > 0:
                    peak_act_rank = int(match["TierAfterUpdate"])
            if int(match["TierAfterUpdate"]) < int(lowest_act_rank):
                if int(match["TierAfterUpdate"]) > 0:
                    lowest_act_rank = int(match["TierAfterUpdate"])

            mmr_momentum = (wins and win_rr / wins or 0) - \
                (losses and loss_rr / losses or 0)

            print(
                f'{match_result} ({match["RankedRatingEarned"]})\t| wins: {wins} (+{win_rr})\t| losses: {losses} (-{loss_rr})\t| mmr_momentum {mmr_momentum:.2f}'
                .expandtabs(14)
            )

    await session.close()

    print(f"\n")
    print(f"===== E4A2 MMR Momentum =====")
    print(f"Matches analyzed: {matches_analyzed}")
    print(f"Current rank: {ranks[str(current_act_rank)]}")
    print(f"Peak rank: {ranks[str(peak_act_rank)]}")
    print(f"Lowest rank: {ranks[str(lowest_act_rank)]}")
    print(f"The rank you deserve: ___")

if __name__ == '__main__':
    if os.environ.get('VAL_DEBUG') == 'True':
        username = os.environ.get('VAL_USERNAME')
        password = os.environ.get('VAL_PASSWORD')
    else:
        sys.stderr.write('Username: ')
        username = input()
        password = getpass.getpass('Password: ')
    asyncio.get_event_loop().run_until_complete(run(username, password))
