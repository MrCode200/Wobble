import asyncio
import logging
from datetime import datetime, timedelta

from discord.ext import commands
from discord import Member
from discord import TextChannel

logger = logging.getLogger('wobble.bot')


# Constants for god names for special prayers
GOD_MATHE501 = "mathe501"
GOD_SNOWSTAR2731 = "snowstar2731"


class FunCommands(commands.Cog):
    """A Cog containing fun commands for interacting with deities.

    This Cog allows users to schedule daily prayers to specified gods
    at a designated time and sends messages in the corresponding temple channel.
    """

    def __init__(self, bot) -> None:
        """Initializes the FunCommands Cog.

        :param bot: The bot instance to which this cog belongs.
        :type bot: commands.Bot
        """
        self.bot = bot
        self.prayer_tasks = {}  #: A dictionary to track scheduled prayer tasks per user.

    @commands.hybrid_command(name='pray', help='Daily tribute to your God', hidden=True)
    async def pray_command(self, ctx: commands.Context, pray: bool, god: Member, temple: TextChannel, hours: int, minutes: int = 0) -> None:
        """Schedules a daily prayer to a specified god at a designated time.

        This command allows users to either schedule or cancel daily prayers.
        If scheduled, the bot will send a message to the specified temple channel
        at the chosen time.

        :param ctx: The context of the command invocation.
        :param pray: A boolean indicating whether to schedule (True) or cancel (False) the prayer.
        :param god: The member representing the god to whom the prayer is directed.
        :param temple: The text channel where the prayer message will be sent.
        :param hours: The hour (in 24-hour format) when the prayer should be sent.
        :param minutes: The minute when the prayer should be sent (default is 0).
        """
        if not (0 <= hours <= 24) or not (0 <= minutes <= 60):
            await ctx.send("Please provide a valid time. Hours should be between 0-23 and minutes between 0-59.", ephemeral=True)
            return

        async def send_prayer() -> None:
            """Sends the prayer message to the specified god in the temple channel."""
            logger.debug(f"Command '{ctx.command.name}' sends prayer to `{god.name}` in channel `{temple.name}`.")
            if god.name == GOD_MATHE501:
                await temple.send(f"Heil {god.mention}, the GOD of Falschgeld `(/≧▽≦)/`")
            if god.name == GOD_SNOWSTAR2731:
                await temple.send(f"Heil {god.mention}, our beloved `GOBLIN GOD`! `(/≧▽≦)/`")
                await temple.send("https://tenor.com/view/goblin-clash-royale-goblin-emote-sneaky-scheming-gif-1484412180542178994")

        async def prayer_task() -> None:
            """The task that waits for the scheduled prayer time and sends the prayer message."""
            while True:
                now = datetime.now()
                target_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                if target_time <= now:
                    target_time += timedelta(days=1)
                delay = (target_time - now).total_seconds()
                logger.debug(f"Sleeping for {delay} seconds till {target_time} for prayer.")
                await asyncio.sleep(delay)
                await send_prayer()

        if pray:
            if ctx.author.id in self.prayer_tasks:
                self.prayer_tasks[ctx.author.id].cancel()
                logging.debug(f"Cancelled existing prayer task for {ctx.author}.")
            task = asyncio.create_task(prayer_task())
            self.prayer_tasks[ctx.author.id] = task
            logger.info(f"Command '{ctx.command.name}' added a prayer task from {ctx.author}.")
            await ctx.send(f"Daily prayer scheduled at `{hours} hour(s)` and `{minutes} minute(s)` to {god.display_name} in the temple {temple.name}! `🛕(‾◡◝)`", ephemeral=True)
        else:
            if ctx.author.id in self.prayer_tasks:
                self.prayer_tasks[ctx.author.id].cancel()
                del self.prayer_tasks[ctx.author.id]
                logger.info(f"Command '{ctx.command.name}' removed a prayer task from {ctx.author}.")
                await ctx.send("Your prayer was cancelled, I am sure the god is not happy about that `╚(*⌂*)╝`", ephemeral=True)
            else:
                logger.warning(f"Command '{ctx.command.name}' called by `{ctx.author}` but no prayer task was scheduled.")
                await ctx.send("No prayer task was scheduled. How could you not believe in **GOD** `(っ °Д °;)っ`?!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(FunCommands(bot))
