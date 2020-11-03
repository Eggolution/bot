import asyncio
import os
import traceback
from pathlib import Path
from random import randint
from datetime import datetime
import discord
from discord.ext import commands
from discord import Member, channel, message
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
import json


def setup(bot2):
    bot2.add_cog(Other(bot2))


class Other(commands.Cog):
    """Other Commands"""

    def __init__(self, bot2):
        self.bot2 = bot2

    @commands.command()
    async def botinfo(self, ctx):
        """Information about the bot"""
        e = discord.Embed(timestamp=datetime.utcnow())
        e.set_author(url=self.bot2.user.avatar_url, name=self.bot2.user.name)
        e.add_field(name="Library", value='discord.py', inline=True)
        e.add_field(name="Version", value=discord.__version__, inline=True)
        e.add_field(name="Developers", value="<@393480172638044160>\n<@731930953446064230>")
        e.description = "[» Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=761317195589746728&permissions=8&scope=bot)\n» ~~Join the Official Server~~ (none yet)"
        e.color = self.bot2.color
        e.set_footer(text='Eggolution info')
        await ctx.send(embed=e)

        # @commands.command()
# async def check(self, ctx,*, arg):
#     arg1 = eval(arg)
#     msg = "Input:\n```"+str(arg)#+"```\n\nOutput:\n```"+str(arg1)++"```"
#     await ctx.send(msg)
#     print(msg)
