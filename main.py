import os
import discord
from discord.ext import commands
from discord import app_commands
from openai import OpenAI
from keep_alive import keep_alive
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Set bot status
@bot.event
async def on_ready():
    await bot.tree.sync()
    activity = discord.Activity(type=discord.ActivityType.listening, name="DanakisDaGoat")
    await bot.change_presence(activity=activity)
    print(f"✅ Logged in as {bot.user} and synced commands.")

# /ask command
@bot.tree.command(name="ask", description="Ask something to the AI")
@app_commands.describe(prompt="Your question or prompt")
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
        await interaction.followup.send("❌ Something went wrong. Please try again later.")
        print(f"[ERROR] {e}")

# Keep bot alive
keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)

# /image
@client.tree.command(name="image", description="Generate an image with AI.")
@app_commands.describe(prompt="Describe the image you want to generate")
async def image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        response = openai_client.images.generate(prompt=prompt, n=1, size="512x512")
        image_url = response.data[0].url
        await interaction.followup.send(image_url)
    except Exception as e:
        await interaction.followup.send("❌ Couldn't generate image.")

# /define
@client.tree.command(name="define", description="Get the definition of a word or concept.")
@app_commands.describe(term="What do you want defined?")
async def define(interaction: discord.Interaction, term: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Define: {term}"}]
        )
        await interaction.followup.send(response.choices[0].message.content)
    except:
        await interaction.followup.send("❌ Failed to define.")

# /translate
@client.tree.command(name="translate", description="Translate text to another language.")
@app_commands.describe(text="What to translate", language="Language to translate to")
async def translate(interaction: discord.Interaction, text: str, language: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Translate this to {language}: {text}"
            }]
        )
        await interaction.followup.send(response.choices[0].message.content)
    except:
        await interaction.followup.send("❌ Could not translate.")

# /summarize
@client.tree.command(name="summarize", description="Summarize a long text.")
@app_commands.describe(text="The text to summarize")
async def summarize(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize this: {text}"}]
        )
        await interaction.followup.send(response.choices[0].message.content)
    except:
        await interaction.followup.send("❌ Failed to summarize.")

# /joke
@client.tree.command(name="joke", description="Get a random joke from the AI.")
async def joke(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Tell me a funny joke."}]
        )
        await interaction.followup.send(response.choices[0].message.content)
    except:
        await interaction.followup.send("❌ No joke for now.")

# /roast
@client.tree.command(name="roast", description="Roast someone with AI.")
@app_commands.describe(user="Tag the user to roast")
async def roast(interaction: discord.Interaction, user: discord.User):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Roast {user.name} in a funny but friendly way."}]
        )
        await interaction.followup.send(response.choices[0].message.content)
    except:
        await interaction.followup.send("❌ No roast today.")

client.run(TOKEN)