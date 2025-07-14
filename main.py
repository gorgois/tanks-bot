import os
import discord
from discord.ext import tasks, commands
from discord import app_commands
import requests
import time
from keep_alive import keep_alive

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Cooldown and caching setup
user_cooldowns = {}  # user_id -> timestamp of last command
cache = {"players": None, "timestamp": 0}
CACHE_DURATION = 60  # seconds cooldown for data fetch

RANK_EMOJIS = {
    # same as before ...
}

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("No Discord token found in environment variable DISCORD_BOT_TOKEN")

def get_players_data():
    now = time.time()
    if cache["players"] and now - cache["timestamp"] < CACHE_DURATION:
        return cache["players"]

    try:
        response = requests.get("https://ratings.ranked-rtanks.online/api/players")
        if response.status_code == 429:
            return "RATE_LIMIT"
        response.raise_for_status()
        data = response.json()
        cache["players"] = data
        cache["timestamp"] = now
        return data
    except Exception as e:
        print(f"Error fetching players data: {e}")
        return None

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")
    update_status.start()

@tasks.loop(minutes=10)
async def update_status():
    data = get_players_data()
    if isinstance(data, list):
        online_count = sum(1 for p in data if p.get("online"))
        await client.change_presence(activity=discord.Game(name=f"{online_count} players online"))
    else:
        print("Could not update status due to rate limit or fetch error")

def is_on_cooldown(user_id):
    now = time.time()
    last = user_cooldowns.get(user_id, 0)
    return (now - last) < 30

def set_cooldown(user_id):
    user_cooldowns[user_id] = time.time()

@tree.command(name="user", description="View player stats")
@app_commands.describe(username="Player name")
async def user(interaction: discord.Interaction, username: str):
    if is_on_cooldown(interaction.user.id):
        await interaction.response.send_message("⏳ Please wait 30 seconds before using this command again.", ephemeral=True)
        return
    set_cooldown(interaction.user.id)
    await interaction.response.defer()
    data = get_players_data()
    if data == "RATE_LIMIT":
        await interaction.followup.send("⚠️ Rate limit reached, please try again later.")
        return
    if not data:
        await interaction.followup.send("⚠️ Failed to fetch player data. Please try again later.")
        return

    player = next((p for p in data if p.get("name", "").lower() == username.lower()), None)
    if not player:
        await interaction.followup.send(f"❌ Player `{username}` not found.")
        return

    rank = player.get("rank", "Recruit")
    emoji = RANK_EMOJIS.get(rank, "")
    kills = player.get("kills", 0)
    deaths = player.get("deaths", 1)
    kd = round(kills / max(deaths,1), 2)
    xp = player.get("score", 0)
    crystals = player.get("crystals", 0)
    goldboxes = player.get("goldboxes", 0)
    online_status = "🟢 Online" if player.get("online") else "⚫ Offline"

    embed = discord.Embed(title=f"{emoji} {player['name']}", color=discord.Color.blue())
    embed.add_field(name="Rank", value=rank)
    embed.add_field(name="Status", value=online_status)
    embed.add_field(name="Kills", value=kills)
    embed.add_field(name="Deaths", value=deaths)
    embed.add_field(name="K/D", value=kd)
    embed.add_field(name="XP", value=xp)
    embed.add_field(name="Crystals", value=crystals)
    embed.add_field(name="Gold Boxes", value=goldboxes)
    await interaction.followup.send(embed=embed)

@tree.command(name="top", description="Show top players by category")
@app_commands.describe(category="Select category")
@app_commands.choices(category=[
    app_commands.Choice(name="K/D", value="kd"),
    app_commands.Choice(name="XP", value="xp"),
    app_commands.Choice(name="Crystals", value="crystals"),
    app_commands.Choice(name="Gold Boxes", value="goldboxes"),
])
async def top(interaction: discord.Interaction, category: app_commands.Choice[str]):
    if is_on_cooldown(interaction.user.id):
        await interaction.response.send_message("⏳ Please wait 30 seconds before using this command again.", ephemeral=True)
        return
    set_cooldown(interaction.user.id)
    await interaction.response.defer()
    data = get_players_data()
    if data == "RATE_LIMIT":
        await interaction.followup.send("⚠️ Rate limit reached, please try again later.")
        return
    if not data:
        await interaction.followup.send("⚠️ Failed to fetch leaderboard data. Please try again later.")
        return

    if category.value == "kd":
        data.sort(key=lambda p: p.get("kills", 0) / max(p.get("deaths", 1), 1), reverse=True)
    elif category.value == "xp":
        data.sort(key=lambda p: p.get("score", 0), reverse=True)
    elif category.value == "crystals":
        data.sort(key=lambda p: p.get("crystals", 0), reverse=True)
    elif category.value == "goldboxes":
        data.sort(key=lambda p: p.get("goldboxes", 0), reverse=True)

    top10 = data[:10]
    embed = discord.Embed(title=f"Top 10 players by {category.name}", color=discord.Color.gold())
    for i, p in enumerate(top10, start=1):
        rank = p.get("rank", "Recruit")
        emoji = RANK_EMOJIS.get(rank, "")
        stat_value = {
            "kd": round(p.get("kills", 0) / max(p.get("deaths", 1), 1), 2),
            "xp": p.get("score", 0),
            "crystals": p.get("crystals", 0),
            "goldboxes": p.get("goldboxes", 0),
        }[category.value]
        embed.add_field(name=f"#{i} {emoji} {p['name']}", value=f"{category.name}: {stat_value}", inline=False)
    await interaction.followup.send(embed=embed)

if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)