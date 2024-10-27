from discord.ext import commands
from discord import Message


from utils import check_level, reset_profile


class RequestHandler(commands.Cog):
    """Cog that handles leveling events for users."""

    def __init__(self, bot):
        """Initialize the LevelEvents cog.

        :param bot: The bot instance that this cog belongs to.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Listener that processes incoming messages, running associated functions"""

        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        username = str(message.author)

        response = check_level(username, len(message_content))
        if response is not None:
            await message.channel.send(response)

        # Only proceed with commands if "wobble" is in the message
        if "wobble" not in message_content:
            return
        print("Wobble was called!")

        # Check for "flip coin" in message
        if "flip" in message_content and "coin" in message_content:
            util_command = self.bot.get_cog("UtilCommands")
            if util_command is not None:
                await message.channel.send(await util_command.flip_coin_command(None))

        if "reset me" in message_content or "!resetprofile" in message_content:
            await message.channel.send(reset_profile(username))



async def setup(bot):
    """Set up the LevelEvents cog.

    This function adds the LevelEvents cog to the provided bot instance.

    :param bot: The bot instance to which the cog will be added.
    """
    await bot.add_cog(RequestHandler(bot))