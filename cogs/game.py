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
import pymongo
from pymongo import MongoClient


def setup(bot):
    bot.add_cog(Game(bot))


class Game(commands.Cog):
    """Game Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        """Start your adventure"""
        e = discord.Embed(timestamp=datetime.utcnow())
        e.set_author(name='Welcome to Eggolution!')
        e.add_field(name='What is Eggolution?',
                    value='Eggolution is a game where you level up to become the best. You can trade, battle, and choose your path.',
                    inline=False)
        e.add_field(name='How do I start?', value='you can start using the e!play command.', inline=False)
        e.add_field(name='How do I play?', value='Just start chatting! If you need more detailed help, use e!help',
                    inline=False)
        e.set_footer(text='Eggolution game')
        e.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def play(self, ctx):
        """Create your profile"""
        mongo_url = "mongodb+srv://xeno:j5w1CrLgar6irElX@cluster0.1kvbu.mongodb.net/<dbname>?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["Info"]
        collection = db["userinfo"]
        author_id = ctx.message.author.id
        form = "egg"
        color = "none"
        insert = {"_id": author_id, "form": form, "color": color, "XP": 0, "level": 0, "hp": 0, "atk": 0, "def": 0, "sp": 0}
        await collection.insert_one(insert)

        await ctx.send('I have created your profile, use e!info to see yourself')

    @commands.command()
    async def info(self, ctx):
        """See your stats"""
        mongo_url = "mongodb+srv://xeno:j5w1CrLgar6irElX@cluster0.1kvbu.mongodb.net/<dbname>?retryWrites=true&w=majority"
        cluster = MongoClient(mongo_url)
        db = cluster["Info"]
        collection = db["userinfo"]
        author_id = ctx.message.author.id
        x = collection.find_one({"_id": author_id}, {"form": 1, "hp": 1, "atk": 1, "def": 1, "sp": 1, "color": 1})

        e = discord.Embed(timestamp=datetime.utcnow())
        e.set_thumbnail(url=ctx.message.author.avatar_url)
        if x["form"] == "egg":
            e.set_author(name=f'You are a {x["color"]} Egg!')
            e.set_image(url="https://media.discordapp.net/attachments/730191153206525955/766757785689260052/Untitled.png?width=517&height=560")
        elif x["form"] == "egg":
            e.set_author(name='Egg')
            e.set_image(url="https://media.discordapp.net/attachments/730191153206525955/766757785689260052/Untitled.png?width=517&height=560")
        elif x["form"] == "egg":
            e.set_author(name='Egg')
            e.set_image(
                url="https://media.discordapp.net/attachments/730191153206525955/766757785689260052/Untitled.png?width=517&height=560")
        elif x["form"] == "egg":
            e.set_author(name='Egg')
            e.set_image(
                url="https://media.discordapp.net/attachments/730191153206525955/766757785689260052/Untitled.png?width=517&height=560")
        elif x["form"] == "egg":
            e.set_author(name='Egg')
            e.set_image(
                url="https://media.discordapp.net/attachments/730191153206525955/766757785689260052/Untitled.png?width=517&height=560")
        elif x["form"] == "egg":
            e.set_author(name='Egg')
            e.set_image(
                url="https://media.discordapp.net/attachments/730191153206525955/766757785689260052/Untitled.png?width=517&height=560")
        e.add_field(name=f'**Attack:** {x["atk"]}/100', value='‎', inline=False)
        e.add_field(name=f'**Defense:** {x["def"]}/100', value='‎', inline=False)
        e.add_field(name=f'**Health:** {x["hp"]}/100', value='‎', inline=False)
        e.add_field(name=f'**Special:** {x["sp"]}/100', value='‎', inline=False)

        await ctx.send(embed=e)