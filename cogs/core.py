# Copyright (c) 2019 Blaze <blaze@vivaldi.net>
# Licensed under the GNU General Public License, version 3 or later.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from discord.ext import commands

from bot import is_owner


class Core(commands.Cog, name='Core'):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def load(self,
                   ctx: commands.context.Context, extension: str) -> None:
        if extension != 'core':
            try:
                self.client.load_extension("cogs.{}".format(extension))
            except Exception as error:
                print("{} cannot be loaded. [{}]".format(extension, error))

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def unload(self,
                     ctx: commands.context.Context, extension: str) -> None:
        if extension != 'core':
            try:
                self.client.unload_extension("cogs.{}".format(extension))
            except Exception as error:
                print("{} cannot be unloaded. [{}]".format(extension, error))

    @commands.command(hidden=True, name='off')
    @commands.check(is_owner)
    async def offline(self, ctx: commands.context.Context) -> None:
        await self.client.logout()


def setup(client):
    client.add_cog(Core(client))
