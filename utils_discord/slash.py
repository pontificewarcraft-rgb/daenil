"""
Slash command management utilities.

This module provides helper coroutines to clear and load slash command
extensions, as well as synchronize them with a specific guild.
"""

from typing import List

import discord
from discord import app_commands

from .guild import get_guild
from .logs import backlog


# List of extension paths containing slash command definitions.
SLASH_EXTENSIONS: List[str] = [
    "commands.miscellaneous.ping",
]


async def clear(bot: discord.Client) -> None:
    """
    Synchronize (clear) slash commands for the configured guild.

    This function triggers a sync operation against the specified guild.
    Note: Discord does not provide a direct "delete all" command via sync;
    this relies on the current state of the command tree.
    """
    guild = get_guild(bot)
    if guild is None:
        await backlog(bot, "❌ Guild not found. Cannot clear slash commands.")
        return

    # Create a temporary CommandTree to force a sync operation.
    # This mirrors the original intent without altering behavior.
    await app_commands.CommandTree(bot).sync(guild=guild)

    await backlog(bot, "✅ Slash command sync completed.")


async def load_extensions(bot: discord.Client) -> None:
    """
    Load configured slash command extensions and synchronize them.

    Each extension is loaded sequentially. After loading, commands are
    copied to the target guild for immediate availability and synced.
    """
    # Load extensions one by one for controlled error handling.
    for extension in SLASH_EXTENSIONS:
        try:
            await bot.load_extension(extension)
            command_name = extension.split(".")[-1]
            await backlog(
                bot,
                f"✅ {command_name} command loaded successfully!",
            )
        except Exception as exc:
            # Log extension load failure but continue attempting others.
            await backlog(
                bot,
                f"❌ Failed to load extension '{extension}': {exc}",
                trace=True,
            )

    try:
        guild = get_guild(bot)
        if guild is None:
            await backlog(bot, "❌ Guild not found. Cannot sync commands.")
            return

        # Copy global commands to the guild for near-instant propagation.
        # This avoids the typical global command propagation delay.
        bot.tree.copy_global_to(guild=guild)

        synced_commands = await bot.tree.sync(guild=guild)

        await backlog(
            bot,
            f"✅ Synced {len(synced_commands)} slash command(s)!",
        )
    except Exception as exc:
        # Broad exception catch ensures operational visibility via backlog.
        await backlog(bot, f"Sync error: {exc}", trace=True)
