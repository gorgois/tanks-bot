import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI
import asyncio

# Load .env variables if present
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise Exception("DISCORD_TOKEN and OPENAI_API_KEY must be set in environment variables.")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

# Set bot presence on ready
@bot.event
async def on_ready():
    await tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="DanakisDaGoat"))
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# --------- AI Commands ---------

@tree.command(name="ask", description="Ask any question to the AI")
@app_commands.describe(prompt="Your question")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        await interaction.followup.send(answer)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI API error: {e}")

@tree.command(name="image", description="Generate an image from a prompt")
@app_commands.describe(prompt="Image description")
async def image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        image_url = response.data[0].url
        await interaction.followup.send(image_url)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI Image generation error: {e}")

@tree.command(name="summarize", description="Summarize a text")
@app_commands.describe(text="Text to summarize")
async def summarize(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        prompt = f"Summarize the following text:\n\n{text}"
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        await interaction.followup.send(summary)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI API error: {e}")

@tree.command(name="define", description="Get definition of a word")
@app_commands.describe(word="Word to define")
async def define(interaction: discord.Interaction, word: str):
    await interaction.response.defer()
    try:
        prompt = f"Define the word '{word}' clearly and concisely."
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        definition = response.choices[0].message.content
        await interaction.followup.send(definition)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI API error: {e}")

@tree.command(name="translate", description="Translate text to English")
@app_commands.describe(text="Text to translate")
async def translate(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        prompt = f"Translate the following text to English:\n\n{text}"
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        translation = response.choices[0].message.content
        await interaction.followup.send(translation)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI API error: {e}")

@tree.command(name="roast", description="Generate a funny roast for a user")
@app_commands.describe(user="User to roast")
async def roast(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer()
    try:
        prompt = f"Write a funny, light-hearted roast for someone named {user.display_name}."
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        roast_text = response.choices[0].message.content
        await interaction.followup.send(roast_text)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI API error: {e}")

@tree.command(name="joke", description="Tell a random joke")
async def joke(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        prompt = "Tell me a funny, clean joke."
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        joke_text = response.choices[0].message.content
        await interaction.followup.send(joke_text)
    except Exception as e:
        await interaction.followup.send(f"❌ OpenAI API error: {e}")

# -------------------

bot.run(DISCORD_TOKEN)