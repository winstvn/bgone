import typing

import discord
from discord.ext import commands

import utility as util
from api_key_list import api_key_list
from config import *
from exceptions import *

# initialize the bot and the key list
bot = commands.Bot(command_prefix='!')
key_list = api_key_list(API_KEYS, f'{API_URL}/account')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error
    

@bot.listen('on_message')
async def on_message(message: discord.Message):
    cleaned_message = message.content.strip().lower()
    jar_emoji = discord.utils.get(message.guild.emojis, name='jar3')
    
    if cleaned_message == 'come':
        if jar_emoji:
            await message.add_reaction(jar_emoji)
        else:
            await message.add_reaction('💦')


@bot.command(name='removebg')
async def removebg(ctx, url: typing.Optional[str] = ''):
    """Attempts to remove the background from an image url given as a parameter 
    or the most recently sent image.

    Args:
        url (str): A optional url containing an image to remove the background from.
    """
    
    async with ctx.typing():
        try:
            url = await util.find_img_url_in_history(ctx, MSG_HISTORY_LIMIT) if url == '' else url
            result_img = util.remove_bg(key_list, url)
            await ctx.send(file=util.byte_to_discord_file(result_img))
            
        except (OutOfCreditsException, 
                RemovebgHTTPException, 
                ImgNotInHistoryException) as e:
            await ctx.send(e)


@bot.command(name='credits-left')
async def credits_left(ctx):
    """Displays the number of free API calls left.
    """    
    await ctx.send(f'{key_list.total_credits} free API calls left')


if __name__ == '__main__':
    bot.run(TOKEN)
