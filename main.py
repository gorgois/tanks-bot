import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio

from utils import get_player_stats, get_leaderboard

TOKEN = "YOUR_BOT_TOKEN_HERE"  # Put your bot token here or load from env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Ranks emojis from your server by ID (example)
RANK_EMOJIS = {
    "recruit": "<:recruit:1390016678452265070>",
    "private": "<:private:1390017940824264876>",
    "gefreiter": "<:gefreiter:1390018050438336562>",
    # add all your ranks here ...
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    update_status.start()

@tree.command(name="user", description="Get player stats by username")
@app_commands.describe(username="Player username")
async def user(interaction: discord.Interaction, username: str):
    await interaction.response.defer()
    stats = get_player_stats(username)
    if not stats:
        await interaction.followup.send(f"Player `{username}` not found or API error.")
        return

    rank_emoji = RANK_EMOJIS.get(stats["Rank"].lower(), "")
    embed = discord.Embed(title=f"Stats for {stats['Username']}", color=discord.Color.blue())
    embed.add_field(name="Rank", value=f"{rank_emoji} {stats['Rank']}", inline=True)
    embed.add_field(name="XP", value=stats["XP"], inline=True)
    embed.add_field(name="Kills", value=stats["Kills"], inline=True)
    embed.add_field(name="Deaths", value=stats["Deaths"], inline=True)
    embed.add_field(name="K/D Ratio", value=stats["K/D"], inline=True)
    embed.add_field(name="Crystals", value=stats["Crystals"], inline=True)
    embed.add_field(name="Gold Boxes", value=stats["Gold Boxes"], inline=True)
    await interaction.followup.send(embed=embed)

@tree.command(name="top", description="Show top players by category")
@app_commands.describe(category="Category to show top by")
@app_commands.choices(category=[
    app_commands.Choice(name="xp", value="exp"),
    app_commands.Choice(name="kills", value="kills"),
    app_commands.Choice(name="crystals", value="crystals"),
    app_commands.Choice(name="goldboxes", value="golds"),
])
async def top(interaction: discord.Interaction, category: app_commands.Choice[str]):
    await interaction.response.defer()
    leaderboard = get_leaderboard(category.value)
    if not leaderboard:
        await interaction.followup.send("Failed to fetch leaderboard data.")
        return

    embed = discord.Embed(title=f"Top players by {category.name.capitalize()}", color=discord.Color.gold())
    for i, (name, value) in enumerate(leaderboard, 1):
        embed.add_field(name=f"{i}. {name}", value=str(value), inline=False)

    await interaction.followup.send(embed=embed)

@tasks.loop(minutes=10)
async def update_status():
    # Example: Fetch number of online players from site and update bot status
    try:
        # Dummy example - replace with real fetching code
        online_players = 1234  # get this from your data source or API
        await bot.change_presence(activity=discord.Game(name=f"{online_players} players online"))
    except Exception as e:
        print(f"Error updating status: {e}")

bot.run(TOKEN)