import discord.ext.commands
from discord.ext import commands
import logging

logger = logging.getLogger('wobble.bot')


def is_developer(ctx) -> bool:
    """Check if the command invoked is from a developer of this bot.

    :param ctx: The context of the command invocation.
    :type ctx: commands.Context
    :return: True if the author of the command is the developer, otherwise False.
    :rtype: bool
    """
    return ctx.author.id == 703265159895973890


class Converter(discord.ext.commands.Converter):
    """
    Converter class for converting command arguments.

    This converter appends a message from the author to the argument provided.
    """

    async def convert(self, ctx: commands.Context, argument: str) -> str:
        """Converts the argument to a specific format.

        :param ctx: The context of the command invocation.
        :param argument: The argument passed to the command.
        :return: A formatted string including the author's mention and the argument.
        """
        return f"{ctx.author} said: {argument}!"


class BaseCommands(commands.Cog):
    """Cog for handling base commands for the bot.

    This class defines a set of commands and listeners that can be invoked
    within the Discord server. Only the designated developer can invoke these commands.
    """

    def __init__(self, bot):
        """Initializes the BaseCommands Cog.

        :param bot: The bot instance to which this cog belongs.
        :type bot: commands.Bot
        """
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
    @commands.check(is_developer)
    async def template_command(self, ctx: commands.Context, first_arg: Converter, second_arg: str = "NoArgumentPassed") -> None:
        """Main command within the template group.

        This command demonstrates various formatting options and accepts
        arguments through a custom Converter.

        :param ctx: The context of the command invocation.
        :param first_arg: The first argument converted using the Converter class.
        :param second_arg: The second argument. Defaults to "NoArgumentPassed".

        Sends a message in the current channel and a DM to the command invoker.
        """
        logger.debug(f"",
                        extra={'command': str(ctx.command.name),
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

        await ctx.send(
            "This is an example text. You can use all Formats: **Bold** - *Italic* - ~~Stroke~~ - SideBarOption - "
            "`codeblock` - ||hidden|| \n"
            f"This is the first arg converted via `Converter` class: `{first_arg}` \n"
            f"This is the first arg + second arg: `{first_arg}` + `{second_arg}`\n"
            f"For more details on `ctx.author.arg`, see the docs: https://discordpy.readthedocs.io/en/stable/api.html#clientuser"
        )
        await ctx.author.send("This is a DM message")

    @template_command.command(name="subcommand")
    @commands.check(is_developer)
    async def template_sub_command(self, ctx: commands.Context, args1: str = None) -> None:
        """Subcommand to handle multiple arguments.

        This command is a subcommand of the template command and handles
        additional arguments passed to it.

        :param ctx: The context of the command invocation.
        :param args1: An optional argument to be processed.
        """
        logger.debug(f"",
                        extra={'command': str(ctx.command.name),
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

        await ctx.send(f"and this is a subcommand, it only runs with template mul_args")

    @commands.command(name="mul_args")
    @commands.check(is_developer)
    async def template_multiple_args_command(self, ctx: commands.Context, *all_args: str) -> None:
        """Subcommand to handle multiple arguments.

        This command accepts multiple arguments and processes them accordingly.

        :param ctx: The context of the command invocation.
        :param all_args: A variable number of arguments passed to the command.
        """
        logger.debug(f"",
                        extra={'command': str(ctx.command.name),
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

        rest_args_joined = "` `".join(all_args)

        await ctx.send(f"This is the rest of the args: `{rest_args_joined}`. This can't be a hybrid_command!")

    @template_command.error
    @commands.check(is_developer)
    async def template_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Handles errors for the `template` command group.

        This method processes errors that occur during the invocation of
        the template command group and sends appropriate feedback to the user.

        :param ctx: The context of the command invocation.
        :param error: The error raised during command invocation.
        """
        if isinstance(error, commands.MissingRequiredArgument):
            logger.error(f"Missing required argument for command '{ctx.command.name}'.",
                        extra={'command': str(ctx.command.name),
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

            await ctx.send("Missing argument: `first_arg` is required.")
        else:
            logger.error("An unknown error was caught: " + str(error),
                        extra={'command': str(ctx.command.name),
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

            await ctx.send("An unknown error was caught: " + str(error))

    @commands.Cog.listener()
    @commands.check(is_developer)
    async def on_message(self, message: discord.Message) -> None:
        """Listener that processes incoming messages, running associated functions.

        This listener checks for messages from the user with the name 'mr.magic9'
        and processes commands if they start with 'temp'.

        :param message: The message object that was sent.
        """
        if message.author == self.bot.user or message.author.name != "mr.magic9":
            return

        message_content = message.content.lower()
        base_commands = self.bot.get_cog("BaseCommands")

        if message_content.startswith("temp"):
            ctx = await self.bot.get_context(message)  # turns the message into a context

            await base_commands.template_command(ctx, "called by listener on_message")


async def setup(bot):
    await bot.add_cog(BaseCommands(bot))
