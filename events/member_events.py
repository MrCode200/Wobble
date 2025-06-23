from discord.ext import commands
from discord import Member, TextChannel
from random import choice
import logging

logger = logging.getLogger(__name__)

class MemberEvents(commands.Cog):
    """Cog that handles member events such as joining and leaving."""

    def __init__(self, bot: commands.Bot):
        """Initializes the MemberEvents Cog.

        :param bot: The bot instance to which this cog belongs.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """Handles the event when a member joins the server.

        Sends a welcome message to the system channel if available.
        """
        channel: TextChannel | None = member.guild.system_channel

        if channel and channel.permissions_for(member.guild.me).send_messages:
            welcome_message = choice([
                f"`Wobble` freut sich, dass du gejoined bist, {member.mention} ||（￣︶￣）↗||",
                f"hALlO {member.mention} ||(❁´◡`❁)||",
                f"Nice t0 sEe U joIn {member.mention} ||(≧∇≦)ﾉ||"
            ])
            await channel.send(welcome_message)
        else:
            logger.warning(f"System channel not available or insufficient permissions in {member.guild.name}.")

        logger.info(f"Member joined: {member} | Welcome message attempted.",
                    extra={'command': 'on_member_join',
                           'guild': str(member.guild)})

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        """Handles the event when a member leaves the server.

        Sends a farewell message to the system channel if available.
        """
        channel: TextChannel | None = member.guild.system_channel

        if channel and channel.permissions_for(member.guild.me).send_messages:
            farewell_message = "Wobbly hätte nie gedacht, dass einer ihn mal verlässt ||（；´д｀）ゞ||"
            await channel.send(farewell_message)
        else:
            logger.warning(f"System channel not available or insufficient permissions in {member.guild.name}.")

        logger.info(f"Member left: {member} | Farewell message attempted.",
                    extra={'command': 'on_member_remove',
                           'guild': str(member.guild)})
