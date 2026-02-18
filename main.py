import discord
from discord.ext import commands

# Set up the bot with default intents
intents = discord.Intents.default()
intents.message_content = True  # Enable if you need to read message content

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # Set the bot's status to "Playing On-duty patrol..."
    await bot.change_presence(activity=discord.Game(name="On-duty patrol..."))
    print(f'{bot.user} has connected to Discord! The bot is now online.')

# Read the token from token.txt
with open('token.txt', 'r') as f:
    token = f.read().strip()

bot.run(token)