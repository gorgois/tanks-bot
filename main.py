import os
import discord
from discord import app_commands
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv
from keep_alive import keep_alive
keep_alive()

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default()
client = commands.Bot(command_prefix="/", intents=intents)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="DanakisDaGoat"))

# /ask
@client.tree.command(name="ask", description="Ask the AI a question.")
@app_commands.describe(prompt="What do you want to ask?")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        await interaction.followup.send(response.choices[0].message.content)
    except Exception as e:
        await interaction.followup.send("❌ Something went wrong.")

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