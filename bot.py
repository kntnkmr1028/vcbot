import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread  # ← これを追加

# --- Flaskの設定 (Render用) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Renderは10000番ポートを要求することが多いため環境変数から取得
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --- Flask設定ここまで ---

load_dotenv()

# 環境変数から取得（RenderのEnvironmentタブで設定した名前に合わせる）
TOKEN = os.getenv("DISCORD_TOKEN") 
CHANNEL_ID_STR = os.getenv("CHANNEL_ID")
CHANNEL_ID = int(CHANNEL_ID_STR) if CHANNEL_ID_STR else None

intents = discord.Intents.default()
# コマンドを使う場合はここをTrueに（今回はVC参加のみならdefaultでOK）
# intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f'Joined to {channel.name}')
    else:
        print("CHANNEL_ID is not set.")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and after.channel is None:
        print("Disconnected. Reconnecting in 5 seconds...")
        await asyncio.sleep(5)
        if CHANNEL_ID:
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.connect()

# プログラムの実行
if __name__ == "__main__":
    # 1. まずWebサーバーを起動（別スレッドで裏側で動かす）
    keep_alive() 
    
    # 2. その後にBotを起動
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("TOKEN is not set in environment variables.")
