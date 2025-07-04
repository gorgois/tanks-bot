import discord
from discord.ext import commands
from discord import app_commands
import openai
import os
from flask import Flask
import threading

# Get secrets from environment
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Web server for keeping bot alive (for Render + UptimeRobot)
app = Flask(__name__)

@app.route("/")
def home():
    return "Roast Bot is running."

def run_web():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_web).start()

# Ready event
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Sync error: {e}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# Roast command
@bot.tree.command(name="roast", description="Pick a user to roast with Tanki-style burns.")
@app_commands.describe(user="The user you want to roast")
async def roast(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        prompt = f"""
You're a sarcastic Tanki Online veteran from 2012. Someone in the game chat is being annoying, and you need to roast them hard.
The roast must be funny, clever, and based on Tanki lingo and player stereotypes. Keep it PG-13 but devastating.

Target username: {user.name}

Now generate the roast as if you're talking to them directly.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.9
        )

        roast_text = response.choices[0].message.content.strip()
        await interaction.followup.send(f"🔥 **Roast for {user.mention}:**\n> {roast_text}", ephemeral=True)

    except Exception as e:
        print(f"OpenAI error: {e}")
        await interaction.followup.send("❌ Oops! Something went wrong generating the roast. Try again later.", ephemeral=True)

# Start the bot
bot.run(TOKEN)