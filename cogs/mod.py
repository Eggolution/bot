import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, Bot, has_guild_permissions
from discord import Member, channel, message
import requests


def setup(bot2):
    bot2.add_cog(Moderation(bot2))


class Moderation(commands.Cog):
    """Moderation Commands"""

    def __init__(self, bot2):
        self.bot2 = bot2

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx, *, pre='.'):
        """Change the prefix"""
        if ctx.message.author.guild_permissions.administrator:
            with open('cogs/prefixes/prefixes1.json', 'r') as f:
                data = json.load(f)

            data[str(ctx.guild.id)] = pre

            with open('cogs/prefixes/prefixes1.json', 'w') as f:
                json.dump(data, f, indent=4)
        elif pre == None:
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
        user = await self.bot1.fetch_user(id)
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
