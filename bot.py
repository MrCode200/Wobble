import logging
import os
from dotenv import load_dotenv
import atexit

from discord.ext import commands
from discord import Intents

from data import close
from cst_logger import setup_logger

# Load Discord Bot Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


setup_logger(logging.DEBUG, 'logs/bot.jsonl', log_in_json=True, stream_in_color=True)
logger = logging.getLogger('wobble.bot')

# Bot Setup
intents = Intents.default()
intents.message_content = True  # NOQA
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Handling the startup
@bot.event
async def on_ready():
    logger.info(f'{bot.user} is now running!')
    await bot.tree.sync()


# Load Cogs
async def setup():
    await bot.load_extension('events.member_events')
    await bot.load_extension('events.request_manager')

    await bot.load_extension('cogs.admin.anti_change_commands')

    await bot.load_extension('cogs.user.fun_commands')
    await bot.load_extension('cogs.user.util_commands')
    await bot.load_extension('cogs.user.info_commands')
    await bot.load_extension('cogs.user.wobble_commands')

    await bot.load_extension('cogs.developer.base_commands')
    logger.debug('Loaded all cogs')


async def main():
    await setup()
    # start the bot using its async start, under context manager
    async with bot:
        await bot.start(TOKEN)

def on_exit():
    logger.info('Shutting down wobble...')
    close()

atexit.register(on_exit)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

