import discord
from discord.ext import commands
from discord import app_commands
import openai
import os
from flask import Flask
import threading

# Load environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

# Flask app for uptime
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_web).start()

# Discord bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    print(f"🤖 Logged in as {bot.user} (ID: {bot.user.id})")

# Roast command
@bot.tree.command(name="roast", description="Roast a user with AI-powered Tanki burns")
@app_commands.describe(user="The user you want to roast")
async def roast(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        prompt = f"""
You're a sarcastic Tanki Online veteran from 2012. Someone in the game chat is being annoying, and you need to roast them hard.
Make the roast funny, clever, and full of Tanki lingo. PG-13, but brutal.

Roast this user: {user.name}
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            max_tokens=150,
            temperature=0.9
        )

        # DEBUGGING: Print raw response
        print("🧠 OpenAI response:", response)

        if (
            response and
            "choices" in response and
            len(response.choices) > 0 and
            "message" in response.choices[0] and
            "content" in response.choices[0].message
        ):
            roast_text = response.choices[0].message.content.strip()
            await interaction.followup.send(
                f"🔥 **Roast for {user.mention}:**\n> {roast_text}", ephemeral=True
            )
        else:
            print("⚠️ OpenAI gave empty or invalid response.")
            await interaction.followup.send(
                "❌ The roast was empty or invalid. Try again shortly.", ephemeral=True
            )

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        await interaction.followup.send(
            "❌ Oops! Something went wrong with OpenAI. Try again later.", ephemeral=True
        )

# Run bot
bot.run(TOKEN)