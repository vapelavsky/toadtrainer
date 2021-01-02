import asyncio
import random
import re

import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
import logging
import os
import csv

from config import ACCOUNT, APP_ID, HASH_ID, BASE_DIR

app = Client(ACCOUNT, APP_ID, HASH_ID)
ch4tid = -1001195752130
CHAT_BASE = os.path.join(BASE_DIR, 'elit_chat.csv')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))


def find_user(user):
    with open(CHAT_BASE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if user == row['name']:
                return int(row['user_id'])


def get_message_id(user):
    for message in app.search_messages(ch4tid, query="дуэль", limit=1, from_user=user):
        return int(message.message_id)


@app.on_message(filters.regex("Дуэль подтверждена, можно делать ставки;"))
def duel_bet(client, message):
    toad_kf = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)', message.text)
    nicknames = re.findall(r'КФ на (.*?) -', message.text)

    if float(toad_kf[0]) < float(toad_kf[1]):
        client.send_message(
            chat_id=message.chat.id,
            text=f"Дуэль ставка 50",
            reply_to_message_id=get_message_id(find_user(nicknames[0]))
        )
    elif float(toad_kf[1]) < float(toad_kf[0]):
        client.send_message(
            chat_id=message.chat.id,
            text=f"Дуэль ставка 50",
            reply_to_message_id=get_message_id(find_user(nicknames[1]))
        )
    elif float(toad_kf[0]) == float(toad_kf[1]):
        client.send_message(
            chat_id=message.chat.id,
            text=f"Дуэль ставка 50",
            reply_to_message_id=get_message_id(find_user(nicknames[random.randint(0, 1)]))
        )
    else:
        client.send_message(
            chat_id=message.chat.id,
            text="Бот пошёл по пизде, свяжитесь с @vapelavsky",
            reply_to_message_id=message.message_id
        )


async def feed():
    await app.send_message(ch4tid, "Покормить жабу")


async def job():
    await app.send_message(ch4tid, "Отправить жабу на работу")
    await asyncio.sleep(7200)
    await app.send_message(ch4tid, "Завершить работу")


scheduler = AsyncIOScheduler()
scheduler.add_job(feed, "interval", seconds=43210)
scheduler.add_job(job, "interval", seconds=21600)
scheduler.start()
app.run()
