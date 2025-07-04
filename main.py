

import discord from discord.ext import commands from discord import app_commands import os from roast import generate_roast from keep_alive import keep_alive from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN") GUILD_ID = discord.Object(id=int(os.getenv("GUILD_ID")))  # optional

intents = discord.Intents.default() intents.message_content = True intents.messages = True intents.guilds = True intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents) message_history = {}  # {user_id: [messages]}

@bot.event async def on_ready(): print(f"Bot is online as {bot.user}") try: synced = await bot.tree.sync() print(f"Synced {len(synced)} command(s)") except Exception as e: print(f"Error syncing commands: {e}")

@bot.event async def on_message(message): if message.author.bot: return

# Save up to 100 messages per user
user_id = message.author.id
if user_id not in message_history:
    message_history[user_id] = []
message_history[user_id].append(message.content)
if len(message_history[user_id]) > 100:
    message_history[user_id] = message_history[user_id][-100:]

await bot.process_commands(message)

@bot.tree.command(name="roast", description="Generate a Tanki-style roast for a user") @app_commands.describe(user="Select the user to roast") async def roast(interaction: discord.Interaction, user: discord.Member): await interaction.response.defer(ephemeral=True) msgs = message_history.get(user.id, []) if not msgs: msgs = ["They barely speak. Tank rust mode activated."]

roast = generate_roast(user.name, msgs)
await interaction.followup.send(content=roast, ephemeral=True)

keep_alive() bot.run(TOKEN)

