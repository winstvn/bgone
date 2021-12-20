import io
import typing

import discord
import requests
from api_key_list import api_key_list
from config import API_URL


def remove_bg_from_img(api_key: str, img_url: str) -> requests.Response:
    """Removes the background from the image in the url and returns the response 
    object. If a bg_img_url is given, then replace the background with the 
    background image.

    Args:
        api_key (str): the API key to use
        img_url (str): the url containing the image to process

    Returns:
        requests.Response: the response from the call
    """
    headers = {'X-Api-Key': api_key}

    data = {'image_url': img_url,
            'crop': True}

    return requests.post(API_URL + '/removebg', headers=headers, data=data, stream=True)


def byte_to_discord_file(obj: bytes) -> discord.File:
    """Converts the bytes object to a discord file.

    Args:
        obj (bytes): the byte object to be converted

    Returns:
        discord.File: a discord file containing the byte object
    """
    obj = io.BytesIO(obj)
    obj.name = 'bgone_result.png'
    return discord.File(obj)


def get_message_img_url(msg: discord.Message) -> typing.Union[str, None]:
    """Returns the first valid image url in the message or None if one cannot 
    be found.

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


def validate_response(response: requests.Response) -> typing.Union[str, None]:
    """Returns None if response status code is ok, otherwise return a customized
    error message.

    Args:
        response (requests.Response): [description]

    Returns:
        typing.Union[str, None]: [description]
    """
    if response.status_code == requests.codes.ok:
        return None

    if response.status_code == 400:
        err_msg = 'Invalid parameters or the foreground cannot be detected.'
    elif response.status_code == 402:
        err_msg = 'Out of API credits!'
    elif response.status_code == 429:
        err_msg = 'Rate limit exceeded. Please try again later.'
    else:
        err_msg = 'Uncaught exception'
    return err_msg


async def remove_bg(ctx, api_keys: api_key_list, url: str) -> None:
    """Attempts to remove the background from the image given in the url.

    Args:
        ctx ([type]): The discord context object 
        api_keys (api_key_list): An api_key_list object
        url (str): The url containing the image to be processed
    """    
    if api_keys.curr_key is not None:
        response = remove_bg_from_img(api_keys.curr_key, url)
        err_msg = validate_response(response)
        if err_msg is None:
            await ctx.send(file=byte_to_discord_file(response.content))
            api_keys.use_key()
        else:
            await ctx.send(err_msg)
    else:
        await ctx.send('Out of API credits!')
