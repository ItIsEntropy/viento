class APIError(Exception):
    '''
    Something went wrong with the weather API
    '''
    # TODO: flesh out
    pass

class APILimitError(APIError):
    '''
    We have reached the API limit, inform user/admin
    '''
    # TODO: flesh out
    pass