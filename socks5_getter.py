import threading
import time

from aiosocksy import Socks5Auth
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
import aiohttp
import asyncio
import ssl
import certifi
import json

import proxy_list

temp_socks_list = []
temp_proxy_list = []
socks_threads = [0]


sslcontext = ssl.create_default_context(cafile=certifi.where())


async def start_parsing():
    while True:
        try:
            await asyncio.create_task(get_socks_list())
        except:
            await asyncio.sleep(10)

async def get_socks_list():
    temp_socks_list.clear()

    auth = Socks5Auth(login='wBNWYX', password='mkUSkp')
    proxy = '185.80.149.190:8000'
    connector = ProxyConnector()
    socks = f'socks5://{proxy}'

    async with aiohttp.ClientSession(connector=connector,
                                     request_class=ProxyClientRequest) as client:
        async with client.get('https://www.proxyscan.io/api/proxy?&ping=1000&limit=400&type=socks5', ssl=sslcontext, proxy=socks, proxy_auth=auth) as resp:
            if resp.status == 200:
                data = await resp.read()
                results_of_parsing = json.loads(data)
                for proxy in results_of_parsing:
                    temp_socks_list.append(f"{proxy['Ip']}:{proxy['Port']}")
                for socks in temp_socks_list:
                    if socks_threads[0] > 10:
                        await asyncio.sleep(1)
                        x = threading.Thread(target=between_callback_socks, args=(socks,))
                        x.start()
                        socks_threads[0] += 1
                    else:
                        x = threading.Thread(target=between_callback_socks, args=(socks,))
                        x.start()
                        socks_threads[0] += 1


def between_callback_socks(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(check_creator_socks(args))
    loop.close()


async def check_creator_socks(proxy):
    should_add = True
    for ready_socks in proxy_list.socks_list:
        if proxy == ready_socks[0]:
            should_add = False
    if should_add:
        try:
            connector = ProxyConnector()
            socks = f'socks5://{proxy}'

            async with aiohttp.ClientSession(connector=connector,
                                             request_class=ProxyClientRequest) as client:
                async with client.get('https://www.google.com/', ssl=sslcontext, proxy=socks) as resp:
                    assert resp.status == 200
        except ssl.SSLError:
            proxy_list.add_to_socks_list(proxy, time.time())
            if proxy_list.get_socks_q() > 100:
                proxy_list.socks_list.pop()
            socks_threads[0] -= 1
        except:
            socks_threads[0] -= 1
            pass




