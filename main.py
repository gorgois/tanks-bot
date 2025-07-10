import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="reactid", description="React to get emoji ID")
async def reactid(ctx: discord.ApplicationContext):
    await ctx.respond("✅ React to **this message** with your emoji!")
    msg_obj = await ctx.original_message()

    def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg_obj.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        emoji = reaction.emoji

        if isinstance(emoji, discord.Emoji):  # custom emoji
            embed = discord.Embed(title="Emoji Info", color=discord.Color.blurple())
            embed.add_field(name="Name", value=emoji.name, inline=True)
            embed.add_field(name="ID", value=emoji.id, inline=True)
            embed.add_field(name="Animated", value=str(emoji.animated), inline=True)
            embed.set_thumbnail(url=emoji.url)
        else:  # standard unicode emoji
            embed = discord.Embed(title="Emoji Info", description="This is a standard emoji (Unicode)", color=discord.Color.green())
            embed.add_field(name="Emoji", value=emoji)

        await ctx.send_followup(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send_followup("⏰ You didn't react in time!")

# Optionally keep_alive() here if you want a web server to ping
# keep_alive()

bot.run(os.getenv("DISCORD_BOT_TOKEN"))