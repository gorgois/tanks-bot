import discord 
from discord.ext import commands 
from discord import app_commands 
import openai 
import aiohttp 
import random 
import json 
import os 
from keep_alive import keep_alive

intents = discord.Intents.all() bot = commands.Bot(command_prefix="/", intents=intents) bot.remove_command("help")

openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE): with open(DATA_FILE, "w") as f: json.dump({}, f)

def load_data(): with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data): with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

@bot.event async def on_ready(): activity = discord.Activity(type=discord.ActivityType.listening, name="danakisdagoat") await bot.change_presence(activity=activity) print(f"Logged in as {bot.user}") try: synced = await bot.tree.sync() print(f"Synced {len(synced)} command(s)") except Exception as e: print(f"Sync error: {e}")

@bot.tree.command(name="ask", description="Ask the AI a question") @app_commands.describe(prompt="Your question") async def ask(interaction: discord.Interaction, prompt: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}] ) answer = response["choices"][0]["message"]["content"] await interaction.followup.send(answer) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="image", description="Generate an image using AI") @app_commands.describe(prompt="Describe the image") async def image(interaction: discord.Interaction, prompt: str): await interaction.response.defer() try: response = openai.Image.create(prompt=prompt, n=1, size="512x512") image_url = response["data"][0]["url"] await interaction.followup.send(image_url) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="summarize", description="Summarize a long text") @app_commands.describe(text="The text to summarize") async def summarize(interaction: discord.Interaction, text: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "user", "content": f"Summarize the following: {text}"} ] ) summary = response["choices"][0]["message"]["content"] await interaction.followup.send(summary) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="define", description="Define a word") @app_commands.describe(word="The word to define") async def define(interaction: discord.Interaction, word: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "user", "content": f"Define the word: {word}"} ] ) definition = response["choices"][0]["message"]["content"] await interaction.followup.send(definition) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="translate", description="Translate a phrase") @app_commands.describe(text="Text to translate", language="Target language") async def translate(interaction: discord.Interaction, text: str, language: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[ {"role": "user", "content": f"Translate this to {language}: {text}"} ] ) translation = response["choices"][0]["message"]["content"] await interaction.followup.send(translation) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="roast", description="Roast a user in a funny way") @app_commands.describe(user="The user to roast") async def roast(interaction: discord.Interaction, user: discord.Member): await interaction.response.defer() try: prompts = [ f"Roast {user.name} in a funny and creative way.", f"Make a hilarious roast about {user.display_name}.", f"Say something savage but funny about {user.name}." ] response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": random.choice(prompts)}] ) roast_text = response["choices"][0]["message"]["content"] await interaction.followup.send(roast_text) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="joke", description="Tell a random joke") async def joke(interaction: discord.Interaction): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Tell me a funny joke."}] ) joke_text = response["choices"][0]["message"]["content"] await interaction.followup.send(joke_text) except Exception as e: await interaction.followup.send(f"Error: {str(e)}")

keep_alive() bot.run(os.getenv("DISCORD_TOKEN"))

