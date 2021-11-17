# Copyright (c) 2019 Blaze <blaze@vivaldi.net>
# Licensed under the GNU General Public License, version 3 or later.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from typing import Optional

import discord
from discord import Colour as col
from discord.ext import commands

from bot_secrets import WELCOME_CHANNEL


class Fun(commands.Cog, name='Fun'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        channel = self.client.get_channel(WELCOME_CHANNEL)
        if channel:
            await channel.send(
                "{} flew away through the open window".format(member.name))

    @commands.command()
    async def radar(self, ctx: commands.context.Context, radar: str) -> None:
        """
        Shows a weather radar map for the selected airport.
        Takes one argument which should be a valid airport code. Example: UMMN
        """
        await ctx.send(
            "http://meteoinfo.by/radar/{}/radar-map.gif".format(radar.upper()))

    @commands.command(name='tr')
    async def translate(self,
                        ctx: commands.context.Context,
                        id: Optional[int] = None) -> None:
        """
        Rewrites the message in an appropriate keyboard layout if it's wrong.
        Takes a message id as an argument or no argument at all. If there's
        no argument, gets the latest message from the channel log.
        """
        channel = ctx.message.channel
        tr = ("qwertyuiop[]asdfghjkl;'zxcvbnm,./"
              "QWERTYUIOP}{ASDFGHJKL:\"ZXCVBNM<>? ")
        lt = ("йцукенгшщзхъфывапролджэячсмитьбю."
              "ЙЦУКЕНГШЩЗЪХФЫВАПРОЛДЖЭЯЧСМИТЬБЮ, ")
        msg = None
        if id:
            msg = await channel.fetch_message(id)
        else:
            msg = await channel.history(limit=1).__anext__()
        if msg:
            result = ''.join([lt[tr.find(c)] for c in msg.content if c in tr])
            em = discord.Embed(description=result, colour=col.dark_gold())
            em.set_author(name=msg.author.name,
                          icon_url=msg.author.avatar_url)
            em.timestamp = msg.created_at
            em.set_footer(text='translated')
            await channel.send(embed=em)


def setup(client):
    client.add_cog(Fun(client))
