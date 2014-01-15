from rest_framework.exceptions import APIException

class BadRequestException(APIException):
    '''
        Bad Request Exception.
    '''
    status_code = 400
    detail = "A Bad Request was made for the API. Revise input parameters."
    
class ImageDoesNotExist(APIException):
    '''
        Image does not exist error.
    '''
    status_code = 404
    detail = "The image key provided does not refer to an image in this database."
    
class DatabaseIntegrity(APIException):
    '''
        An error occurred while trying to write to the database.
    '''
    status_code = 500
    detail = 'An error occurred while trying to write to the database.'