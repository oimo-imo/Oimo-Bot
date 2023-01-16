import discord
import os
from time import sleep
from discord.ext import tasks
from datetime import datetime
from pytz import timezone
import feedparser
import asyncio

# TOKENとチャンネルID
CHANNEL_ID=977891750653861898
CHANNEL_ID_rss=1064559798089154701

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await greet()
    loop.start()
    time_check.start()
    loop_rss.start()

#起動したらおはよう！と言う
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('おはよう！')
    

# ▼▼▼ メッセージ送受信に関する機能 ▼▼▼

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「oimo」と発言したら「おいも」が返る処理
    if message.content == 'oimo':
        await message.channel.send('おいも')


# ▼▼▼ここから時間に関する機能 ▼▼▼

# 19時30分になったらゴミ出しに行こうねと通知
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now(timezone('Asia/Tokyo'))
    if now.hour == 19 and now.minute == 30:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('ゴミ出しに行こうね！')  


#次の日のゴミ出しの内容を毎日19時に通知
# 30秒に一回ループ
@tasks.loop(seconds=60)
async def time_check():
    sleepTime = 0
    # 現在の時刻
    now = datetime.now(timezone('Asia/Tokyo'))
    if now.weekday() == 6 and now.hour == 19 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('月曜日は段ボールの日だよ！')  
    elif now.weekday() == 0 and now.hour == 19 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('火曜日は燃えるゴミの日だよ！')
    elif now.weekday() == 1 and now.hour == 19 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('水曜日は燃えないゴミの日だよ！')
    elif now.weekday() == 2 and now.hour == 19 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('木曜日は燃えるゴミの日だよ！')
    elif now.weekday() == 3 and now.hour == 19 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('金曜日はペットボトルの日だよ！')
    elif now.weekday() == 4 and now.hour == 19 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('土曜日は燃えるゴミの日だよ！')


#▼▼▼ 指定時間にRSSからニュースを通知する ▼▼▼
RSS_URL = 'https://automaton-media.com/feed/' #AUTOMATONのRSS-URL
news_list = []
 
async def pickup():
    d = feedparser.parse(RSS_URL)
    for entry in d.entries:
        print(entry.title, entry.link)
        channel = client.get_channel(CHANNEL_ID_rss)
        await channel.send(entry.title+ entry.link)
        news_list.append(entry.title+ '\r\n'+ entry.link)

@tasks.loop(seconds=60)
async def loop_rss():
    now = datetime.now()
    if now.hour == 12 and now.minute == 00:
        await pickup()


# Botの起動とDiscordサーバーへの接続
client.run(os.environ["DISCORD_TOKEN"])
