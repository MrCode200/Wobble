import random

from discord.ext import commands

from utils import reset_profile


class UtilCommands(commands.Cog):
    """Cog that contains commands related to user profile information."""
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='flipcoin', help='Flips a Coino')
    async def flip_coin_command(self, ctx):
        """Command to flip a digital coin

        :param ctx: The context in which a command is invoked. This includes
                    information about the message, the channel, and the author.
        """

        print("UtilsCommands-def flipcoincommand")

        result = "head" if random.random() > 0.5 else "tail"
        if ctx is None:
            return f"Wobble heard to flip Coin, Wobble flipped `{result}` ||(o゜▽゜)o☆||"
        await ctx.send(f"Wobble heard to flip Coin, Wobble flipped `{result}` ||(o゜▽゜)o☆||")

    @commands.hybrid_command(name='resetprofile', help="Resets your profile to level 1 and 0xp")
    async def reset_profile_command(self, ctx):
        await ctx.send(reset_profile(str(ctx.author)))


async def setup(bot):
    await bot.add_cog(UtilCommands(bot))
