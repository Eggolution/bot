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
from contextlib import redirect_stdout


def setup(bot2):
    bot2.add_cog(Config(bot2))


class Config(commands.Cog):
    """Owner Commands"""
    def __init__(self, bot2):
        self.bot2 = bot2

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        """Reload Cogs (Owner Only)"""
        if ctx.message.author.id == 393480172638044160:
            if not cog:
                # No cog, means we reload all cogs
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Reloading all cogs!",
                        color=0x808080,
                        timestamp=ctx.message.created_at
                    )
                    for ext in os.listdir("./cogs/"):
                        if ext.endswith(".py") and not ext.startswith("_"):
                            try:
                                self.bot2.unload_extension(f"cogs.{ext[:-3]}")
                                self.bot2.load_extension(f"cogs.{ext[:-3]}")
                                embed.add_field(
                                    name=f"Reloaded: `{ext}`",
                                    value='\uFEFF',
                                    inline=False
                                )
                            except Exception as e:
                                embed.add_field(
                                    name=f"Failed to reload: `{ext}`",
                                    value=e,
                                    inline=False
                                )
                            await asyncio.sleep(0.5)
                    await ctx.send(embed=embed)
            else:
                # reload the specific cog
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Reloading all cogs!",
                        color=0x808080,
                        timestamp=ctx.message.created_at
                    )
                    ext = f"{cog.lower()}.py"
                    if not os.path.exists(f"./cogs/{ext}"):
                        # if the file does not exist
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value="This cog does not exist.",
                            inline=False
                        )

                    elif ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot2.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot2.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception:
                            desired_trace = traceback.format_exc()
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=desired_trace,
                                inline=False
                            )
                    await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot2.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=f'Eggolution'))
        print("I'm ready")

    @commands.command()
    async def change(self, ctx, arg, *, argv: str):
        """Change the presence of the bot (Owner Only)"""
        if ctx.message.author.id == 393480172638044160:
            if arg.lower() == 'listening':
                await self.bot2.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.listening, name=f'{argv}'))
                await ctx.send(f'Egg is now listening to {argv}')
            elif arg.lower() == 'playing':
                await self.bot2.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.playing, name=f'{argv}'))
                await ctx.send(f'Egg is now playing {argv}')
            elif arg.lower() == 'watching':
                await self.bot2.change_presence(
                    activity=discord.Activity(type=discord.ActivityType.watching, name=f'{argv}'))
                await ctx.send(f'Egg is now watching {argv}')
            else:
                await ctx.send('Be more specific')
        else:
            await ctx.send('No perms, sorry')