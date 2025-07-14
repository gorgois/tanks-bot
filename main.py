import discord
from discord import app_commands
from discord.ext import tasks
import os
import aiohttp
import json
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

with open("emojis.json", "r") as f:
    emojis = json.load(f)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    await tree.sync()
    update_status.start()

# 🟢 Update bot status every 10 minutes with online player count
@tasks.loop(minutes=10)
async def update_status():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ratings.ranked-rtanks.online/api/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    count = data.get("online", 0)
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{count} players online"))
    except Exception as e:
        print("Failed to update status:", e)

# 📊 /user command
@tree.command(name="user", description="Get player stats by nickname")
@app_commands.describe(nickname="The player's nickname")
async def user(interaction: discord.Interaction, nickname: str):
    await interaction.response.defer()
    url = f"https://ratings.ranked-rtanks.online/api/user/{nickname}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title=f"{data['nickname']}'s Stats", color=discord.Color.gold())
                    embed.add_field(name="XP", value=data.get("xp", "N/A"), inline=True)
                    embed.add_field(name="Kills", value=data.get("kills", "N/A"), inline=True)
                    embed.add_field(name="Deaths", value=data.get("deaths", "N/A"), inline=True)
                    embed.add_field(name="Crystals", value=data.get("crystals", "N/A"), inline=True)
                    embed.add_field(name="Gold Boxes", value=data.get("gold_boxes", "N/A"), inline=True)
                    embed.add_field(name="K/D", value=data.get("kd_ratio", "N/A"), inline=True)
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("❌ Player not found.")
    except Exception as e:
        print("User fetch failed:", e)
        await interaction.followup.send("⚠️ Failed to fetch player data. Please try again later.")

# 🏆 /top command
@tree.command(name="top", description="Show top players")
async def top(interaction: discord.Interaction):
    await interaction.response.defer()
    url = "https://ratings.ranked-rtanks.online/api/top"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title="🏆 Top Players", color=discord.Color.blurple())
                    for i, player in enumerate(data[:10], 1):
                        line = f"**{i}.** {player['nickname']} - {player['xp']} XP {emojis.get('crystals', '')} {player['crystals']}"
                        embed.add_field(name="\u200b", value=line, inline=False)
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("⚠️ Failed to fetch leaderboard.")
    except Exception as e:
        print("Top fetch failed:", e)
        await interaction.followup.send("⚠️ Failed to fetch leaderboard data. Please try again later.")

# 🔐 Run the bot
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ DISCORD_TOKEN not found in environment variables.")
else:
    bot.run(TOKEN)