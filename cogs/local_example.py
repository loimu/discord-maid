# Copyright (c) 2019 Blaze <blaze@vivaldi.net>
# Licensed under the GNU General Public License, version 3 or later.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import aiohttp
import subprocess
import io

import discord
from discord import Colour as col
from discord.ext import commands

from bot import is_owner


class Local(commands.Cog, name='Local'):

    def __init__(self, client):
        self.client = client

    def capitalize(self, string: str) -> str:
        return (string[0].upper() + string[1:]) if string else ''

    async def get_img(self, url: str) -> discord.File:
        filename = url.split('/')[-1]
        img_file = b''
        async with aiohttp.ClientSession(loop=self.client.loop) as s:
            async with s.get(url) as r:
                img_file = await r.read()
        return discord.File(fp=io.BytesIO(img_file), filename=filename)

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def np(self, ctx: commands.context.Context) -> None:
        em = discord.Embed(title='_now playing_ :headphones:',
                           description=subprocess.getoutput("mocp -Q '%title'"),
                           colour=col.orange())
        em.set_footer(text='mocp')
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Local(client))
