import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive  # Only if using Render/Replit

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    # Sync slash commands with Discord
    await bot.tree.sync()

@bot.tree.command(name="reactid", description="React to get emoji info")
async def reactid(interaction: discord.Interaction):
    # Send initial message and wait to get the message object
    msg = await interaction.response.send_message(
        "✅ React to **this message** with your emoji!", wait=True
    )

    def check(reaction, user):
        return user.id == interaction.user.id and reaction.message.id == msg.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        emoji = reaction.emoji

        if isinstance(emoji, discord.Emoji):  # Custom emoji
            embed = discord.Embed(
                title="Custom Emoji Info", color=discord.Color.blurple()
            )
            embed.add_field(name="Name", value=emoji.name, inline=True)
            embed.add_field(name="ID", value=str(emoji.id), inline=True)
            embed.add_field(name="Animated", value=str(emoji.animated), inline=True)
            embed.set_thumbnail(url=emoji.url)
        else:  # Unicode emoji
            embed = discord.Embed(
                title="Standard Emoji Info", color=discord.Color.green()
            )
            embed.add_field(name="Emoji", value=emoji, inline=True)
            embed.add_field(name="Note", value="This is a standard emoji (no ID)", inline=False)

        await interaction.followup.send(embed=embed)

    except asyncio.TimeoutError:
        await interaction.followup.send("⏰ You didn't react in time!")

# Keep alive for Render/Replit (if you use it)
keep_alive()

# Put your bot token here
TOKEN = "YOUR_BOT_TOKEN"

bot.run(TOKEN)