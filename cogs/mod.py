import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
from discord import Member, channel, message
from datetime import datetime


def setup(bot):
    bot.add_cog(Moderation(bot))


class Moderation(commands.Cog):
    """Moderation Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx, *, pre='e!'):
        """Change the prefix"""
        if ctx.message.author.guild_permissions.administrator:
            await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": pre})
            await ctx.send('Prefix changed!')
        elif pre is None:
            await ctx.send('Prefix cannot be blank! (ping me to see my current prefix)')
        else:
            await ctx.send('Sorry you do not have permissions to do that!')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def nick(self, ctx, user: discord.Member, *, nickname):
        """Nickname Someone"""
        await user.edit(nick=nickname)
        await ctx.send('Nicknamed!')

    @commands.command(name="kick", pass_context=True)
    @has_permissions(manage_roles=True, kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member"""
        await member.kick(reason=reason)
        await ctx.send('Kicked :white_check_mark:')
        await ctx.send('https://tenor.com/view/kicked-in-the-nuts-kick-gif-6926792')

    @commands.command(name="ban", pass_context=True)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member"""
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member} :white_check_mark:')
        await ctx.send('https://tenor.com/view/when-your-team-too-good-ban-salt-bae-gif-7580925')

    @commands.command(name='unban', pass_context=True)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, id: int):
        """Unban a member"""
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned :white_check_mark:')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def purge(self, ctx, limit: int):
        """Purge messages"""
        limit1 = limit + 1
        await ctx.channel.purge(limit=limit1)

    @commands.command()
    async def echo(self, ctx, *, message):
        """Echo your message"""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        """Lockdown a channel"""
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put `{channel.name}` on lockdown.")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[
            ctx.guild.default_role].send_messages is None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put `{channel.name}` on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have removed `{channel.name}` from lockdown.")

    @commands.group(name='warn', invoke_without_command=True)
    async def warn(self, ctx, mention: discord.Member, *, reason="Not Provided"):
        """Warn a member"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        if ctx.author.guild_permissions.manage_messages:
            if mention.bot:
                await ctx.send("You can't warn a bot...", delete_after=5.0)
            elif ctx.author is mention:
                await ctx.send(f"{ctx.author.mention}, You can't warn youself..")
            elif mention is ctx.guild.owner:
                await ctx.send(f"{ctx.author.mention}, You can't warn the owner of the server...")
            elif ctx.author is ctx.guild.owner:
                collections = db["warn"]
                detail = {"mention": mention.id, "reason": reason, "author": ctx.author.id,
                          "channel": ctx.channel.id,
                          "guild": ctx.guild.id}
                collections.insert_one(detail)
                warnlists = collections.find({"mention": int(mention.id), "guild": int(ctx.guild.id)})
                warnings = []
                for x in warnlists:
                    warnings.append(x)
                value = len(warnings)
                embed = discord.Embed(color=0x808080,
                                      description=f"**{mention.mention} has been warned.**  \n**Reason-** {reason} ",
                                      timestamp=datetime.utcnow())

                embed.set_author(name=f"Warning #{value}")
                embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
                await ctx.send(embed=embed)
                embed1 = discord.Embed(color=0x808080,
                                       description=f"***You have been warned by {ctx.author}.***  \n**Reason-** {reason} ",
                                       timestamp=datetime.utcnow())
                embed1.set_author(name=f"Warning #{value}")
                embed1.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
                await mention.send(embed=embed1)
            elif ctx.author.top_role <= mention.top_role or mention is ctx.guild.owner:
                await ctx.send(
                    f"{ctx.author.mention},You can't warn a member whose role is either equal or greater then your role...")
            else:
                if ctx.author.guild_permissions.manage_messages:
                    collections = db["warn"]
                    detail = {"mention": mention.id, "reason": reason, "author": ctx.author.id,
                              "channel": ctx.channel.id,
                              "guild": ctx.guild.id}
                    collections.insert_one(detail)
                    warnlists = collections.find({"mention": int(mention.id), "guild": int(ctx.guild.id)})
                    warnings = []
                    for x in warnlists:
                        warnings.append(x)
                    value = len(warnings)
                    embed = discord.Embed(color=0x808080,
                                          description=f"***{mention.mention} has been warned.***  \n**Reason-** {reason} ")
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(name=f"Warning #{value}")
                    embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
                    await ctx.send(embed=embed)
                    embed1 = discord.Embed(color=0x808080,
                                           description=f"***You have been warned by {ctx.author}.***  \n**Reason-** {reason} ",
                                           timestamp=datetime.utcnow())
                    embed1.set_author(name=f"Warning #{value}")
                    embed1.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
                    await mention.send(embed=embed1)
                else:
                    await ctx.send("You need to have **manage messages** permission to use this command...")
        else:
            await ctx.send("You need to have **manage messages** permission to use this command...")

    @commands.command()
    async def warnings(self, ctx, mention: discord.Member):
        """See the warnings of a user"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        collections = db["warn"]
        warnlists = collections.find({"mention": int(mention.id), "guild": int(ctx.guild.id)})
        warnings = []
        for x in warnlists:
            warnings.append(x)
        value = len(warnings)
        embed = discord.Embed(title="Warnings", description=f"No warning for {mention.mention}.",
                              color=0x808080,
                              timestamp=datetime.utcnow())
        embed1 = discord.Embed(title="Warnings",
                               description=f'Total warnings {mention.mention} has received: **{value}**',
                               color=0x808080,
                               timestamp=datetime.utcnow())

        if not warnings:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed1)

    @warn.command(name='clear')
    async def clear_subcommand(self, ctx, mention: discord.Member):
        """Clear warnings"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        if ctx.author.guild_permissions.manage_messages:
            collections = db["warn"]
            collections.delete_many({"mention": int(mention.id), "guild": int(ctx.guild.id)})
            embed = discord.Embed(title="Warnings", description=f"Warnings of {mention.mention} has been cleared.",
                                  color=0x808080,
                                  timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.send("You need to have **manage messages** permission to use this command...")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.bot.snipes[message.channel.id] = message

    @commands.command()
    async def snipe(self, ctx, *, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            msg = self.bot.snipes[channel.id]
        except KeyError:
            return await ctx.send('Nothing to snipe!')
        # one liner, dont complain
        await ctx.send(
            embed=discord.Embed(description=msg.content, color=msg.author.color).set_author(name=str(msg.author),
                                                                                            icon_url=str(
                                                                                                msg.author.avatar_url)))

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    @commands.guild_only()
    async def flood(self, ctx):
        x = 0
        while x < 25:
            await ctx.send('Flood')
            x += 1
