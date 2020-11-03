import asyncio
import os
import traceback
from pathlib import Path
from random import randint

import discord
from discord.ext import commands
from discord import Member, channel, message
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
import json


def setup(bot2):
    bot2.add_cog(Fun(bot2))


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, bot2):
        self.bot2 = bot2

    @commands.command()
    async def hello(self, ctx):
        """Star Wars reference"""
        async with ctx.typing():
            await ctx.send('Hello there,')
            await asyncio.sleep(1)
            await ctx.send('General Kenobi')
