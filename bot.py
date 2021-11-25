#! /usr/bin/env python3
# Copyright (c) 2019 Blaze <blaze@vivaldi.net>
# Licensed under the GNU General Public License, version 3 or later.
# See the file http://www.gnu.org/copyleft/gpl.txt.

import discord
from discord import Colour as col
from discord.ext import commands

from bot_secrets import PREFIX, OWNER_ID, BOT_TOKEN

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)
extensions = ['core', 'admin', 'mod', 'fun']

is_owner = lambda x: x.message.author.id == OWNER_ID


@client.event
async def on_ready():
    print("logged in")


@client.event
async def on_message(message: discord.Message) -> None:
    if not message.content.startswith(PREFIX):
        return
    await message.delete()
    await client.process_commands(message)


@client.event
async def on_command_error(ctx: commands.context.Context, error) -> None:
    command = ctx.message.content.split()[0].replace(PREFIX, '', 1)
    em = discord.Embed(title='Command Error',
                       description=':question: Something went wrong',
                       colour=col.dark_red())
    em.set_footer(text="See {}help {}".format(PREFIX, command))
    if isinstance(error, commands.errors.CommandNotFound):
        em.description = ":warning: Command not found"
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        em.description = ":warning: Argument is missing"
    elif isinstance(error, commands.errors.UserInputError):
        em.description = ":warning: Wrong argument. {}".format(error)
    await ctx.send(embed=em)
    print(error)


if __name__ == '__main__':
    for ext in extensions:
        try:
            client.load_extension("cogs.{}".format(ext))
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(ext, error))
    client.run(BOT_TOKEN)
