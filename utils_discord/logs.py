"""
Backlog logging utility for Discord bots.

This module provides a helper coroutine to send diagnostic or logging
messages to a dedicated Discord text channel named ``backlog📟`` across
any guild the bot is connected to.
"""

import traceback
from typing import Optional

import discord
from discord.ext.commands import Bot


async def backlog(
    bot: Optional[discord.Client] = None,
    message: str = "",
    trace: bool = False,
) -> None:
    """
    Send a message to the first ``backlog📟`` text channel found across
    all guilds the bot is connected to.

    If ``trace`` is True, the current exception traceback is appended
    to the message in a formatted code block.

    Args:
        bot: An instance of ``discord.Client`` or ``commands.Bot``.
        message: The message content to send.
        trace: Whether to append the current exception traceback.

    Returns:
        None. The coroutine exits after sending the message to the first
        matching channel or after logging warnings if unsuccessful.
    """
    if trace:
        # Append the current exception traceback for debugging purposes.
        message = f"{message}\n```python\n{traceback.format_exc()}\n```"

    # Always log to stdout as a fallback for visibility.
    print(message)

    if not isinstance(bot, discord.Client):
        # Defensive check: ensures predictable behavior if an invalid
        # object is passed as the bot parameter.
        print(
            "Warning: Backlog not issued. 'bot' parameter is not a valid "
            "discord.Client instance.\n"
            f"Type found: {type(bot)};\n"
            f"Content: {bot}"
        )
        return

    for guild in bot.guilds:
        for channel in guild.text_channels:
            # Channel name comparison is exact by design to avoid
            # accidentally logging to similarly named channels.
            if channel.name == "backlog📟":
                await channel.send(message)
                return  # Stop after the first successful send.

    # If execution reaches this point, no matching channel was found.
    print("Warning: 'backlog📟' channel not found in any guild.")
