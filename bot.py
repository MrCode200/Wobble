import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents

# Load Discord Bot Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Bot Setup
intents = Intents.default()
intents.message_content = True  # NOQA
bot = commands.Bot(command_prefix='!', intents=intents)


# Handling the startup
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


# Load Cogs
async def setup():
    await bot.load_extension('events.member_events')
    await bot.load_extension('cogs.user.info_commands')
    await bot.load_extension('cogs.user.wobble_commands')


# Main Entry Point
async def main():
    await setup()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    bot.run(TOKEN)
