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
    detail = "The image id provided does not refer to an image in this database."
    
class TagGroupDoesNotExist(APIException):
    '''
        Tag Group does not exist error.
    '''
    status_code = 404
    detail = "The tag group id provided does not refer to a tag group in this database."
    
class TagDoesNotExist(APIException):
    '''
        Tag does not exist error.
    '''
    status_code = 404
    detail = "The tag id provided does not refer to a tag in this database."
    
class DatabaseIntegrity(APIException):
    '''
        An error occurred while trying to write to the database.
    '''
    status_code = 500
    detail = 'An error occurred while trying to write to the database.'
    
class NotImplementedException(APIException):
    '''
        An error to throw when a form/view has not been implemented yet.
    '''
    status_code = 404
    detail = 'This method has not been implemented, and is thus missing.'