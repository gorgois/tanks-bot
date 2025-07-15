import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import requests
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

EMOJIS = {
    "goldboxes": "<:goldbox:1390056100182622401>",
    "xp": "<:crystals:1390016761851809942>",
    "crystals": "<:crystals:1390016761851809942>",
    "kd": "⚔️",
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing: {e}")

@tree.command(name="user", description="Get player stats by nickname")
@app_commands.describe(nickname="The nickname of the player")
async def user(interaction: discord.Interaction, nickname: str):
    await interaction.response.defer()
    try:
        res = requests.get(f"https://ratings.ranked-rtanks.online/api/user/{nickname}")
        if res.status_code == 200:
            data = res.json()
            embed = discord.Embed(
                title=f"{data['nickname']}'s Stats",
                color=discord.Color.gold()
            )
            embed.add_field(name="XP", value=f"{EMOJIS['xp']} {data['xp']}", inline=True)
            embed.add_field(name="Crystals", value=f"{EMOJIS['crystals']} {data['crystals']}", inline=True)
            embed.add_field(name="K/D", value=f"{EMOJIS['kd']} {data['kill_death_ratio']}", inline=True)
            embed.add_field(name="Gold Boxes", value=f"{EMOJIS['goldboxes']} {data['gold_boxes']}", inline=True)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Player not found.")
    except Exception as e:
        print(e)
        await interaction.followup.send("Failed to fetch data.")

@tree.command(name="top", description="Show leaderboard by category")
@app_commands.choices(category=[
    app_commands.Choice(name="XP", value="xp"),
    app_commands.Choice(name="Crystals", value="crystals"),
    app_commands.Choice(name="K/D", value="kill_death_ratio"),
    app_commands.Choice(name="Gold Boxes", value="gold_boxes")
])
async def top(interaction: discord.Interaction, category: app_commands.Choice[str]):
    await interaction.response.defer()
    try:
        res = requests.get("https://ratings.ranked-rtanks.online/api/leaderboard")
        if res.status_code == 200:
            data = res.json()
            top_list = sorted(data, key=lambda x: x[category.value], reverse=True)[:10]
            embed = discord.Embed(
                title=f"Top 10 by {category.name}",
                color=discord.Color.green()
            )
            for i, player in enumerate(top_list, start=1):
                emoji = EMOJIS.get(category.value, "")
                value = player.get(category.value, "N/A")
                embed.add_field(
                    name=f"{i}. {player['nickname']}",
                    value=f"{emoji} {value}",
                    inline=False
                )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Couldn't fetch leaderboard.")
    except Exception as e:
        print(e)
        await interaction.followup.send("Something went wrong.")

keep_alive()
bot.run(TOKEN)