import discord.ext.commands
from discord.ext import commands


class Converter(discord.ext.commands.Converter):
    """
    This converts the argument
    """
    async def convert(self, ctx, argument):
        return f"{ctx.author} said: {argument}!"


class BaseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(
            name = "template", # Name of the command when calling it in discord
            aliases = ["temp", "temp_command"], # This function also gets called when the aliases are used
            help = "This is help : template_command", # This gets called when using <prefix>help <command> under <command>
            description = "This is description : template_command", # This gets called when using <prefix>help <command> above <command>
            brief = "This is brief : template_command", # This gets called when using <prefix>help
            enabled = True, # This disables the command when set to False
            hidden = False) # Hides the descriptions in <prefix>help when set to True
    async def template_command(self, ctx, first_arg : Converter, second_arg = "NoArgumentPassed"):
        """This will be overriden in the help variable in the decorator above"""

        await ctx.send("This is a example text, You can use all Formats: **Bold** - *Italic* - ~~Stroke?~~ - SideBarOption? - `codeblock` - ||hidden|| \n"
                        f"This is the first arg converted via `Converter` class: `{first_arg}` \n"
                        f"This is the first arg + second arg: `{first_arg}` + `{second_arg}`\n"
                        f"To use `ctx.author.arg` where arg is insideDoc: https://discordpy.readthedocs.io/en/stable/api.html#clientuser")
        await ctx.author.send(f"This is a DM msg")

    @template_command.error
    async def template_command_error(self, ctx, error):
        """Catches Errors"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument: `first_arg` is required.")
        else:
            await ctx.send("An unknown error was caught: " + str(error))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listener that processes incoming messages, running associated functions"""
        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        base_commands = self.bot.get_cog("BaseCommands")

        if message_content.startswith("temp"):
            ctx = await self.bot.get_context(message) #turns the message into a context

            await base_commands.template_command(ctx, "called by" "listener on_message")

    """@template_command.command(name="mul_args")
    async def template_multiple_args(self, ctx, *all_args):
        rest_args_joined = " ".join(all_args)
        await ctx.send(f"This is the rest of the args via `" f".join(rest_args)`: {rest_args_joined}")"""

async def setup(bot):
    await bot.add_cog(BaseCommands(bot))