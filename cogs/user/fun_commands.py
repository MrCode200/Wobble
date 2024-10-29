import asyncio
from datetime import datetime, timedelta

from discord.ext import commands
from discord import Member
from discord import TextChannel

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prayer_tasks  = {}

    @commands.hybrid_command(name='pray', help='Daily tribute to your God', hidden=True)
    async def pray_command(self, ctx, pray: bool, god : Member, temple: TextChannel, hours: int, minutes: int = 0):
        """Pray to Falschgeld daily at a specified time."""

        async def send_prayer():
            if god.name == "mathe501":
                await temple.send("Heil {god.mention}, the GOD of Falschgeld `(/≧▽≦)/`")
            if god.name == "snowstar2731":
                await temple.send("Heil {god.mention}, our beloved `GOBLIN GOD`! `(/≧▽≦)/`")
                await temple.send("https://tenor.com/view/goblin-clash-royale-goblin-emote-sneaky-scheming-gif-1484412180542178994")

        async def prayer_task():
            while True:
                now = datetime.now()
                target_time = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
                if target_time <= now:
                    target_time += timedelta(days=1)
                delay = (target_time - now).total_seconds()
                await asyncio.sleep(delay)
                await send_prayer()


        if pray:
            if ctx.author.id in self.prayer_tasks:
                self.prayer_tasks[ctx.author.id].cancel()
            task = asyncio.create_task(prayer_task())
            self.prayer_tasks[ctx.author.id] = task
            await ctx.send(f"Daily prayer scheduled at `{hours} hour(s)` and `{minutes} minute(s)` to {god.display_name} in the temple {temple.name}! `🛕(‾◡◝)`", ephemeral=True)
        else:
            if ctx.author.id in self.prayer_tasks:
                self.prayer_tasks[ctx.author.id].cancel()
                del self.prayer_tasks[ctx.author.id]
                await ctx.send("Your prayer was cancelled, i am sure the god is not happy about that `╚(*⌂*)╝`", ephemeral=True)
            else:
                await ctx.send("No prayer task was scheduled. How could you not believe in **GOD** `(っ °Д °;)っ`?!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(FunCommands(bot))