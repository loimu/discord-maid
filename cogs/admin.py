# Copyright (c) 2019 Blaze <blaze@vivaldi.net>
# Licensed under the GNU General Public License, version 3 or later.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from typing import Optional

import discord
from discord import Colour as col
from discord.ext import commands

from bot import is_owner


class Admin(commands.Cog, name='Admin'):

    def __init__(self, client):
        self.client = client

    @commands.command(name='server')
    async def server_info(self, ctx: commands.context.Context) -> None:
        """
        Shows some information about the server
        """
        server = ctx.message.guild
        info = "name: {}\nuser count: {}\ncreation date: {}".format(
            server.name,
            server.member_count,
            server.created_at)
        em = discord.Embed(title='server info',
                           description=info, colour=col.green())
        em.set_thumbnail(url=server.icon_url)
        await ctx.message.channel.send(embed=em)

    @commands.command(aliases=['pfp'])
    async def avatar(self, ctx: commands.context.Context, id: int) -> None:
        """
        Shows the profile picture of the given user in full size.
        A valid user id should be provided as an argument.
        """
        if id < 100_000_000_000_000_000:
            raise commands.errors.UserInputError("User id is not valid")
            return
        user = await self.client.fetch_user(id)
        em = discord.Embed(title="profile picture of {}".format(user.name),
                           color=col.gold())
        em.set_image(url=user.avatar_url)
        await ctx.message.channel.send(embed=em)

    @commands.command(hidden=True, name='user')
    @commands.check(is_owner)
    async def user_info(self,
                        ctx: commands.context.Context, target: str) -> None:
        user = ctx.message.guild.get_member_named(target)
        info = "name: {}\nrole: {}\nid: {}\njoined:{}\ncreated: {}".format(
            user.name,
            user.top_role,
            user.id,
            user.joined_at,
            user.created_at)
        em = discord.Embed(description=info, colour=user.color)
        em.set_author(name=user.nick)
        em.set_thumbnail(url=user.avatar_url)
        await ctx.message.channel.send(embed=em)

    @commands.command()
    async def quote(self, ctx: commands.context.Context, id: int) -> None:
        """
        Shows the quoted message if the valid message id is given.
        Quoting messages from channels where you don't have
        the read permission is not allowed.
        Embedded messages can't be quoted too.
        """
        channel = ctx.message.channel
        member = ctx.message.author
        if id < 100_000_000_000_000_000:
            raise commands.errors.UserInputError("Message id is not valid")
            return
        for ch in channel.guild.text_channels:
            try:
                msg = await ch.fetch_message(id)
            except discord.errors.NotFound:
                continue
            if not member.permissions_in(ch).read_messages:
                raise commands.errors.UserInputError("No permissions to read")
                break
            if any(msg.embeds):
                raise commands.errors.UserInputError("Is an embedded message")
                break
            em = discord.Embed(title=None,
                               description=msg.content,
                               colour=msg.author.color)
            name = msg.author.nick if msg.author.nick else msg.author.name
            em.set_author(name=name, icon_url=msg.author.avatar_url)
            em.timestamp = msg.created_at
            if any(msg.attachments):
                em.set_image(url=msg.attachments[0]['url'])
            em.set_footer(text="quote from #{}".format(msg.channel.name))
            await channel.send(embed=em)
            break

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def purge(self,
                    ctx: commands.context.Context,
                    target: Optional[str] = None) -> None:
        channel = ctx.message.channel
        if target:
            if target.isdigit():
                await channel.purge(limit=int(target))
            else:
                await channel.purge(
                    check=lambda x: x.author == x.guild.get_member_named(
                        target))
        else:
            await channel.purge(limit=1)


def setup(client):
    client.add_cog(Admin(client))
