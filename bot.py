import os
from dotenv import load_dotenv
import atexit

from discord.ext import commands
from discord import Intents

from data import close

# Load Discord Bot Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Bot Setup
intents = Intents.default()
intents.message_content = True  # NOQA
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Handling the startup
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

    await bot.tree.sync()


# Load Cogs
async def setup():
    await bot.load_extension('events.member_events')
    await bot.load_extension('events.request_manager')
    await bot.load_extension('cogs.user.util_commands')
    await bot.load_extension('cogs.user.info_commands')
    await bot.load_extension('cogs.user.wobble_commands')


# Main Entry Point
async def main():
    await setup()


def on_exit():
    close()

atexit.register(on_exit)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    bot.run(TOKEN)
