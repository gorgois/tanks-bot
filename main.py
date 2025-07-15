import discord
from discord import app_commands
from discord.ext import commands
import os
import cloudscraper
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    print(f"Bot is online as {bot.user}")

@bot.tree.command(name="user", description="Get player stats from Ranked RTanks")
@app_commands.describe(username="The player's exact name")
async def user(interaction: discord.Interaction, username: str):
    await interaction.response.defer()

    try:
        scraper = cloudscraper.create_scraper()
        url = f"https://ratings.ranked-rtanks.online/api/players/{username}"
        response = scraper.get(url)

        if response.status_code != 200:
            await interaction.followup.send("❌ Player not found.")
            return

        data = response.json()
        if not data or "username" not in data:
            await interaction.followup.send("❌ Player not found.")
            return

        stats = {
            "Username": data.get("username"),
            "XP": f"{data.get('experience'):,}",
            "Kills": f"{data.get('kills'):,}",
            "Deaths": f"{data.get('deaths'):,}",
            "K/D Ratio": round(data.get('kills') / data.get('deaths'), 2) if data.get('deaths') else "N/A",
            "Crystals": f"{data.get('crystals'):,}",
            "Gold Boxes": f"{data.get('gold_boxes'):,}",
            "Rating": data.get("rating")
        }

        embed = discord.Embed(
            title=f"📊 Stats for {stats['Username']}",
            color=discord.Color.blue()
        )

        for key, value in stats.items():
            if key != "Username":
                embed.add_field(name=key, value=value, inline=True)

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send("⚠️ An error occurred while fetching stats.")
        print(f"Error: {e}")

bot.run(TOKEN)