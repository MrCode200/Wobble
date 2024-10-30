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
        name="template",
        aliases=["temp", "temp_command"],
        help="This is help: template_command",
        description="This is description: template_command",
        brief="This is brief: template_command",
        enabled=True,
        hidden=False
    )
    async def template_command(self, ctx, first_arg: Converter, second_arg: str = "NoArgumentPassed"):
        """Main command within the template group."""
        await ctx.send(
            "This is an example text. You can use all Formats: **Bold** - *Italic* - ~~Stroke~~ - SideBarOption - "
            "`codeblock` - ||hidden|| \n"
            f"This is the first arg converted via `Converter` class: `{first_arg}` \n"
            f"This is the first arg + second arg: `{first_arg}` + `{second_arg}`\n"
            f"For more details on `ctx.author.arg`, see the docs: https://discordpy.readthedocs.io/en/stable/api.html#clientuser"
        )
        await ctx.author.send("This is a DM message")

    @template_command.command(name="subcommand")
    async def template_sub_command(self, ctx, args1: str = None):
        """Subcommand to handle multiple arguments."""
        await ctx.send(f"and this is a subcommand, it only runs with template mul_args")

    @commands.command(name="mul_args")
    async def template_multiple_args_command(self, ctx, *all_args):
        """Subcommand to handle multiple arguments."""
        rest_args_joined = "` `".join(all_args)

        await ctx.send(f"This is the rest of the args: `{rest_args_joined}`. This cant be a hybrid_command!")

    @template_command.error
    async def template_command_error(self, ctx, error):
        """Handles errors for the `template` command group."""
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


async def setup(bot):
    await bot.add_cog(BaseCommands(bot))