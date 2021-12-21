import io
import json
import typing

import discord
import requests
from PIL import Image
from requests.exceptions import HTTPError

from api_key_list import api_key_list
from config import API_URL
from exceptions import *


def remove_bg_from_img(api_key: str, img_url: str) -> requests.Response:
    """Removes the background from the image in the url by a POST request to
    remove.bg API and returns the response object.

    Args:
        api_key (str): The API key to use.
        img_url (str): The url containing the image to process.

    Returns:
        requests.Response: The response from the POST request.
    """
    headers = {'X-Api-Key': api_key}

    data = {
        'image_url': img_url,
        'crop': True
        }

    return requests.post(f'{API_URL}/removebg', headers=headers, data=data)


def crop_to_bbox(im_bytes: bytes) -> bytes:
    """Crop empty regions from the image byte representation.

    Args:
        im_bytes (bytes): Byte representation of the image.

    Returns:
        bytes: Byte representation of the cropped image.
    """    
    result_img_btye = io.BytesIO()
    
    with Image.open(io.BytesIO(im_bytes)) as im:
        bbox = im.getbbox()
        im = im.crop(bbox)
        im.save(result_img_btye, format='PNG')
        
    return result_img_btye.getvalue()


def byte_to_discord_file(obj: bytes) -> discord.File:
    """Converts the bytes object to a discord file.

    Args:
        obj (bytes): The byte object to be converted.

    Returns:
        discord.File: A discord file containing the byte object.
    """
    obj = io.BytesIO(obj)
    obj.name = 'bgone_result.png'
    return discord.File(obj)


def extract_message_img_url(msg: discord.Message) -> typing.Union[str, None]:
    """Returns the first valid image url in the message or None if one cannot 
    be found.

    Args:
        msg (Message): A Message object.

    Returns:
        str | None: The first valid image url in the message or None.
    """
    # check if the image url is in the message contents first
    if msg.clean_content[-4:].lower() in ['.jpg', '.png', 'jpeg']:
        return msg.clean_content

    # check for an image url in the attachments afterwards
    for attachment in msg.attachments:
        if attachment.url[-4:].lower() in ['.jpg', '.png', 'jpeg']:
            return attachment.url

    # return None if no image urls were found
    return None


async def find_img_url_in_history(ctx, limit: int) -> str:
    async for msg in ctx.channel.history(limit=limit):
        url = extract_message_img_url(msg)
        if url is not None:
            return url
    else:
        raise ImgNotInHistoryException(f'Could not detect an image in the last {limit} messages!')


def validate_response(response: requests.Response) -> None:
    """Returns None if response status code is ok, otherwise raise an HTTPerror
    using the error message from the response.

    Args:
        response (Response): The response from remove.bg API call.

    Raises:
        HTTPError: An HTTPError containing the error message returned.
    """    
    if response.status_code != requests.codes.ok:
        raise HTTPError(response)
    
    return


def remove_bg(api_keys: api_key_list, url: str) -> bytes:
    """Attempts to remove the background from the image given in the url.

    Args:
        api_keys (api_key_list): An api_key_list object.
        url (str): The url containing the image to be processed.

    Raises:
        OutOfCreditsException: Raised when there are no more available API keys.
        RemovebgHTTPException: Raised when there was an HTTP error from remove.bg API.

    Returns:
        bytes: A byte representation of the image with background removed.
    """
    if api_keys.curr_key is None:
        raise OutOfCreditsException('Out of API credits!')
    
    response = remove_bg_from_img(api_keys.curr_key, url)
    try:
        validate_response(response)
        api_keys.use_key()
        return crop_to_bbox(response.content)
    except HTTPError as e:
        error = json.loads(response.text)
        error_msg = error['errors'][0]['title']
        raise RemovebgHTTPException(error_msg) from e
