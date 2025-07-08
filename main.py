import discord from discord.ext import commands from discord import app_commands import openai import os import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")

intents = discord.Intents.default() intents.message_content = True bot = commands.Bot(command_prefix="!", intents=intents)

discord_token = os.getenv("DISCORD_TOKEN")

@bot.event async def on_ready(): print(f"Logged in as {bot.user.name} ({bot.user.id})") try: synced = await bot.tree.sync() print(f"Synced {len(synced)} command(s)") except Exception as e: print(f"Error syncing commands: {e}")

/ask command

@bot.tree.command(name="ask", description="Ask anything to ChatGPT") @app_commands.describe(question="Your question") async def ask(interaction: discord.Interaction, question: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}] ) answer = response.choices[0].message.content await interaction.followup.send(f"Question: {question}\nAnswer: {answer}") except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

/image command

@bot.tree.command(name="image", description="Generate an AI image") @app_commands.describe(prompt="What image should the AI generate?") async def image(interaction: discord.Interaction, prompt: str): await interaction.response.defer() try: response = openai.Image.create( prompt=prompt, n=1, size="512x512" ) image_url = response['data'][0]['url'] await interaction.followup.send(f"Here’s your image:\n{image_url}") except Exception as e: await interaction.followup.send(f"❌ Error generating image: {e}")

/define command

@bot.tree.command(name="define", description="Define a word") @app_commands.describe(word="Word to define") async def define(interaction: discord.Interaction, word: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Define the word: {word}"}] ) answer = response.choices[0].message.content await interaction.followup.send(f"Definition of {word}: {answer}") except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

/summarize command

@bot.tree.command(name="summarize", description="Summarize a paragraph") @app_commands.describe(text="Text to summarize") async def summarize(interaction: discord.Interaction, text: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Summarize this: {text}"}] ) answer = response.choices[0].message.content await interaction.followup.send(f"Summary: {answer}") except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

/translate command

@bot.tree.command(name="translate", description="Translate text to another language") @app_commands.describe(text="Text to translate", language="Target language") async def translate(interaction: discord.Interaction, text: str, language: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Translate this to {language}: {text}"}] ) answer = response.choices[0].message.content await interaction.followup.send(f"Translation: {answer}") except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

/roast command

@bot.tree.command(name="roast", description="Roast someone") @app_commands.describe(name="Name of the person to roast") async def roast(interaction: discord.Interaction, name: str): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Roast {name} in a funny and light-hearted way."}] ) roast_text = response.choices[0].message.content await interaction.followup.send(roast_text) except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

/joke command

@bot.tree.command(name="joke", description="Tell a joke") async def joke(interaction: discord.Interaction): await interaction.response.defer() try: response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Tell me a funny joke."}] ) joke_text = response.choices[0].message.content await interaction.followup.send(joke_text) except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

bot.run(discord_token)

