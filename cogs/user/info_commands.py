from discord.ext import commands

from data import fetch_user_xp_and_lvl


class InfoCommands(commands.Cog):
    """Cog that contains commands related to user profile information."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='showprofile', help='Provides information your profile')
    async def show_profile_command(self, ctx):
        """Command to show the user's profile information.

        This command retrieves the user's XP and level from the database
        and sends a message with that information. If the user is not
        found in the database, it sends a debug message.

        :param ctx: The context in which a command is invoked. This includes
                    information about the message, the channel, and the author.
        """

        data = fetch_user_xp_and_lvl(str(ctx.author))

        if data[0] is None:
            await ctx.send(f"DEBUG: {ctx.author} is not in database")
        else:
            await ctx.send(f"{ctx.author} has {data[0]}xp and is Level {data[1]}")


async def setup(bot):
    await bot.add_cog(InfoCommands(bot))

