class OutOfCreditsException(Exception):
    '''Out of credits for remove.bg API'''
    pass

class RemovebgHTTPException(Exception):    
    '''HTTP Error returned from remove.bg API'''
    pass
