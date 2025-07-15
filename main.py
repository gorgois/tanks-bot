import os
import discord
from discord import app_commands
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import asyncio
import time
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}!")

def scrape_player_stats(nickname: str):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    url = f"https://ratings.ranked-rtanks.online/user/{nickname}"
    driver.get(url)
    time.sleep(3)  # wait for page load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    table = soup.find("table")
    if not table:
        return None

    stats = {}
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            stats[key] = value

    return stats

@bot.tree.command(name="user", description="Get RTanks Online player stats")
@app_commands.describe(nickname="Exact RTanks nickname")
async def user(interaction: discord.Interaction, nickname: str):
    await interaction.response.defer()

    loop = asyncio.get_running_loop()
    stats = await loop.run_in_executor(None, scrape_player_stats, nickname)

    if not stats:
        await interaction.followup.send(f"❌ Could not find or parse data for player `{nickname}`.")
        return

    embed = discord.Embed(title=f"Stats for {nickname}", color=0x00ffcc)
    for key, val in stats.items():
        embed.add_field(name=key, value=val, inline=True)

    await interaction.followup.send(embed=embed)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)