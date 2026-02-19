"""
Guild retrieval utilities for Discord bots.

This module provides synchronous and asynchronous helpers to retrieve a
`discord.Guild` instance either from the local cache or, optionally,
from the Discord API.
"""

from typing import Optional

import discord

import constants
from .logs import backlog


def get_guild(
    bot: discord.Client,
    guild_id: int = constants.LOTQD_ID,
) -> Optional[discord.Guild]:
    """
    Retrieve a guild from the client's cache (no API call).

    Args:
        bot: An initialized ``discord.Client`` instance.
        guild_id: The unique identifier of the guild.

    Returns:
        The cached ``discord.Guild`` if found; otherwise ``None``.

    Raises:
        ValueError: If ``bot`` is not provided.
    """
    if bot is None:
        raise ValueError("A valid 'bot' instance is required.")

    guild = bot.get_guild(guild_id)

    if guild is None:
        # Cache-only lookup; no network request is performed here.
        print(f"Guild with ID {guild_id} not found in cache (sync lookup).")

    return guild


async def get_guild_async(
    bot: discord.Client,
    guild_id: int = constants.LOTQD_ID,
    fetch_if_missing: bool = True,
) -> Optional[discord.Guild]:
    """
    Retrieve a guild from cache, optionally falling back to an API fetch.

    The function first checks the local cache (fast path). If the guild
    is not present and ``fetch_if_missing`` is True, it attempts to fetch
    the guild from the Discord API.

    Args:
        bot: An initialized ``discord.Client`` instance.
        guild_id: The unique identifier of the guild.
        fetch_if_missing: Whether to perform an API call if the guild
            is not found in cache.

    Returns:
        The ``discord.Guild`` instance if found or fetched successfully;
        otherwise ``None``.

    Raises:
        ValueError: If ``bot`` is not provided.
    """
    if bot is None:
        raise ValueError("A valid 'bot' instance is required.")

    # Fast path: attempt cache lookup first (no network I/O).
    guild = bot.get_guild(guild_id)
    if guild is not None:
        return guild

    if not fetch_if_missing:
        # Explicitly avoid API call if disabled by caller.
        print(
            f"Guild with ID {guild_id} not found in cache "
            "(async lookup, fetch disabled)."
        )
        return None

    # Slow path: fetch from Discord API.
    try:
        return await bot.fetch_guild(guild_id)
    except (discord.NotFound, discord.Forbidden):
        # NotFound: Guild does not exist or bot is not in it.
        # Forbidden: Bot lacks permission to access the guild.
        await backlog(
            bot,
            (
                f"Guild with ID {guild_id} not found or inaccessible "
                "(API fetch)."
            ),
        )
    except discord.HTTPException as exc:
        # Generic HTTP failure (e.g., network issues, rate limits).
        await backlog(
            bot,
            f"Failed to fetch guild {guild_id}: {exc}",
        )

    return None