import asyncio
import os
import random
import traceback
from pathlib import Path
from random import randint

import aiohttp
import discord
from discord.ext import commands
from discord import Member, channel, message
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
from datetime import datetime
from secrets import DAGPI

def setup(bot):
    bot.add_cog(Fun(bot))


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Star Wars reference"""
        async with ctx.typing():
            await ctx.send('Hello there,')
            await ctx.send('General Kenobi')

    @commands.command(description="See your avatar", aliases=['avatar'])
    async def av(self, ctx, *, member : discord.Member=None):
        if member is None:
            author = ctx.message.author
        else:
            author = member
        embed = discord.Embed(timestamp=datetime.utcnow(), color=0x808080, title="Avatar")
        embed.set_author(name=author, icon_url=author.avatar_url)
        embed.set_image(url=author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def dadjoke(self, ctx):
        """Returns a Dad Joke"""
        headers = {
            'Accept': "application/json",
            'User-Agent': "Eggolution Discord Bot (https://discord.gg/UkKdT5A)"
        }
        async with aiohttp.ClientSession(headers=headers) as cs:
            async with cs.get('https://icanhazdadjoke.com/') as r:
                res = await r.json()  # returns dict
                embed = discord.Embed(timestamp=datetime.utcnow(), color=0x808080)
                embed.set_author(name='Dad Joke')
                embed.set_thumbnail(
                    url='https://i.imgur.com/iEQKdHA.png')
                embed.add_field(name=res["joke"], value="‎")

                msg = await ctx.send(embed=embed)
                await msg.add_reaction('🤣')

    @commands.command()
    async def joke(self, ctx):
        """Returns a Joke"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://sv443.net/jokeapi/v2/joke/Any') as r:
                res = await r.json()  # returns dict
                embed = discord.Embed(timestamp=datetime.utcnow(), color=0x808080)
                embed.set_author(name='Joke')
                embed.set_thumbnail(
                    url='https://i.imgur.com/iEQKdHA.png')
                embed.add_field(name=res["setup"], value=f"||{res['delivery']}||")

                msg = await ctx.send(embed=embed)
                await msg.add_reaction('🤣')

    @commands.command()
    async def meme(self, ctx):
        """Get a meme"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.herokuapp.com/gimme/dankmemes') as resp:
                resp = await resp.json()

            if resp['nsfw'] == True and not ctx.channel.is_nsfw():
                return await ctx.send("⚠️ This meme is marked as NSFW and I can't post it in a non-nsfw channel.")
            else:
                embed = discord.Embed(title=resp['title'], url=resp['postLink'], color=0x2F3136)
                embed.set_image(url=resp['url'])
                embed.set_footer(text="r/Dankmemes")
                await ctx.send(embed=embed)

    @commands.command(aliases=['pokemon'])
    async def wtp(self, ctx):
        """Play a pokemon guessing game"""
        headers = {
            "Authorization" : DAGPI
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://api.dagpi.xyz/data/wtp') as resp:
                res = await resp.json()

        question = discord.Embed(color=0x808080, timestamp=datetime.utcnow(), title=f'Who is that pokemon!').set_image(url=res["question"])
        correct = discord.Embed(color=0x808080, timestamp=datetime.utcnow(), title=f'You are correct!').set_image(
            url=res["answer"])
        wrong = discord.Embed(color=0x808080, timestamp=datetime.utcnow(), title=f'The correct answer is {res["Data"]["name"]}').set_image(
            url=res["answer"])
        sent = await ctx.send(embed=question)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel
            )
            if msg.content.lower() == res["Data"]["name"].lower():
                await ctx.send(embed=correct)

            else:
                await ctx.send(embed=wrong)

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling due to timeout", delete_after=10)

    @commands.command()
    async def roast(self, ctx, *, member : discord.Member=None):
        """Roast someone or get a roast"""
        headers = {
            "Authorization": DAGPI
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://api.dagpi.xyz/data/roast') as resp:
                res = await resp.json()

        if member is None:
            await ctx.send(f'Here is your roast:\n{res["roast"]}')
        else:
            if (ctx.message.guild.me in ctx.message.mentions) or (member.id == 393480172638044160):
                await ctx.send("I don't feel like roasting them")
            else:
                await ctx.send(f'<@{member.id}>, {res["roast"]}')

    @commands.command(aliases=['ym', 'yom'])
    async def yomama(self, ctx, *, member: discord.Member=None):
        """Get a Yo Mama Joke"""
        headers = {
            "Authorization": DAGPI
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://api.dagpi.xyz/data/yomama') as resp:
                res = await resp.json()
        if member is None:
            await ctx.send(f'Here is your Joke,\n{res["description"]}')
        else:
            if (ctx.message.guild.me in ctx.message.mentions) or (member.id == 393480172638044160):
                await ctx.send("I don't feel like roasting them with a Yo Mama Joke")
            else:
                await ctx.send(f'<@{member.id}>, {res["description"]}')

    @commands.command()
    async def Waifu(self, ctx):
        """Get some Waifu"""
        headers = {
            "Authorization": DAGPI
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://api.dagpi.xyz/data/waifu') as resp:
                res = await resp.json()
        embed = discord.Embed(color=0x808080, title="Here is your Waifu", timestamp=datetime.utcnow()).set_image(url=res["display_picture"])
        await ctx.send(embed=embed)
