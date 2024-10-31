from discord.ext import commands
from discord import Message


from utils import check_level, reset_profile


class RequestHandler(commands.Cog):
    """Cog that handles leveling events for users."""

    def __init__(self, bot: commands.Bot):
        """Initialize the LevelEvents cog.

        :param bot: The bot instance that this cog belongs to.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """
        Listener that processes incoming messages, running associated functions only if the message contains str 'wobble'.
        Function which are checked for are:

        - "wobble" in message
        - "flip coin" in message
        - "reset me" in message

        :param message: The message object that was sent.
        """

        if message.author == self.bot.user:
            return

        ctx = await self.bot.get_context(message)
        message_content = message.content.lower()
        username = str(message.author)

        response = check_level(username, len(message_content))
        if response is not None:
            await message.channel.send(response)

        # Only proceed with commands if "wobble" is in the message
        if "wobble" not in message_content:
            return

        util_commands = self.bot.get_cog("UtilCommands")

        # Check for "flip coin" in message
        if "flip" in message_content and "coin" in message_content:
            if util_commands is not None:
                await util_commands.flip_coin_command(ctx)

        if "reset me" in message_content:
            if util_commands is not None:
                await message.channel.send(await reset_profile(username))



async def setup(bot: commands.Bot):
    await bot.add_cog(RequestHandler(bot))
