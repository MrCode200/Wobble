import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from discord.ext import commands
from discord import Member, TextChannel

logger = logging.getLogger('wobble.bot')

# Constants for god names for special prayers
GOD_MATHE501 = "mathe501"
GOD_SNOWSTAR2731 = "snowstar2731"
GAY_BARDIA8490 = "bardia.8490"


class FunCommands(commands.Cog):
    """A Cog containing fun commands for interacting with deities.

    This Cog allows users to schedule or cancel daily prayers to specified gods
    at a designated time and sends messages in the corresponding temple channel.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # Map user_id to Task objects
        self.prayer_tasks: dict[int, asyncio.Task] = {}

    @commands.hybrid_command(
        name='pray',
        help='Schedule or cancel daily prayers to a god in a specific channel',
        usage='<enable: True/False> <@god> <#channel> <hours> [minutes=0] [message]'
    )
    async def pray_command(
        self,
        ctx: commands.Context,
        enable: bool,
        god: Member,
        temple: TextChannel,
        hours: int,
        minutes: int = 0,
        *,
        message: Optional[str] = None
    ) -> None:
        # Validate time
        if not (0 <= hours <= 23):
            await ctx.send("❌ Hours must be between 0 and 23.", ephemeral=True)
            return
        if not (0 <= minutes <= 59):
            await ctx.send("❌ Minutes must be between 0 and 59.", ephemeral=True)
        # Validate channel
        if not temple or not temple.permissions_for(ctx.me).send_messages:
            await ctx.send(f"❌ I can't send messages in {temple.mention}.", ephemeral=True)
            return

        # Cancel existing task if present
        existing = self.prayer_tasks.get(ctx.author.id)
        if existing and not existing.done():
            existing.cancel()
            logger.info(f"Cancelled existing prayer task for {ctx.author}.")
            del self.prayer_tasks[ctx.author.id]
            if not enable:
                await ctx.send(
                    "Your prayer was cancelled, I am sure the god is not happy about that `╚(*⌂*)╝`",
                    ephemeral=True
                )
                return
        elif not enable:
            await ctx.send(
                "No prayer task was scheduled. How could you not believe in **GOD** `(っ °Д °;)っ`?!",
                ephemeral=True
            )
            return

        # Define the actual message-sending logic
        async def send_prayer() -> None:
            try:
                if message:
                    await temple.send(message)
                elif god.name == GOD_MATHE501:
                    await temple.send(f"Heil {god.mention}, the GOD of `Falschgeld` `(/≧▽≦)/`")
                elif god.name == GOD_SNOWSTAR2731:
                    await temple.send(f"Heil {god.mention}, our beloved `GOBLIN GOD`! `(/≧▽≦)/`")
                    await temple.send(
                        "https://tenor.com/view/goblin-clash-royale-goblin-emote-sneaky-scheming-gif-1484412180542178994"
                    )
                elif god.name == GAY_BARDIA8490:
                    await temple.send(
                        f"O Hell no i don't pray to a F*** gay person: {god.mention}, I am no IDIOT `( ͠° ͟ʖ ͡°))`"
                    )
                    await temple.send(
                        "https://cdn.discordapp.com/attachments/1299715274433499219/1301609665179684914/GayDGayGIF_2.gif?ex=672519f6&is=6723c876&hm=db30cda576a39f35cf0359afdc0fb71b3a25fdc697d3d67f1231d8dd58298e05&"
                    )
                    await temple.send("You look too gay that my eyes burn, F***!")
                else:
                    await temple.send(f"Pray to {god.mention}, our beloved God! `(/≧▽≦)/`")
            except Exception as e:
                logger.error(f"Error sending prayer: {e}", exc_info=True)

        # Background task to wait until the next target time and repeat every 24h
        async def prayer_task() -> None:
            # Ensure the bot is ready
            await self.bot.wait_until_ready()
            while True:
                # Compute timezone offset between local and UTC
                now_local = datetime.now()
                now_utc = datetime.utcnow()
                offset = now_local - now_utc
                # Desired next prayer in local time
                target_local = now_local.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                if target_local <= now_local:
                    target_local += timedelta(days=1)
                # Convert to UTC for sleep calculation
                target_utc = target_local - offset
                delay = (target_utc - now_utc).total_seconds()
                now = datetime.now()
                target = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                if target <= now:
                    target += timedelta(days=1)
                delay = (target - now).total_seconds()
                logger.debug(f"Prayer for {ctx.author} sleeping {delay} seconds until {target}.")
                await asyncio.sleep(delay)
                await send_prayer()
                # Next prayer in 24h
                await asyncio.sleep(24 * 3600)

        # Capture author for callback
        author = ctx.author
        # Schedule the background prayer task
        task = asyncio.create_task(prayer_task(), name=f"prayer_{author.id}")
        def _on_done(t: asyncio.Task) -> None:
            if t.cancelled():
                logger.info(f"Prayer task for {author} was cancelled.")
            else:
                err = t.exception()
                if err:
                    logger.error(f"Prayer task for {author} terminated: {err}", exc_info=True)
        task.add_done_callback(_on_done)
        self.prayer_tasks[author.id] = task

        await ctx.send(
            f"Daily prayer scheduled at `{hours} hour(s)` and `{minutes} minute(s)` to `{god.display_name}` in the temple `{temple.name}`! 🛕(‾◡◝)",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCommands(bot))
