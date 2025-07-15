import os
import discord
from discord.ext import tasks
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))

# Specific users and their custom emoji reactions
SPECIAL_USERS = {
    1367486289787752448: "🔥",  # Replace with actual user ID
    987654321098765432: "💀"
}

# Default emoji for all other users
DEFAULT_EMOJI = "🏳️‍🌈"  # Pride flag

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == CHANNEL_ID:
        # Get emoji for user or use the default pride flag
        emoji = SPECIAL_USERS.get(message.author.id, DEFAULT_EMOJI)
        try:
            await message.add_reaction(emoji)
        except Exception as e:
            print(f"❌ Failed to react: {e}")

keep_alive()
client.run(TOKEN)