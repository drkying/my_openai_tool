import asyncio
import os

from telethon import TelegramClient, events

from orderInOkx import order
from ai2OrderByBot import ai_get_order
from log_e2btc import log_e2btc

# api_id = 23634450
# api_hash = 'ad2960063be45070ac1c32f0edb34cca'

api_id = int(os.environ.get('TG_API_ID'))
api_hash = os.environ.get('TG_API_HASH')

client = TelegramClient('session_name', api_id, api_hash)

watch_list = [] # 监听的用户名
id_list = []

watch_list_str = os.environ.get('WATCH_LIST')
# 以,分割字符串
if watch_list_str is not None:
    watch_list = watch_list_str.split(',')
    print(watch_list)



async def get_user_id(username):
    user = await client.get_entity(username)
    return user.id

def judge_obj(obj):
    if obj == {}:
        return False
    # obj不是空对象时,且遍历obj的每一个属性不为空时，才会执行下单操作
    if obj is not None and isinstance(obj, dict):
        for key in obj:
            if obj[key] == '':
                return False
        return True
    return False

@client.on(events.NewMessage)
async def my_event_handler(event):
    if event.sender_id in id_list:
        print(event)
        log_e2btc("tg接收的消息", event.raw_text)
        try:
            obj = None
            if event.raw_text != '':
                obj = ai_get_order(event.raw_text)
            if judge_obj(obj):
                order(obj)
                log_e2btc('下单完成,e_god', obj)
            else:
                log_e2btc('未获取到下单信息')
        except Exception as e:
            log_e2btc('下单失败', e)


async def main():
    await client.start()
    for name in watch_list:
        id_list.append(await get_user_id(name))
    log_e2btc('获取到的用户和id', watch_list, id_list)
    await client.run_until_disconnected()


print(judge_obj({}))
asyncio.run(main())