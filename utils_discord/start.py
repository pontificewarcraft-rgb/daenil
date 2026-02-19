"""
Bot startup utility.

This module provides a simple helper to run the Discord bot using
a token stored in a local file.
"""

from discord import Client


def run(bot: Client) -> None:
    """
    Run the Discord bot using the token from 'token.txt'.

    Args:
        bot: An initialized ``discord.Client`` or ``commands.Bot`` instance.

    Raises:
        FileNotFoundError: If 'token.txt' does not exist.
        discord.LoginFailure: If the token is invalid.
    """
    try:
        with open("token.txt", "r", encoding="utf-8") as file:
            token = file.read().strip()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Token file 'token.txt' not found.") from exc

    # Start the bot with the provided token
    bot.run(token)
