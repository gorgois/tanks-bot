import discord
from discord.ext import commands
from discord import app_commands
import os
import openai
import asyncio
from flask import Flask
from threading import Thread

# Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Load tokens from environment
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Flask app for keep-alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- AI Commands ---

@tree.command(name="ask", description="Ask the AI a question")
@app_commands.describe(question="Your question")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            max_tokens=300,
            temperature=0.7,
        )
        answer = response['choices'][0]['message']['content'].strip()
        await interaction.followup.send(answer)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@tree.command(name="image", description="Generate an image from a prompt")
@app_commands.describe(prompt="Image description")
async def image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        await interaction.followup.send(image_url)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@tree.command(name="summarize", description="Summarize text")
@app_commands.describe(text="Text to summarize")
async def summarize(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    prompt = f"Summarize the following text:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5,
        )
        summary = response['choices'][0]['message']['content'].strip()
        await interaction.followup.send(summary)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@tree.command(name="define", description="Get a definition of a word")
@app_commands.describe(word="Word to define")
async def define(interaction: discord.Interaction, word: str):
    await interaction.response.defer()
    prompt = f"Define the word '{word}' clearly and concisely."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3,
        )
        definition = response['choices'][0]['message']['content'].strip()
        await interaction.followup.send(definition)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@tree.command(name="translate", description="Translate text to a language")
@app_commands.describe(text="Text to translate", language="Target language")
async def translate(interaction: discord.Interaction, text: str, language: str):
    await interaction.response.defer()
    prompt = f"Translate the following text to {language}:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5,
        )
        translation = response['choices'][0]['message']['content'].strip()
        await interaction.followup.send(translation)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@tree.command(name="roast", description="Generate a funny roast")
@app_commands.describe(target="User or text to roast")
async def roast(interaction: discord.Interaction, target: str):
    await interaction.response.defer()
    prompt = f"Make a funny but light roast about: {target}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.9,
        )
        roast_text = response['choices'][0]['message']['content'].strip()
        await interaction.followup.send(roast_text)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

@tree.command(name="joke", description="Get a random joke")
async def joke(interaction: discord.Interaction):
    await interaction.response.defer()
    prompt = "Tell me a short, funny joke."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.9,
        )
        joke_text = response['choices'][0]['message']['content'].strip()
        await interaction.followup.send(joke_text)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

# --- Bot events ---

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}.")

# Run keep-alive flask server
keep_alive()
bot.run(DISCORD_TOKEN)