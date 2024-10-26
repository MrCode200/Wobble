from discord.ext import commands

class WobbleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wobble', help='Wobble?')
    async def wobble(self, ctx):
        """Send a playful 'Wobble' message.

        This command sends a fun message to the context where it was invoked.

        :param ctx: The context in which the command was invoked, including
                    information about the message, the channel, and the author.
        """
        await ctx.send("WobbLe wOBblE ＼（〇_ｏ）／")


async def setup(bot):
    await bot.add_cog(WobbleCommands(bot))