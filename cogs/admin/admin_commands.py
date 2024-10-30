from discord.ext import commands


class AntiChangeCommand(commands.Cog):
    """Cog that contains commands related to user profile information."""
    def __init__(self, bot):
        self.bot = bot
        self.anti_delete = False

    @commands.hybrid_command()
    async def toggle_anti_del_msg_command(self, ctx, on: bool):
        pass

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        if not anti_delete:
            return


async def setup(bot):
    await bot.add_cog(AntiChangeCommand(bot))
