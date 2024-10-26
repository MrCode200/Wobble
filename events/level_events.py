from abc import abstractmethod
from discord.ext import commands
from discord import Message

from data import add_or_update_user_xp_and_lvl, fetch_user_xp_and_lvl


class LevelEvents(commands.Cog):
    """Cog that handles leveling events for users."""

    def __init__(self, bot):
        """Initialize the LevelEvents cog.

        :param bot: The bot instance that this cog belongs to.
        """
        self.bot = bot

    @staticmethod
    def calculate_lvl(level: int, xp: int) -> int:
        """Calculate the level based on experience points.

        This method calculates the XP required for the next level based
        on the current level and returns the new level if the user has
        enough XP to level up.

        :param level: The current level of the user.
        :param xp: The current experience points of the user.
        :return: The new level after considering the current XP.
        """
        base_xp = 100
        growth_factor = 1.5

        xp_for_next_level = int(base_xp * (level ** growth_factor))

        if xp >= xp_for_next_level:
            return level + 1
        return level

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Listener that processes incoming messages for XP updates.

        This method checks if the message author is not the bot itself,
        retrieves user XP and level, calculates the updated XP and level,
        and updates the database accordingly. If the user levels up,
        a congratulatory message is sent.

        :param message: The message object containing the message data.
        """
        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        username = str(message.author)

        try:
            user_data = fetch_user_xp_and_lvl(str(message.author))

            if user_data is None:
                initial_xp = len(message_content)
                add_or_update_user_xp_and_lvl(username, 0, 1)
                await message.channel.send(f"Welcome {username}! You are reborn in this new World (〃￣︶￣)人(￣︶￣〃)")
                return

            updated_level = LevelEvents.calculate_lvl(user_data[1], user_data[0] + len(message_content))

            add_or_update_user_xp_and_lvl(username, user_data[0] + len(message_content), updated_level)

            if updated_level > user_data[1]:
                await message.channel.send(
                    f"CONGRATS🎉, Wobble is happy to announce that you LEVELD up to Level {updated_level} o(*^＠^*)o! ")
        except Exception as e:
            print(e)


async def setup(bot):
    """Set up the LevelEvents cog.

    This function adds the LevelEvents cog to the provided bot instance.

    :param bot: The bot instance to which the cog will be added.
    """
    await bot.add_cog(LevelEvents(bot))
