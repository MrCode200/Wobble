import asyncio
from datetime import datetime, timedelta

from discord.ext import commands

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pray_to_falschgeld', help='Daily tribute to God Falschgeld', hidden=True)
    async def pray_to_falschgeld_command(self, ctx, pray: bool = False, hours: int = 9, minutes: int = 0):
        """pray to falschgeld"""
        async def send_prayer():
            await ctx.send("Heil @Mathe, the Boss of Falschgeld!")

        async def prayer_task():
            while pray:
                # Calculate the time until the next target time
                now = datetime.now()
                target_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)

                # If the target time has already passed today, schedule it for the next day
                if target_time <= now:
                    target_time += timedelta(days=1)

                delay = (target_time - now).total_seconds()

                # Wait until the target time
                await asyncio.sleep(delay)

                # Send the prayer message
                await send_prayer()


        # Create a background task for the prayer loop
        if pray:
            asyncio.create_task(prayer_task())
            await ctx.send(f"Daily prayer scheduled at {hours}:{minutes}!", ephemeral=True)
        else:
            await ctx.send("Prayer not scheduled. Set `pray=True` to activate.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCommands(bot))