from random import choice

from discord.ext import commands
from discord import Member


class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.bot.get_channel(1299755932636545095)
        await channel.send(choice([f"Wobbly freut sich das du gejoint bist, {member.mention}（￣︶￣）↗　",
                           f"hALlO {member.mention} (❁´◡`❁)",
                           f"Nice t0 sEe U joIn (≧∇≦)ﾉ"]))

    @commands.Cog.listener()
    async def on_member_leave(self, member: Member):
        channel = self.bot.get_channel(1299755932636545095)
        await channel.send(f"Wobbly hätte nie gedacht das einer ihn mal verlässt （；´д｀）ゞ")


async def setup(bot):
    await bot.add_cog(MemberEvents(bot))