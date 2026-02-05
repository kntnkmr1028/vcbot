import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
#render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Renderが指定するポートでサーバーを起動
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
#render

load_dotenv()
# --- 設定項目 ---
TOKEN = os.getenv("DISCORD_TOKEN") # Botのトークン
CHANNEL_ID = int(os.getenv("CHANNEL_ID")) # 常駐させたいVCのチャンネルID
# ----------------

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(CHANNEL_ID)
    
    if channel and isinstance(channel, discord.VoiceChannel):
        # 起動時にVCへ参加
        await channel.connect()
        print(f'Joined to {channel.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Bot自身がVCから切断された場合、再接続を試みる
    if member.id == bot.user.id and after.channel is None:
        print("Disconnected. Reconnecting in 5 seconds...")
        await asyncio.sleep(5)
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.connect()

bot.run(TOKEN)
