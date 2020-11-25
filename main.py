import motor.motor_asyncio

from cogs.mongo import Document

import DiscordUtils
from datetime import datetime
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


async def get_prefix(bot, message):
    if message.author.id == 393480172638044160:
        return commands.when_mentioned_or('t')(bot, message)

    else:
        if not message.guild:
            return commands.when_mentioned_or('t')(bot, message)

        try:
            data = await bot.config.find(message.guild.id)

            if not data or "prefix" not in data:
                return commands.when_mentioned_or('t')(bot, message)
            return commands.when_mentioned_or(data["prefix"].lower(), data["prefix"].upper())(bot, message)
        except:
            return commands.when_mentioned_or('t')(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owners_id=393480172638044160,
                         intents=intents)
bot.snipes = {}

bot.launch_time = datetime.utcnow()


tracker = DiscordUtils.InviteTracker(bot)

ext = ['cogs.config', 'cogs.game', 'cogs.fun', 'cogs.other', 'cogs.mod', 'jishaku', 'cogs.invite', 'cogs.events', 'cogs.music', 'cogs.help']
if __name__ == '__main__':
    bot.connection_url = "mongodb+srv://xeno:j5w1CrLgar6irElX@cluster0.1kvbu.mongodb.net/<dbname>?retryWrites=true&w=majority"
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["Info"]
    bot.invites = Document(bot.db, "invites")
    bot.invitee = Document(bot.db, "invitee")
    bot.warns = Document(bot.db, "warns")
    bot.userinfo = Document(bot.db, "userinfo")
    bot.config = Document(bot.db, "prefixes")

    for extension in ext:
        bot.load_extension(extension)

    # https://www.youtube.com/watch?v=uXn-zOt68V8

bot.run(TOKEN)
