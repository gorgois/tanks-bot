import discord
from discord.ext import commands
from keep_alive import keep_alive  # Optional for Render hosting

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
    msg = await ctx.respond("✅ React to **this message** with your emoji!")
    msg_obj = await msg.original_response()

    def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg_obj.id

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        emoji = reaction.emoji

        # Check if it's a custom emoji
        if isinstance(emoji, discord.Emoji):
            embed = discord.Embed(title="Emoji Info", color=discord.Color.blurple())
            embed.add_field(name="Name", value=emoji.name, inline=True)
            embed.add_field(name="ID", value=emoji.id, inline=True)
            embed.add_field(name="Animated", value=str(emoji.animated), inline=True)
            embed.set_thumbnail(url=emoji.url)
        else:
            embed = discord.Embed(title="Emoji Info", description="This is a standard emoji (Unicode)", color=discord.Color.green())
            embed.add_field(name="Emoji", value=emoji)

        await ctx.send_followup(embed=embed)

    except TimeoutError:
        await ctx.send_followup("⏰ You didn't react in time!")

keep_alive()
bot.run("YOUR_BOT_TOKEN")