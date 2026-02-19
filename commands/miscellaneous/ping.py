"""Discord bot extension for a simple ping command."""

import discord

from discord import app_commands
from discord.ext import commands


class PingCog(commands.Cog):
    """Cog for handling the ping command."""

    def __init__(self, bot: commands.Bot) -> None:
        """
        Initialize the PingCog.

        Args:
            bot: The Discord bot instance.
        """
        self.bot = bot

    @app_commands.command(name="ping", description="Verify the Service's response time.")
    async def ping(self, interaction: discord.Interaction) -> None:
        """
        Respond to the ping command with a pong message.

        Args:
            interaction: The interaction context from the command invocation.
        """
        await interaction.response.send_message("Pong! 🏓 Ranger Daenil is on duty!")


async def setup(bot: commands.Bot) -> None:
    """
    Set up the extension by adding the PingCog to the bot.

    Args:
        bot: The Discord bot instance to add the cog to.
    """
    await bot.add_cog(PingCog(bot))