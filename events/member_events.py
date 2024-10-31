import logging
from discord.ext import commands
from discord import Member
from random import choice

# Configure logging
logger = logging.getLogger('wobble.bot')


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

        This method sends a welcome message to a designated channel when a new
        member joins.

        :param member: The member who has joined the server.
        """
        channel = self.bot.get_channel(1299755932636545095)
        welcome_message = choice([
            f"`Wobble` freut sich, dass du gejoined bist, @{member.mention} ||（￣︶￣）↗||",
            f"hALlO @{member.mention} ||(❁´◡`❁)||",
            f"Nice t0 sEe U joIn @{member.mention} ||(≧∇≦)ﾉ||"
        ])

        await channel.send(welcome_message)

        # Log the event
        logger.info(f"Member joined: {member} | Welcome message sent.",
                    extra={'command': 'on_member_leave',
                           'guild': str(member.guild)})

    @commands.Cog.listener()
    async def on_member_leave(self, member: Member) -> None:
        """Handles the event when a member leaves the server.

        This method sends a farewell message to a designated channel when a member
        leaves.

        :param member: The member who has left the server.
        """
        channel = self.bot.get_channel(1299755932636545095)
        farewell_message = f"Wobbly hätte nie gedacht, dass einer ihn mal verlässt ||（；´д｀）ゞ||"

        await channel.send(farewell_message)

        # Log the event
        logger.info(f"Member left: {member} | Farewell message sent.",
                    extra={'command': 'on_member_leave',
                           'guild': str(member.guild)})


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberEvents(bot))
