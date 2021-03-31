from base64 import b64encode
import os
import random
import typing
import asyncio

import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./env/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('REMOVE_BG_API_KEY')
REMOVE_BG_ENDPOINT = 'https://api.remove.bg/v1.0/removebg'

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


def remove_bg_from_img(img_url: str, bg_img_url: str = '') -> bytes:
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
    
    return response.content


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='rm-bg')
async def rm_bg(ctx, url: typing.Optional[str] = None):
    await ctx.send(f'You passed {" ".join(args)}')


if __name__ == '__main__':
    # bot.run(TOKEN)
