import logging
from datetime import datetime, time as dt_time
from typing import Optional

from discord.ext import commands, tasks
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
        # Map user_id to Loop objects
        self.prayer_loops: dict[int, tasks.Loop] = {}

    @commands.hybrid_command(
        name='pray',
        help='Schedule or cancel daily prayers to a god in a specific channel',
        usage='<enable: True/False> <@god> <#channel> <hours> [minutes=0] [message]')
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

        # Cancel existing loop if present
        existing = self.prayer_loops.get(ctx.author.id)
        if existing and existing.is_running():
            existing.cancel()
            logger.info(f"Cancelled existing prayer loop for {ctx.author}.")
            del self.prayer_loops[ctx.author.id]

        if not enable:
            await ctx.send("Your prayer was cancelled.", ephemeral=True)
            return

        # Define prayer send function
        async def send_prayer() -> None:
            try:
                logger.debug(f"Sending prayer to {god.name} in {temple.name}.")
                if message:
                    await temple.send(message)
                elif god.name == GOD_MATHE501:
                    await temple.send(f"Heil {god.mention}, the GOD of `Falschgeld` `(/≧▽≦)/`")
                elif god.name == GOD_SNOWSTAR2731:
                    await temple.send(f"Heil {god.mention}, our beloved `GOBLIN GOD`! `(/≧▽≦)/`")
                    await temple.send("https://tenor.com/view/goblin-clash-royale-goblin-emote-sneaky-scheming-gif-1484412180542178994")
                elif god.name == GAY_BARDIA8490:
                    await temple.send(f"O Hell no i don't pray to a F*** gay person: {god.mention}, I am no IDIOT `( ͠° ͟ʖ ͡°))`")
                    await temple.send("https://cdn.discordapp.com/attachments/1299715274433499219/1301609665179684914/GayDGayGIF_2.gif?ex=672519f6&is=6723c876&hm=db30cda576a39f35cf0359afdc0fb71b3a25fdc697d3d67f1231d8dd58298e05&")
                    await temple.send("You look too gay that my eyes burn, F***!")
                else:
                    await temple.send(f"Pray to {god.mention}, our beloved God! `(/≧▽≦)/`")
            except Exception as e:
                logger.error(f"Error sending prayer: {e}", exc_info=True)

        # Schedule loop at specific time daily
        target_time = dt_time(hour=hours, minute=minutes)
        loop = tasks.Loop(send_prayer, time=[target_time])
        loop.before_loop(self.bot.wait_until_ready)
        loop.start()

        # Store loop
        self.prayer_loops[ctx.author.id] = loop

        await ctx.send(
            f"Daily prayer scheduled for {hours:02d}:{minutes:02d} to {god.display_name} in {temple.mention}!",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(FunCommands(bot))
