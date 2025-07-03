
import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Load or initialize data
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
else:
    users = {}

# Rank system
ranks = [
    ("Recruit", 0),
    ("Private", 1000),
    ("Gefreiter", 2500),
    ("Corporal", 5000),
    ("Master Corporal", 8500),
    ("Sergeant", 12000),
    ("Staff Sergeant", 16000),
    ("First Sergeant", 20000),
    ("Sergeant Major", 25000),
    ("Warrant Officer 1", 30000),
    ("Warrant Officer 2", 36000),
    ("Warrant Officer 3", 43000),
    ("Warrant Officer 4", 51000),
    ("Third Lieutenant", 60000),
    ("Second Lieutenant", 70000),
    ("First Lieutenant", 82000),
    ("Captain", 95000),
    ("Major", 110000),
    ("Lieutenant Colonel", 126000),
    ("Colonel", 144000),
    ("Brigadier", 164000),
    ("Major General", 186000),
    ("Lieutenant General", 210000),
    ("General", 236000),
    ("Commander", 264000),
    ("Marshal", 294000),
    ("Fieldmarshal", 326000),
    ("Generalissimo", 360000),
    ("Legend", 395000),
    ("Legend 2", 430000)
]

def get_rank(xp):
    for i in reversed(range(len(ranks))):
        if xp >= ranks[i][1]:
            return ranks[i][0], i, ranks[i][1]
    return "Recruit", 0, 0

@bot.command()
async def battle(ctx):
    uid = str(ctx.author.id)
    if uid not in users:
        users[uid] = {"xp": 0, "crystals": 0}
    earned_xp = random.randint(200, 500)
    earned_crystals = random.randint(100, 300)
    users[uid]["xp"] += earned_xp
    users[uid]["crystals"] += earned_crystals

    # Goldbox chance
    if random.randint(1, 100) <= 5:
        users[uid]["crystals"] += 1000
        gold = True
    else:
        gold = False

    with open("users.json", "w") as f:
        json.dump(users, f)

    rank, _, _ = get_rank(users[uid]["xp"])
    msg = f"🏆 You joined a battle!
You earned **{earned_xp} XP** and **💎 {earned_crystals} crystals**.
Your rank: **{rank}**"
    if gold:
        msg += "
🎉 You caught a **GOLDBOX**! (+1000 💎)"
    await ctx.send(msg)

@bot.command()
async def rank(ctx):
    uid = str(ctx.author.id)
    if uid not in users:
        await ctx.send("You haven't played yet. Use `/battle` first!")
        return
    xp = users[uid]["xp"]
    current_rank, index, current_xp = get_rank(xp)
    next_rank = ranks[index + 1][0] if index + 1 < len(ranks) else "MAX"
    next_xp = ranks[index + 1][1] if index + 1 < len(ranks) else xp

    percent = round((xp - current_xp) / (next_xp - current_xp) * 100) if next_xp > current_xp else 100
    bar = "▓" * (percent // 10) + "░" * (10 - percent // 10)

    await ctx.send(f"🎖 Rank: **{current_rank}**
Progress to **{next_rank}**: [{bar}] {percent}%
💎 Crystals: {users[uid]['crystals']}")

@bot.command()
async def shop(ctx):
    await ctx.send("🛒 **Shop**:
1. 1-min XP Pass (x2 XP) - 500 💎
2. 5-min XP Pass - 2000 💎
3. 1-hour XP Pass - 10000 💎
(More coming soon...)")

# Replace with your token
bot.run("YOUR_BOT_TOKEN")
