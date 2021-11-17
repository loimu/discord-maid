# Copyright (c) 2019 Blaze <blaze@vivaldi.net>
# Licensed under the GNU General Public License, version 3 or later.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from typing import Optional, List

import discord
from discord.utils import get
from discord import Colour as col
from discord.ext import commands


mod_role = 'staff'


class Mod(commands.Cog, name='Mod'):
    """
    requires "Manage Roles" permission
    """

    def __init__(self, client):
        self.client = client

    async def notify(self,
                     channel: discord.TextChannel,
                     message: discord.Message) -> None:
        em = discord.Embed(title="#{}".format(channel.name),
                           description=message, colour=col.red())
        await channel.send(embed=em)

    async def get_muted_role(self, server: discord.Guild) -> discord.Role:
        muted = 'muted'
        role = get(server.roles, name=muted)
        if not role:
            role = await server.create_role(name=muted)
            perms = discord.PermissionOverwrite(send_messages=False)
            for ch in server.channels:
                await ch.set_permissions(role, overwrite=perms)
        return role

    @commands.command()
    @commands.has_role(mod_role)
    async def mute(self, ctx: commands.context.Context, target: str) -> None:
        """
        Mutes a given user
        """
        server = ctx.message.guild
        user = server.get_member_named(target)
        mod = get(user.roles, name=mod_role)
        if mod:
            await self.notify(ctx.message.channel,
                              "You can't mute your fellow mod.")
            return
        muted = await self.get_muted_role(server)
        await user.add_roles(muted)
        await self.notify(ctx.message.channel,
                          "User {} was muted by {}.".format(
                              user.name, ctx.message.author.nick))

    @commands.command()
    @commands.has_role(mod_role)
    async def unmute(self, ctx: commands.context.Context, target: str) -> None:
        """
        Unmutes a given user
        """
        user = ctx.message.guild.get_member_named(target)
        muted = get(user.roles, name='muted')
        if muted:
            await user.remove_roles(muted)
        await self.notify(ctx.message.channel,
                          "User {} was unmuted.".format(user.name))

    @commands.command()
    @commands.has_role(mod_role)
    async def stop(self, ctx: commands.context.Context) -> None:
        """
        Unmutes the channel command was invoked on
        """
        server = ctx.message.guild
        channel = ctx.message.channel
        everyone = get(channel.changed_roles, name='@everyone')
        perms = channel.overwrites_for(everyone)
        perms.send_messages = False
        await channel.set_permissions(everyone, overwrite=perms)
        mod = get(server.roles, name=mod_role)
        if mod:
            perms = discord.PermissionOverwrite(send_messages=True)
            await channel.set_permissions(mod, overwrite=perms)
        await self.notify(
            channel, "Channel was deliberately muted by {}. :mute:".format(
                ctx.message.author.nick))

    @commands.command()
    @commands.has_role(mod_role)
    async def start(self, ctx: commands.context.Context) -> None:
        """
        Mutes the channel command was invoked on
        """
        server = ctx.message.guild
        channel = ctx.message.channel
        everyone = get(channel.changed_roles, name='@everyone')
        perms = channel.overwrites_for(everyone)
        perms.send_messages = None
        await channel.set_permissions(everyone, overwrite=perms)
        await self.notify(channel,
                          "Channel was unmuted. Enjoy your freedom. :speaker:")


def setup(client):
    client.add_cog(Mod(client))
