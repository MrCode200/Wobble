import random
import logging

from discord.ext import commands
from utils import reset_profile


logger = logging.getLogger('wobble.bot')


class UtilCommands(commands.Cog):
    """Cog that contains commands related to user utility functions."""

    def __init__(self, bot: commands.Bot):
        """Initializes the UtilCommands Cog.

        :param bot: The bot instance to which this cog belongs.
        """
        self.bot = bot

    @commands.hybrid_command(name='resetprofile', help="Resets your profile to level 1 and 0xp")
    async def reset_profile_command(self, ctx: commands.Context) -> None:
        """Resets the user's profile to level 1 and 0 XP.

        This command invokes the reset_profile function to reset the user's profile.

        :param ctx: The context in which a command is invoked. This includes
                    information about the message, the channel, and the author.
        """
        result = reset_profile(str(ctx.author))
        logger.info(f"Profile reset for Author.",
                    extra={'command': str(ctx.command.name),
                           'author': str(ctx.author),
                           'guild': str(ctx.guild)})

        await ctx.send(result)

    @commands.hybrid_command(name='flipcoin', help='Flips a digital coin')
    async def flip_coin_command(self, ctx: commands.Context) -> None:
        """Command to flip a digital coin.

        This command simulates a coin flip and returns the result to the user.

        :param ctx: The context in which a command is invoked. This includes
                    information about the message, the channel, and the author.
        """
        result = "head" if random.random() > 0.5 else "tail"
        logger.info(f"Coin flipped by: Result was `{result}`.",
                    extra={'command': 'flip_coin',
                           'author': str(ctx.author),
                           'guild': str(ctx.guild)})

        await ctx.send(f"Wobble heard to flip Coin, Wobble flipped `{result}`. `(o゜▽゜)oo`")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UtilCommands(bot))
