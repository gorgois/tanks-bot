import os
import discord
from discord.ext import tasks
from discord import app_commands
import requests
from keep_alive import keep_alive  # Make sure keep_alive.py is present

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Emoji dictionary for ranks
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
    "Warrant Officer 1": "<:warrantofficer1:1390053727842472057>",
    "Warrant Officer 2": "<:warrantofficer2:1390053807274197102>",
    "Warrant Officer 3": "<:warrantofficer3:1390053863112835234>",
    "Warrant Officer 4": "<:warrantofficer4:1390053917093662750>",
    "Warrant Officer 5": "<:warrantofficer5:1390053966586318849>",
    "Third Lieutenant": "<:thirdlieutenant:1378306902257045514>",
    "Second Lieutenant": "<:secondlieutenant:1378306959941304320>",
    "First Lieutenant": "<:firstlieutenant:1378307018359836772>",
    "Captain": "<:captain:1378307107178414110>",
    "Major": "<:major:1390054463133188317>",
    "Lieutenant Colonel": "<:lieutenantcolonel:1390054483190349925>",
    "Colonel": "<:colonel:1390054505801977906>",
    "Brigadier": "<:brigadier:1378308029031776278>",
    "Major General": "<:majorgeneral:1390055209488875520>",
    "Lieutenant General": "<:lieutenantgeneral:1390055232226197514>",
    "General": "<:general:1390055254170665072>",
    "Marshall": "<:marshall:1390018947822125228>",
    "Field Marshall": "<:fieldmarshall:1390019065887592600>",
    "Commander": "<:commander:1390019160284598274>",
    "Generalisimo": "<:generalisimo:1390019231713591366>",
    "Gold Box": "<:goldbox:1390056100182622401>",
    "Crystals": "<:crystals:1390016761851809942>"
}

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("No Discord token found in environment variable DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")
    update_status.start()

@tasks.loop(minutes=10)
async def update_status():
    try:
        response = requests.get("https://ratings.ranked-rtanks.online/api/players")
        players = response.json()
        online_count = sum(1 for p in players if p.get("online"))
        await client.change_presence(activity=discord.Game(name=f"{online_count} players online"))
    except Exception as e:
        print(f"Failed to update status: {e}")

@tree.command(name="user", description="View player stats")
@app_commands.describe(username="Player name")
async def user(interaction: discord.Interaction, username: str):
    await interaction.response.defer()
    try:
        response = requests.get("https://ratings.ranked-rtanks.online/api/players")
        players = response.json()
        player = next((p for p in players if p.get("name", "").lower() == username.lower()), None)
        if not player:
            await interaction.followup.send(f"Player `{username}` not found.")
            return
        
        rank = player.get("rank", "Recruit")
        emoji = RANK_EMOJIS.get(rank, "")
        kills = player.get("kills", 0)
        deaths = player.get("deaths", 1)  # avoid division by zero
        kd = round(kills / deaths, 2)
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
    except Exception as e:
        await interaction.followup.send(f"Error fetching player data: {e}")

@tree.command(name="top", description="Show top players by category")
@app_commands.describe(category="Select category")
@app_commands.choices(category=[
    app_commands.Choice(name="K/D", value="kd"),
    app_commands.Choice(name="XP", value="xp"),
    app_commands.Choice(name="Crystals", value="crystals"),
    app_commands.Choice(name="Gold Boxes", value="goldboxes"),
])
async def top(interaction: discord.Interaction, category: app_commands.Choice[str]):
    await interaction.response.defer()
    try:
        response = requests.get("https://ratings.ranked-rtanks.online/api/players")
        players = response.json()

        if category.value == "kd":
            players.sort(key=lambda p: p.get("kills", 0) / max(p.get("deaths", 1), 1), reverse=True)
        elif category.value == "xp":
            players.sort(key=lambda p: p.get("score", 0), reverse=True)
        elif category.value == "crystals":
            players.sort(key=lambda p: p.get("crystals", 0), reverse=True)
        elif category.value == "goldboxes":
            players.sort(key=lambda p: p.get("goldboxes", 0), reverse=True)

        top10 = players[:10]
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
    except Exception as e:
        await interaction.followup.send(f"Error fetching top players: {e}")

if __name__ == "__main__":
    keep_alive()
    client.run(TOKEN)