from discord.ext import commands


class BaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(  
            name="template", 
            help="Creates a Template For everytype command")
    async def template_command(self, ctx):
        await ctx.send("This is a example text, You can use all Formats: **Bold** - *Italic* - ~~Stroke?~~ - SideBarOption - `codeblock` - ||hidden||")

async def setup(bot):
    await bot.add_cog(BaseCommands(bot))