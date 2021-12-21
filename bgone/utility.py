import io
import typing
import json

import discord
import requests
from PIL import Image
from requests.exceptions import HTTPError

from api_key_list import api_key_list
from config import API_URL


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

    data = {'image_url': img_url,
            'crop': True}

    return requests.post(f'{API_URL}/removebg', headers=headers, data=data)


def crop_to_bbox(im_bytes: bytes) -> bytes:
    """Crop empty regions from the image byte array.

    Args:
        im_bytes (bytes): Byte array representation of the image.

    Returns:
        bytes: Byte array representation of the cropped image.
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
        msg (discord.Message): A discord.Message object.

    Returns:
        str|None: The first valid image url in the message or None.
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


def validate_response(response: requests.Response) -> None:
    """Returns None if response status code is ok, otherwise raise an HTTPerror
    using the error message from the response.

    Args:
        response (requests.Response): The response from remove.bg API call.

    Raises:
        HTTPError: An HTTPError containing the error message returned.
    """    
    if response.status_code != requests.codes.ok:
        error = json.loads(response.text)
        raise HTTPError(error['errors'][0]['title'])
    
    return


def remove_bg(api_keys: api_key_list, url: str) -> None:
    """Attempts to remove the background from the image given in the url.

    Args:
        api_keys (api_key_list): An api_key_list object.
        url (str): The url containing the image to be processed.
    """
    if api_keys.curr_key is None:
        raise Exception('Out of API credits!')
    
    response = remove_bg_from_img(api_keys.curr_key, url)
    try:
        validate_response(response)
        api_keys.use_key()
        return crop_to_bbox(response.content)
    except HTTPError as e:
        raise e
