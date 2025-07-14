import discord
from discord import app_commands
from discord.ext import tasks
import requests
import json
import asyncio
from keep_alive import keep_alive

# Replace with your actual emoji IDs from your server
RANK_EMOJIS = {
    "Recruit": "<:recruit:1390016678452265070>",
    "Private": "<:private:1390017940824264876>",
    "Gefreiter": "<:gefreiter:1390018050438336562>",
    "Corporal": "<:corporal:1390018154956066978>",
    "Master Corporal": "<:mastercorporal:1390018238213132409>",
    "Sergeant": "<:sergeant:1390052941641023540>",
    "Staff Sergeant": "<:staffsergeant:1390018562802061332>",
    "Master Sergeant": "<:mastersergeant:1390018691168473199>",
    "First Sergeant": "<:firstsergeant:1390018767991607481>",
    "Sergeant Major": "<:sergeantmajor:1390018851994996867>",
    "Commander": "<:commander:1390019160284598274>",
    "Generalisimo": "<:generalisimo:1390019231713591366>",
    # Add all other rank mappings...
}

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # Replace this securely

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")
    update_status.start()

# --- STATUS REFRESH ---
@tasks.loop(minutes=10)
async def update_status():
    try:
        url = "https://ratings.ranked-rtanks.online/ladder"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text
            online_count = data.count('online-indicator')
            await client.change_presence(activity=discord.Game(name=f"{online_count} players online"))
    except Exception as e:
        print("Status update error:", e)

# --- /user command ---
@tree.command(name="user", description="Get real-time RTanks player stats")
async def user(interaction: discord.Interaction, username: str):
    await interaction.response.defer()
    url = f"https://ratings.ranked-rtanks.online/user/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        await interaction.followup.send(f"❌ Player `{username}` not found.")
        return

    data = response.text
    try:
        json_data = json.loads(data)

        rank = json_data.get("rank", "Unknown")
        kd = json_data.get("kd", "N/A")
        crystals = json_data.get("crystals", "N/A")
        xp = json_data.get("xp", "N/A")
        golds = json_data.get("goldboxes", "N/A")
        online = "🟢 Online" if json_data.get("online", False) else "⚫ Offline"

        emoji = RANK_EMOJIS.get(rank, "")
        embed = discord.Embed(title=f"{username}'s Profile", color=discord.Color.blue())
        embed.set_thumbnail(url=f"https://raw.githubusercontent.com/your-rank-image-path/{rank.lower().replace(' ', '')}.png")
        embed.add_field(name="Rank", value=f"{emoji} {rank}", inline=False)
        embed.add_field(name="Status", value=online, inline=True)
        embed.add_field(name="K/D", value=kd, inline=True)
        embed.add_field(name="Crystals", value=crystals, inline=True)
        embed.add_field(name="XP", value=xp, inline=True)
        embed.add_field(name="Gold Boxes", value=golds, inline=True)
        embed.set_footer(text="Live data from RTanks")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        print(e)
        await interaction.followup.send("⚠️ Error fetching data.")

# --- /top command ---
@tree.command(name="top", description="View top players by a stat category")
async def top(interaction: discord.Interaction, category: str):
    await interaction.response.defer()
    url = "https://ratings.ranked-rtanks.online/ladder"
    response = requests.get(url)

    if response.status_code != 200:
        await interaction.followup.send("Failed to fetch leaderboard.")
        return

    try:
        leaderboard = json.loads(response.text)

        if category not in ["xp", "kd", "crystals", "goldboxes"]:
            await interaction.followup.send("Invalid category. Use: xp, kd, crystals, goldboxes")
            return

        sorted_players = sorted(leaderboard, key=lambda x: x.get(category, 0), reverse=True)
        top10 = sorted_players[:10]

        embed = discord.Embed(title=f"🏆 Top 10 by {category.capitalize()}", color=discord.Color.gold())
        for i, p in enumerate(top10, 1):
            embed.add_field(
                name=f"{i}. {p['username']}",
                value=f"{category.upper()}: {p.get(category, 0)} | Rank: {p.get('rank', 'Unknown')}",
                inline=False
            )
        await interaction.followup.send(embed=embed)

    except Exception as e:
        print(e)
        await interaction.followup.send("Error parsing leaderboard.")

# Start Flask keep-alive
keep_alive()
client.run(TOKEN)