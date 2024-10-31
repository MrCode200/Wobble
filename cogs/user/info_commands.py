from discord.ext import commands

from data import fetch_user_xp_and_lvl


class InfoCommands(commands.Cog):
    """Cog that contains commands related to user profile information."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initializes the InfoCommands Cog.

        :param bot: The bot instance to which this cog belongs.
        """
        self.bot = bot

    @commands.hybrid_command(name='showprofile', help='Provides information about your profile')
    async def show_profile_command(self, ctx: commands.Context) -> None:
        """Command to show the user's profile information.

        This command retrieves the user's XP and level from the database
        and sends a message with that information. If the user is not
        found in the database, it sends a debug message.

        :param ctx: The context in which a command is invoked. This includes
                    information about the message, the channel, and the author.
        """
        data = fetch_user_xp_and_lvl(str(ctx.author))

        if data[0] is None:
            await ctx.send(f"DEBUG: `{ctx.author}` is not in the database")
        else:
            await ctx.send(f"Wobble knows that `{ctx.author}` has `{data[0]} xp` and is `Level {data[1]}` `(。・ω・。)`")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InfoCommands(bot))
