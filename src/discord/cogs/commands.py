import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="join")
    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):
        print('try to join')
        try:
            channel = ctx.message.author.voice.channel
        except discord.ClientException as e :
            return await ctx.send(f"Failed to join voice channel: {e}")
        await channel.connect()

    @commands.guild_only()
    @commands.hybrid_command(name="leave")
    async def leave(self, ctx):
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send('disconnected')
        else:
            return await ctx.send('bot is not connected!')

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
