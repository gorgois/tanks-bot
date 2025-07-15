import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from keep_alive import keep_alive  # Keeps the bot alive on Render

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.environ.get("DISCORD_TOKEN")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}!")

@bot.tree.command(name="user", description="Get player stats from Rtanks Online")
@app_commands.describe(nickname="Exact player nickname")
async def user(interaction: discord.Interaction, nickname: str):
    await interaction.response.defer()
    url = f"https://ratings.ranked-rtanks.online/user/{nickname}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            await interaction.followup.send(f"Player `{nickname}` not found.")
            return

        soup = BeautifulSoup(res.text, 'html.parser')
        stats_table = soup.find("table")
        if not stats_table:
            await interaction.followup.send(f"Failed to parse stats for `{nickname}`.")
            return

        rows = stats_table.find_all("tr")
        data = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                data[key] = value

        embed = discord.Embed(title=f"Stats for {nickname}", color=0x00ffcc)
        for key, value in data.items():
            embed.add_field(name=key, value=value, inline=True)

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send("An error occurred while fetching data.")
        print(e)

keep_alive()
bot.run(TOKEN)