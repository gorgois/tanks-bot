import os
import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
bot.remove_command("help")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="danakisdagoat"))
    print(f"Bot is online as {bot.user}")

# /ask command
@bot.tree.command(name="ask", description="Ask the AI any question.")
@app_commands.describe(prompt="Your question or message")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo"
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception as e:
        await interaction.followup.send("❌ Something went wrong.")

# /define command
@bot.tree.command(name="define", description="Define a word or concept.")
@app_commands.describe(word="The word to define")
async def define(interaction: discord.Interaction, word: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": f"Define the word: {word}"}],
            model="gpt-3.5-turbo"
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception:
        await interaction.followup.send("❌ Could not define the word.")

# /translate command
@bot.tree.command(name="translate", description="Translate text to another language.")
@app_commands.describe(text="Text to translate", language="Language to translate to")
async def translate(interaction: discord.Interaction, text: str, language: str):
    await interaction.response.defer()
    try:
        prompt = f"Translate this to {language}:\n{text}"
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo"
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception:
        await interaction.followup.send("❌ Translation failed.")

# /summarize command
@bot.tree.command(name="summarize", description="Summarize a large block of text.")
@app_commands.describe(text="Text to summarize")
async def summarize(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        prompt = f"Summarize this:\n{text}"
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo"
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception:
        await interaction.followup.send("❌ Could not summarize.")

# /roast command
@bot.tree.command(name="roast", description="Roast someone with AI.")
@app_commands.describe(name="Name or subject to roast")
async def roast(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    try:
        prompt = f"Roast someone named {name} in a funny and clever way."
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo"
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception:
        await interaction.followup.send("❌ Couldn't generate roast.")

# /joke command
@bot.tree.command(name="joke", description="Tell a random joke.")
async def joke(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": "Tell me a funny joke"}],
            model="gpt-3.5-turbo"
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception:
        await interaction.followup.send("❌ Couldn't tell a joke.")

bot.run(DISCORD_TOKEN)