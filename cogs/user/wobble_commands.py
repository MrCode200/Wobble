import logging

from discord.ext import commands


logger = logging.getLogger('wobble.bot')


class WobbleCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='wobble', help='Wobble?')
    async def wobble(self, ctx: commands.Context) -> None:
        """Send a playful 'Wobble' message.

        This command sends a fun message to the context where it was invoked.

        :param ctx: The context in which the command was invoked, including
                    information about the message, the channel, and the author.
        """
        logger.info("",
                    extra={'command': str(ctx.command.name),
                           'author': str(ctx.author),
                           'guild': str(ctx.guild)})

        await ctx.send("WobbLe wOBblE `＼（〇_ｏ）／`")


async def setup(bot: commands.Bot):
    await bot.add_cog(WobbleCommands(bot))