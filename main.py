import io
import os
import typing
from base64 import b64encode
import pickle

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./env/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('REMOVE_BG_API_KEY')
REMOVE_BG_ENDPOINT = 'https://api.remove.bg/v1.0/removebg'
MSG_HISTORY_LIMIT = 10

bot = commands.Bot(command_prefix='!')


def image_url_to_b64(url: str) -> typing.Union[str, None]:
    """converts the image located at the url to a base64 encoded string. Returns
    None if the url does not contain an image or if the request fails

    Args:
        url (str): the url containing the image

    Returns:
        str or None: the base64 encoded image or None if request failed or
                     returns non-image object
    """
    response = requests.get(url)
    
    if (response.status_code != requests.codes.ok or
        not response.headers['Content-Type'].lower().startswith('image/')):
        return None
    else:
        uri = ("data:" +
            response.headers['Content-Type'] + ";" +
            "base64," + b64encode(response.content).decode("utf-8"))
        return uri


def remove_bg_from_img(img_url: str, bg_img_url: str = '') -> io.BytesIO:
    """removes the background from the image in the url and a byte object

    Args:
        b64_img (str): [description]

    Returns:
        bytes: [description]
    """    
    headers = {'X-Api-Key': API_KEY}
    data = {'crop': True,
            'image_url': img_url,
            'format': 'png'}
    
    if not bg_img_url:
        data['bg_image_url'] = bg_img_url
    
    response = requests.post(REMOVE_BG_ENDPOINT, headers=headers, data=data)
    response.raise_for_status()
    
    img = io.BytesIO(response.content)
    img.name = 'removed-bg.jpg' if bg_img_url else 'removed-bg.png'
    
    return img


def get_message_img_url(msg: discord.Message) -> typing.Union[str, None]:
    """returns the first valid image url in the message or None if one cannot 
    be found

    Args:
        msg (discord.Message): [description]

    Returns:
        typing.Union[str, None]: [description]
    """
    # check if the image url is in the message contents first
    if msg.clean_content[-4:] in ['.jpg', '.png', 'jpeg']:
        return msg.clean_content
    
    # check for an image url in the attachments afterwards
    for attachment in msg.attachments:
        if attachment.url[-4:] in ['.jpg', '.png', 'jpeg']:
            return attachment.url
        
    # return None if no image urls were found
    return None


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    
@bot.event
async def on_error(event, *args, **kwargs):
    pass


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
        try:
            bg_removed_img = remove_bg_from_img(url)
            await ctx.send(file=discord.File(bg_removed_img))
        except requests.HTTPError as e:
            if str(e).startswith('400'):
                await ctx.send('Cannot detect foreground on image. :(')
            elif str(e).startswith('402'):
                await ctx.send('There are no more API credits. Try again in 1 month :)')
            elif str(e).startswith('429'):
                await ctx.send('Rate limit exceeded. Please try again later.')
        except Exception as e:
            await print(e)
    else:
        async for msg in ctx.channel.history(limit=MSG_HISTORY_LIMIT):
            url = get_message_img_url(msg)
            if url is not None:
                break
        else:
            print('No image found!')
            return
        
        try:
            bg_removed_img = remove_bg_from_img(url)
            await ctx.send(file=discord.File(bg_removed_img))
        except requests.HTTPError as e:
            if str(e).startswith('402'):
                await ctx.send('There are no more API credits. Try again in 1 month :)')
            elif str(e).startswith('429'):
                await ctx.send('Rate limit exceeded. Please try again later.')
        except Exception as e:
            await print(e)
                    
                    
#TODO: make a command to check # of credits left

if __name__ == '__main__':
    bot.run(TOKEN)
