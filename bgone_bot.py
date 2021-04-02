from api_key_list import api_key_list
import os
import typing

import utility as util

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./env/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEYS = os.getenv('REMOVE_BG_API_KEY').split(', ')
MSG_HISTORY_LIMIT = 10

bot = commands.Bot(command_prefix='!')
key_list = api_key_list(API_KEYS, util.API_URL+'/account')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# @bot.event
# async def on_command_error(ctx, error):
#     pass


@bot.command()
async def bgone(ctx, url: typing.Optional[str] = ''):
    """attempts to remove the background from an image url given as a parameter 
    or the most recently sent image.

    Args:
        url (str, optional): A url containing an image to remove the background
                             from. If one is not given, then will attempt to
                             search for image in message history.
    """
    if url:
        await util.remove_bg(ctx, key_list, url)
    else:
        async for msg in ctx.channel.history(limit=MSG_HISTORY_LIMIT):
            url = util.get_message_img_url(msg)
            if url is not None:
                break
        else:
            await ctx.send('Image not found!')
            return

        await util.remove_bg(ctx, key_list, url)


@bot.command(name='bgone-replacebg')
async def bgone_replacebg(ctx, bg_url: str, url: typing.Optional[str] = ''):
    """attempts to remove background from the image url and replace it with the
    given image. If image url is not provided, then will search for an image in
    message history.

    Args:
        bg_url (str): An url containing the image to replace background with.
        url (str, optional): An url containing an image to remove the background
                             from. If one is not given, then will attempt to
                             search for image in message history.
    """
    if url:
        await util.remove_bg(ctx, key_list, url, bg_url)
    else:
        async for msg in ctx.channel.history(limit=MSG_HISTORY_LIMIT):
            url = util.get_message_img_url(msg)
            if url is not None:
                break
        else:
            await ctx.send('No image found!')
            return

        await util.remove_bg(ctx, key_list, url, bg_url)


@bot.command(name='credits-left')
async def credits_left(ctx):
    await ctx.send(f'{util.num_credits_left(key_list)} free API calls left')


if __name__ == '__main__':
    bot.run(TOKEN)
