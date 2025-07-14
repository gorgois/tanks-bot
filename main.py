import os
import discord
import asyncio
from flask import Flask
import threading

TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))  # Set this in Render's env variables

# Read nicknames from file
def get_nicknames():
    with open('nicknames.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

nicknames = get_nicknames()

# Flask web server for Render/UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()

# Discord bot setup
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(CHANNEL_ID)
        if channel is None:
            print("Channel not found. Check CHANNEL_ID.")
            return
        for nickname in nicknames:
            await channel.send(f'/user {nickname}')
            await asyncio.sleep(30)

intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run(TOKEN)