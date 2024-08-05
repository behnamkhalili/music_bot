import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'),intents=discord.Intents.all(),activity = discord.Game(name='comming soon...'),help_command=None)
    
    async def on_ready(self):
        await self.load_cogs()
        print(f'{self.user} now connected')
    
    
    async def load_cogs(self):
        cogs = ['commands']
        for cog in cogs:
            try:
                await self.load_extension(f'cogs.{cog}')
                print(f'Loaded cog: {cog}')
            except Exception as e:
                print(f'Failed to load cog: {cog}\n\nError: {str(e)}')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = Bot()
if __name__ == "__main__":
    asyncio.run(bot.run(TOKEN))