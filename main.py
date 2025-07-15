import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup
import httpx
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="user", description="Check stats for a RTanks Online player")
@app_commands.describe(nickname="Exact in-game nickname")
async def user(interaction: discord.Interaction, nickname: str):
    await interaction.response.defer()

    url = f"https://ratings.ranked-rtanks.online/user/{nickname}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    
    if r.status_code != 200:
        await interaction.followup.send("❌ Player not found or website is down.")
        return

    soup = BeautifulSoup(r.text, "html.parser")

    try:
        rank = soup.select_one("div.player-info span.rank").text.strip()
        crystals = soup.select_one("div.crystals span.value").text.strip()
        golds = soup.select_one("div.golds span.value").text.strip()
        kd = soup.select_one("div.kd span.value").text.strip()
        xp = soup.select_one("div.xp span.value").text.strip()
    except:
        await interaction.followup.send("⚠️ Failed to parse the player data.")
        return

    embed = discord.Embed(title=f"Stats for {nickname}", color=0x2ecc71)
    embed.add_field(name="Rank", value=rank, inline=True)
    embed.add_field(name="Crystals", value=crystals, inline=True)
    embed.add_field(name="Gold Boxes", value=golds, inline=True)
    embed.add_field(name="K/D", value=kd, inline=True)
    embed.add_field(name="XP", value=xp, inline=True)
    embed.set_footer(text="RTanks Online")

    await interaction.followup.send(embed=embed)

# Keep the bot alive
keep_alive()

# Get token from environment variable
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
bot.run(TOKEN)