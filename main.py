import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive  # Only needed if using Render hosting

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.slash_command(name="reactid", description="React to get emoji info")
async def reactid(ctx: discord.ApplicationContext):
    # Use normal send instead of respond to avoid delay issues
    msg = await ctx.send("✅ React to **this message** with your emoji!")

    def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        print(f"✅ Reaction received: {reaction.emoji} from {user}")  # Debug print

        emoji = reaction.emoji

        if isinstance(emoji, discord.Emoji):  # Custom emoji
            embed = discord.Embed(title="Custom Emoji Info", color=discord.Color.blurple())
            embed.add_field(name="Name", value=emoji.name, inline=True)
            embed.add_field(name="ID", value=str(emoji.id), inline=True)
            embed.add_field(name="Animated", value=str(emoji.animated), inline=True)
            embed.set_thumbnail(url=emoji.url)
        else:  # Standard Unicode emoji
            embed = discord.Embed(title="Standard Emoji Info", color=discord.Color.green())
            embed.add_field(name="Emoji", value=emoji, inline=True)
            embed.add_field(name="Note", value="This is a standard emoji (no ID)", inline=False)

        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        print("❌ Timeout — user did not react in time.")
        await ctx.send("⏰ You didn't react in time!")

# Keep alive for Render
keep_alive()

# Replace with your actual bot token
bot.run("YOUR_BOT_TOKEN")