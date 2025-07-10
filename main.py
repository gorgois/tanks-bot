import discord
from discord.ext import commands
import asyncio
import os
from keep_alive import keep_alive  # Optional

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # this is for slash commands

@bot.event
async def on_ready():
    await tree.sync()  # Sync slash commands when bot starts
    print(f"Logged in as {bot.user}")

@tree.command(name="reactid", description="React to get emoji ID")
async def reactid(interaction: discord.Interaction):
    await interaction.response.send_message("✅ React to **this message** with your emoji!", ephemeral=False)
    msg = await interaction.original_response()

    def check(reaction, user):
        return user.id == interaction.user.id and reaction.message.id == msg.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        emoji = reaction.emoji

        if isinstance(emoji, discord.Emoji):
            embed = discord.Embed(title="Emoji Info", color=discord.Color.blurple())
            embed.add_field(name="Name", value=emoji.name, inline=True)
            embed.add_field(name="ID", value=emoji.id, inline=True)
            embed.add_field(name="Animated", value=str(emoji.animated), inline=True)
            embed.set_thumbnail(url=emoji.url)
        else:
            embed = discord.Embed(title="Emoji Info", description="This is a standard emoji (Unicode)", color=discord.Color.green())
            embed.add_field(name="Emoji", value=emoji)

        await interaction.followup.send(embed=embed)

    except asyncio.TimeoutError:
        await interaction.followup.send("⏰ You didn't react in time!")

# Run the bot
keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))