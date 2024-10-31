import logging

from discord.ext import commands
from discord import Message

logger = logging.getLogger('wobble.bot')


class AntiChangeCommand(commands.Cog):
    """A Cog containing commands for moderating message deletion and edits.

    This Cog enables toggling of features that log and report when messages are
    deleted or edited by users, allowing specified users to monitor these actions.
    """

    def __init__(self, bot: commands.Bot) -> None:
        """Initializes the AntiChangeCommand Cog.

        :param bot: The bot instance to which this cog belongs.
        """
        self.bot = bot
        self.anti_delete = False  #: Tracks the anti-delete message toggle state
        self.anti_edit = False  #: Tracks the anti-edit message toggle state
        self.programmer_channel = None

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Event listener that triggers when the bot is ready.

        Fetches the channel for reporting deletions and edits.

        :raises discord.NotFound: If the channel does not exist.
        """
        self.programmer_channel = await self.bot.fetch_channel(1299715274433499219)

    @commands.hybrid_command(name="toggle_anti_del", help="Enable or disable message delete monitoring.")
    async def toggle_anti_del_command(self, ctx: commands.Context, enable: bool) -> None:
        """Toggles the anti-delete message feature.

        This command allows a specified user to enable or disable monitoring
        of deleted messages.

        :param ctx: The context of the command invocation.
        :param enable: True to enable the feature, False to disable.
        """
        if ctx.author.name == "mr.magic9" or ctx.author.id == ctx.author.owner_id or ctx.author.guild_permissions.administrator:
            self.anti_delete = enable
            logger.info(f"Anti delete message toggled {'On' if enable else 'Off'}.",
                        extra={'command': 'toggle_anti_del',
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

            await ctx.send(
                f"Anti delete message toggled `{'On' if enable else 'Off'}`! "
                f"Wobble will do its best to find all deleters `╰(*°▽°*)╯`." if enable else "Off"
            )
        else:
            await ctx.send("Wobble thinks you do not have permission to do that `┗|｀O′|┛`.", ephemeral=True)

    @commands.hybrid_command(name="toggle_anti_edit", help="Enable or disable message edit monitoring.")
    async def toggle_anti_edit_command(self, ctx: commands.Context, enable: bool) -> None:
        """Toggles the anti-edit message feature.

        This command allows a specified user to enable or disable monitoring
        of edited messages.

        :param ctx: The context of the command invocation.
        :param enable: True to enable the feature, False to disable.
        """
        if ctx.author.name == "mr.magic9" or ctx.author.id == ctx.author.owner_id or ctx.author.guild_permissions.administrator:
            self.anti_edit = enable
            logger.info(f"Anti edit message toggled {'On' if enable else 'Off'}.",
                        extra={'command': 'toggle_anti_del',
                               'author': str(ctx.author),
                               'guild': str(ctx.guild)})

            await ctx.send(
                f"Anti edit message toggled `{'On' if enable else 'Off'}`! "
                f"Wobble will do its best to find all editors `╰(*°▽°*)╯`." if enable else "Off"
            )
        else:
            await ctx.send("Wobble thinks you do not have permission to do that `┗|｀O′|┛`.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message) -> None:
        """Listener for message deletion events. Notifies if anti-delete is active.

        This method is triggered when a message is deleted, and sends a notification
        to the appropriate channel if anti-delete monitoring is enabled.

        :param message: The message object of the deleted message.
        """
        logger.debug(f"Catched message deleted: '{message.content}' by {message.author}",
                        extra={'command': 'toggle_anti_del',
                               'author': 'listener',
                               'guild': str(message.guild)})

        if self.anti_delete and message.author.id != self.bot.user.id:
            await message.channel.send(
                f"Wobble saw how `{message.author.name}` just deleted a message `(▀̿Ĺ̯▀̿ ̿)`: \nMessage: `{message.content}`"
            )
        else:
            await self.programmer_channel.send(f"Wobble saw how `{message.author.name}` just deleted a message `(▀̿Ĺ̯▀̿ ̿)`: "
                                       f"\nMessage: `{message.content}`")

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        """Listener for message edit events. Notifies if anti-edit is active.

        This method is triggered when a message is edited, and sends a notification
        to the appropriate channel if anti-edit monitoring is enabled.

        :param before: The original message content before editing.
        :param after: The message content after editing.
        """
        logger.debug(f"Catched message edited: '{before.content}' to '{after.content}' by {before.author}",
                        extra={'command': 'toggle_anti_del',
                               'author': 'listener',
                               'guild': str(before.guild)})

        if self.anti_edit and before.author.id != self.bot.user.id:
            await before.channel.send(
                f"Wobble saw how `{before.author.name}` just edited their message `(▀̿Ĺ̯▀̿ ̿)`:\n"
                f"**Before:** `{before.content}`\n**After:** `{after.content}`"
            )
        else:
            await self.programmer_channel.send(
                f"Wobble saw how `{before.author.name}` just edited their message `(▀̿Ĺ̯▀̿ ̿)`:\n"
                f"**Before:** `{before.content}`\n**After:** `{after.content}`"
            )


async def setup(bot):
    await bot.add_cog(AntiChangeCommand(bot))
