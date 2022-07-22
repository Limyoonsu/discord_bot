import discord
import asyncio
import requests
import json
from discord.ext import commands
from collections import OrderedDict

bot = commands.Bot(command_prefix="@")

# bot info
TOKEN = ""

# nhn cloud sms 상품 info
APP_KEY = ""
API_URL = ""
SECRET_KEY = ""


@bot.event
async def on_ready():
    print('Loggend in Bot: ', bot.user.name)
    print('Bot id: ', bot.user.id)
    print('connection was succesful!')
    print('=' * 30)
    # 위 코드는 =라는 문자를 30개 출력하라는 뜻이다.

@bot.command(name='공지')
async def roll(ctx, notice):
    body = dict()
    body["title"] = "[openstack] 새로운 공지사항이 등록되었습니다."
    body["body"] = f"{notice}"
    body["sendNo"] = ""      # 발신번호
    body["recipientList"] = []

    f = open('./phone_number.txt', mode='r')
    line = None
    while True:
        PHONE = OrderedDict()
        line = f.readline().strip()

        if not line: break

        PHONE["recipientNo"] = line
        body["recipientList"].append(PHONE)
    f.close()

    #print(json.dumps(body))

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Secret-Key': SECRET_KEY
    }

    res = requests.post(f'{API_URL}/sms/v3.0/appKeys/{APP_KEY}/sender/mms',
                        data=json.dumps(body),
                        headers=headers)

    #await ctx.send(f'발송완료')    # 디스코드 채널에 전송

bot.run(TOKEN)
