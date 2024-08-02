import os

import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv

import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)


@bot.event
async def on_ready():
    try:
        print(f'{bot.user} succesfully connected')
    except:
        print("[!] Couldn't connect, an Error occured")


@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
            await ctx.send(f"Connected to {channel}")
        except Exception as e:
            await ctx.send(f"Could not connect to voice channel: {e}")
    else:
        await ctx.send("You are not connected to a voice channel.")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Lefted the voice channel")
    else:
        await ctx.send("You have to be in a voice channel to run this command")




bot.run(TOKEN)
