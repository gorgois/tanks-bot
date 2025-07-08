import discord
from discord.ext import commands
from discord import app_commands
import openai
import os

# Read tokens from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN or not OPENAI_API_KEY:
    raise ValueError("Missing DISCORD_TOKEN or OPENAI_API_KEY environment variables")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="danakisdagoat"))
    await tree.sync()
    print("Slash commands synced.")

# --- AI Commands ---

@tree.command(name="ask", description="Ask a question to the AI")
@app_commands.describe(question="Your question")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        await interaction.followup.send(answer)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

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
        image_url = response.data[0].url
        await interaction.followup.send(image_url)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error generating image: {str(e)}")

@tree.command(name="joke", description="Get a random joke from AI")
async def joke(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        prompt = "Tell me a short, funny joke."
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        joke_text = response.choices[0].message.content
        await interaction.followup.send(joke_text)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

@tree.command(name="roast", description="Get an AI-generated roast")
@app_commands.describe(target="User or topic to roast")
async def roast(interaction: discord.Interaction, target: str):
    await interaction.response.defer()
    try:
        prompt = f"Make a funny but friendly roast about {target}."
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        roast_text = response.choices[0].message.content
        await interaction.followup.send(roast_text)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

@tree.command(name="summarize", description="Summarize a text")
@app_commands.describe(text="Text to summarize")
async def summarize(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        prompt = f"Summarize the following text briefly:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message.content
        await interaction.followup.send(summary)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

@tree.command(name="translate", description="Translate text to English")
@app_commands.describe(text="Text to translate")
async def translate(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        prompt = f"Translate the following text to English:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        translation = response.choices[0].message.content
        await interaction.followup.send(translation)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

@tree.command(name="define", description="Get a definition for a word")
@app_commands.describe(word="Word to define")
async def define(interaction: discord.Interaction, word: str):
    await interaction.response.defer()
    try:
        prompt = f"Define the word: {word}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        definition = response.choices[0].message.content
        await interaction.followup.send(definition)
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    bot.run(TOKEN)