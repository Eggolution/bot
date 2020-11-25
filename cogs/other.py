import asyncio
import os
import time
import traceback
from pathlib import Path
from random import randint
from datetime import datetime
import discord
import googletrans as googletrans
from discord.ext import commands
from discord import Member, channel, message
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
import json


def setup(bot):
    bot.add_cog(Other(bot))


class Other(commands.Cog):
    """Other Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.trans = googletrans.Translator()

    @commands.command()
    async def botinfo(self, ctx):
        """Information about the bot"""
        e = discord.Embed(timestamp=datetime.utcnow())
        e.set_author(url=self.bot.user.avatar_url, name=self.bot.user.name)
        e.add_field(name="Library", value='discord.py', inline=True)
        e.add_field(name="Version", value=discord.__version__, inline=True)
        e.add_field(name="Developers", value="<@393480172638044160>")
        e.description = "[» Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=761317195589746728&permissions=8&scope=bot)\n» ~~Join the Official Server~~ (none yet)"
        e.set_footer(text='Eggolution info')
        await ctx.send(embed=e)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Quickly test the bot's ping"""

        new = await ctx.send('Pong!')
        delta = new.created_at - ctx.message.created_at
        await new.edit(content=f'Pong!\n'
                               f'Round trip: {delta.total_seconds() * 1000:.0f} ms\n'
                               f'Heartbeat latency: {self.bot.latency * 1000:.0f} ms')


    @commands.command()
    async def translate(self, ctx, *, message: commands.clean_content):
        """Translates a message to English using Google translate."""

        loop = self.bot.loop

        try:
            ret = await loop.run_in_executor(None, self.trans.translate, message)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e.__class__.__name__}: {e}')

        embed = discord.Embed(title='Translated', colour=0x808080)
        src = googletrans.LANGUAGES.get(ret.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(ret.dest, 'Unknown').title()
        embed.add_field(name=f'From {src}', value=ret.origin, inline=False)
        embed.add_field(name=f'To {dest}', value=ret.text, inline=False)
        await ctx.send(embed=embed)
