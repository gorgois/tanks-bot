import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Your emoji server or custom emoji dictionary (simplified)
EMOJIS = {
    "crystals": "<:crystals:1390016761851809942>",
    "gold": "<:goldbox:1390056100182622401>",
    "xp": "<:xp:💠>",  # Replace with your real emoji if needed
    "kd": "⚔️"
}

BASE_URL = "https://ratings.ranked-rtanks.online/api"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print("Sync error:", e)

@tree.command(name="user", description="Get RTanks player info")
@app_commands.describe(name="Exact player name")
async def user(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/player?nickname={name}") as resp:
            if resp.status != 200:
                await interaction.followup.send("⚠️ Player not found.")
                return
            data = await resp.json()
    
    embed = discord.Embed(title=f"Stats for {name}", color=discord.Color.blue())
    embed.add_field(name="XP", value=f"{EMOJIS['xp']} {data['xp']}", inline=True)
    embed.add_field(name="K/D", value=f"{EMOJIS['kd']} {data['kd']:.2f}", inline=True)
    embed.add_field(name="Gold Boxes", value=f"{EMOJIS['gold']} {data['goldBoxes']}", inline=True)
    embed.add_field(name="Crystals", value=f"{EMOJIS['crystals']} {data['crystals']}", inline=True)
    await interaction.followup.send(embed=embed)

@tree.command(name="top", description="Show top players by category")
@app_commands.choices(
    category=[
        app_commands.Choice(name="XP", value="xp"),
        app_commands.Choice(name="K/D", value="kd"),
        app_commands.Choice(name="Gold Boxes", value="goldBoxes"),
        app_commands.Choice(name="Crystals", value="crystals"),
    ]
)
async def top(interaction: discord.Interaction, category: app_commands.Choice[str]):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/leaderboard") as resp:
            if resp.status != 200:
                await interaction.followup.send("❌ Couldn't fetch the leaderboard.")
                return
            leaderboard = await resp.json()

    cat = category.value
    emoji = EMOJIS.get(cat, "")
    sorted_lb = sorted(leaderboard, key=lambda x: x[cat], reverse=True)
    top_players = sorted_lb[:10]

    desc = ""
    for i, player in enumerate(top_players, 1):
        desc += f"**{i}.** {player['nickname']} — {emoji} `{player[cat]}`\n"

    embed = discord.Embed(
        title=f"🏆 Top Players by {category.name}",
        description=desc,
        color=discord.Color.gold()
    )
    await interaction.followup.send(embed=embed)

bot.run(TOKEN)