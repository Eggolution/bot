import asyncio
import os
import traceback
from pathlib import Path
from datetime import datetime

import DiscordUtils
import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Invites(bot))


class Invites(commands.Cog):
    """Invite Tracker Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)



    @commands.Cog.listener()
    async def on_ready(self):
        await self.tracker.cache_invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.update_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        inviter = await self.tracker.fetch_inviter(member)  # inviter is the member who invited
        print(inviter, member)
        data = await self.bot.invites.find(inviter.id)
        if data is None:
            data = {"_id": member.guild.id, str(inviter.id): [0, 0, 0]}

        data[str(inviter.id)][0] += 1
        data[str(inviter.id)][1] += 1
        await self.bot.invites.upsert(data)

        DATA = await self.bot.invitee.find(member.id)
        if DATA is None:
            DATA = {"_id": member.guild.id, str(member.id): inviter.id}
        await self.bot.invitee.upsert(DATA)
        await self.bot.invites.upsert({"_id": member.guild.id, str(member.id): 0})

        channel = discord.utils.get(member.guild.text_channels, name="invites")
        embed = discord.Embed(
            title=f"Welcome {member.display_name}",
            description=f"Invited by: {inviter.mention}\nInvites: {data[str(inviter.id)][0]}",
            timestamp=member.joined_at
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        DATA = await self.bot.invitee.find(member.guild.id)
        inviter = DATA[str(member.id)]
        data = await self.bot.invites.find(member.guild.id)
        data[str(inviter)][0] -= 1
        data[str(inviter)][2] += 1
        await self.bot.invites.upsert(data)
        channel = discord.utils.get(member.guild.text_channels, name="invites")
        embed = discord.Embed(
            title=f"Goodbye {member.display_name}",
            timestamp=datetime.utcnow(),
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        await channel.send(embed=embed)

    @commands.command()
    async def invites(self, ctx, *, member: discord.Member=None):
        """Check how many invites someone has"""
        if member is None:
            author = ctx.message.author.id
            at = ctx.message.author
        else:
            author = member.id
            at = member
        data = await self.bot.invites.find(ctx.message.guild.id)
        if data is None:
            await ctx.send('This server has no invites!')
        else:
            embed = discord.Embed(
                title=f'{at} has:',
                description=f'`{data[str(author)][0]}` invites, `{data[str(author)][1]}` total,`{data[str(author)][2]}` left',
                color=0x808080
            )
            embed.set_thumbnail(url=at.avatar_url)
            embed.set_footer(text=ctx.message.guild.name, icon_url=ctx.message.guild.icon_url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addInvites(self, ctx, member: discord.Member, *, amount):
        """Add invites to a member"""
        data = await self.bot.invites.find(ctx.message.guild.id)
        data[member][0] = data[member][0] + int(amount)

        await self.bot.invites.update({"_id": ctx.message.guild.id, str(member): data})

        await ctx.send(f'Added {amount} invites to {member},who now has {data[member][0]} invites')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def subInvites(self, ctx, member: discord.Member, *, amount):
        """Add invites to a member"""
        data = await self.bot.invites.find(ctx.message.guild.id)
        data[member][0] = data[member][0] - int(amount)

        await ctx.send(f'Subtracted {amount} invites from{member},who now has {data[member][0]} invites')

        await self.bot.invites.update({"_id": ctx.message.guild.id, str(member): data})

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearInvites(self, ctx):
        embed = discord.Embed(title="Are you sure you want to delete ALL invites in this server? (yes or no)", description="This will timeout in 60 seconds")
        sent = await ctx.send(embed=embed)

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=60,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel
            )
            if msg.content.lower() == "yes":
                await self.bot.invites.delete_by_id(ctx.message.guild.id)
                await ctx.send('Success!')

            if msg.content.lower() == "no":
                await msg.delete()
                await sent.delete()
                await ctx.send("Cancelling...", delete_after=10)

        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("Cancelling due to timeout", delete_after=10)
