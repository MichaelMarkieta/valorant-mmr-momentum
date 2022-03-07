import re
import aiohttp
import asyncio
import json
import getpass
import sys


async def run(username, password):
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
    #print(data)
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
    #print('User ID: ' + user_id)
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    headers['X-Riot-ClientVersion'] = "release-04.04-shipping-16-67925"
    headers['X-Riot-ClientPlatform'] = "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQ0LjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"

    async with session.get(f'https://pd.na.a.pvp.net/mmr/v1/players/{user_id}/competitiveupdates', headers=headers) as r:
        data = json.loads(await r.text())
    print(json.dumps(data, indent=4))

    await session.close()

if __name__ == '__main__':
    sys.stderr.write('Username: ')
    username = input()
    password = getpass.getpass('Password: ')
    asyncio.get_event_loop().run_until_complete(run(username, password))
