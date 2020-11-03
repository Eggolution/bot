import asyncio
import os
import traceback
from pathlib import Path
from random import randint

import motor.motor_asyncio
from pymongo import MongoClient

from cogs.mongo import Document

import DiscordUtils

from secrets import TOKEN
import discord
from discord.ext import commands
from discord import Member, channel, message
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
import json
from pretty_help import PrettyHelp

intents = discord.Intents.default()
intents.members = True


def get_prefix(bot, message):
    with open('cogs/prefixes/prefixes.json', 'r') as f:
        data = json.load(f)
    if not str(message.channel.id) in data:
        return commands.when_mentioned_or('e!', 'E!', '~')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)


bot: Bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owners_id=393480172638044160,
                         intents=intents)

bot.help_command = PrettyHelp(color=0x808080, active=100)

tracker = DiscordUtils.InviteTracker(bot)

ext = ['cogs.config', 'cogs.game', 'cogs.fun', 'cogs.other', 'cogs.mod', 'jishaku', 'cogs.invite']
if __name__ == '__main__':
    bot.connection_url = "mongodb+srv://xeno:j5w1CrLgar6irElX@cluster0.1kvbu.mongodb.net/<dbname>?retryWrites=true&w=majority"
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["Info"]
    bot.invites = Document(bot.db, "invites")
    for extension in ext:
        bot.load_extension(extension)

    # https://www.youtube.com/watch?v=uXn-zOt68V8

bot.run(TOKEN)
