"""
Discord presence management utility.

This module provides a helper coroutine to set the bot's presence
status with a custom activity and log its online status.
"""

import discord
from typing import Optional

from utils_discord.logs import backlog


async def set_presence(
    bot: discord.Client,
    activity_type: str = "On-duty Patrol",
) -> None:
    """
    Set the bot's presence activity and log its online status.

    Args:
        bot: An initialized ``discord.Client`` instance.
        activity_type: The activity/game name to display as the bot's status.

    Returns:
        None.
    """
    if bot is None:
        raise ValueError("A valid 'bot' instance is required.")

    # Notify backlog that the bot is online.
    await backlog(bot, "I am online!")

    # Update Discord presence with a Game activity.
    await bot.change_presence(activity=discord.Game(name=activity_type))
