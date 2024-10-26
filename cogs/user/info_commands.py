from discord.ext import commands

class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='showprofile', help='Provides information your profile')
    async def help_command(self, ctx):
        await ctx.send(f"{ctx.author} is level one")


async def setup(bot):
    await bot.add_cog(InfoCommands(bot))

