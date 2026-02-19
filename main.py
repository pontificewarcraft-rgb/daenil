"""
Main entry point for the Discord bot.

Initializes the bot client, sets up intents, registers events,
loads slash commands, sets presence, and starts the bot.
"""

import discord

from discord.ext import commands

from utils_discord.logs import backlog
from utils_discord.guild import get_guild
from utils_discord.slash import load_extensions
from utils_discord.presence import set_presence
from utils_discord.start import run

# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable reading message content

# Instantiate the bot client
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    """
    Event handler triggered when the bot is ready.

    Sets the bot's presence and loads all configured slash command
    extensions.
    """
    try:
        await set_presence(bot)
        await load_extensions(bot)
        await backlog(bot, "✅ Fully ready!")

    except Exception as exc:
        # Catch-all to log any unexpected errors during startup.
        await backlog(bot, f"⚠️ Error during on_ready: {exc}", trace=True)

if __name__ == "__main__":
    # Start the bot using the provided run utility
    run(bot)
