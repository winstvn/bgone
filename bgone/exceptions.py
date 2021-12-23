from discord.ext.commands.converter import EmojiConverter


class OutOfCreditsException(Exception):
    '''Out of credits for remove.bg API'''
    pass

class RemovebgHTTPException(Exception):    
    '''HTTP Error returned from remove.bg API'''
    pass

class ImgNotInHistoryException(Exception):
    '''An image URL was not found in message history'''
    pass

class NotAnImageUrl(Exception):
    '''The URL did not contain an image'''
    pass
