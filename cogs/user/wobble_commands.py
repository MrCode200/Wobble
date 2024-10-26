from discord.ext import commands

class WobbleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wobble', help='Wobble?')
    async def help_command(self, ctx):
        await ctx.send("WobbLe wOBblE ＼（〇_ｏ）／")


async def setup(bot):
    await bot.add_cog(WobbleCommands(bot))