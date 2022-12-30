import os
from lib2to3.pgen2.token import GREATER
import schedule
import discord
from time import sleep
from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
import feedparser

intents=discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# TOKENとチャンネルID
CHANNEL_ID=977891750653861898

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await greet()

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == 'oimo':
        await message.channel.send('おいも')

#起動したらおはよう！と言う
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('おはよう！')

# 指定時間に走る処理
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '19:30':
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('ゴミ出しに行けよ！')  


#次の日のゴミ出しの内容を毎日19時に通知
# 30秒に一回ループ
@tasks.loop(seconds=30)
async def time_check():
    sleepTime = 0
    # 現在の時刻
    now = datetime()
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
    


time_check.start()
loop.start()


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)


bot.run(os.environ["DISCORD_TOKEN"])
