import asyncio
import random

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


class DuelSearchEngine:
    def replace_all(self, dic):
        for i, j in dic.items():
            text = self.replace(i, j)
        return text

    def find_user(self):
        with open(CHAT_BASE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self == row['name']:
                    return int(row['user_id'])

    def get_message_id(self):
        for message in app.search_messages(ch4tid, query="дуэль", limit=1, from_user=self):
            return int(message.message_id)


@app.on_message(filters.group & filters.regex("Дуэль подтверждена, можно делать ставки;"))
def duel_bet(client, message):
    str_dict = {'Дуэль подтверждена, можно делать ставки;': '',
                'Для совершения ставки - "Дуэль ставка СУММА" (реплаем на игрока)': '',
                'Для старта дуэли - "Дуэль старт': '',
                'КФ на ': '',
                '\n': ' '}
    mes = message.text
    mw_msg = DuelSearchEngine.replace_all(mes, str_dict)
    res_msg = mw_msg.split(' ')
    if float(res_msg[3]) < float(res_msg[6]):
        client.send_message(
            chat_id=message.chat.id,
            text=f"Дуэль ставка {random.randint(30, 80)}",
            reply_to_message_id=DuelSearchEngine.get_message_id(DuelSearchEngine.find_user(res_msg[1]))
        )
    elif float(res_msg[6]) < float(res_msg[3]):
        client.send_message(
            chat_id=message.chat.id,
            text=f"Дуэль ставка {random.randint(30, 80)}",
            reply_to_message_id=DuelSearchEngine.get_message_id(DuelSearchEngine.find_user(res_msg[4]))
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
