from rest_framework.exceptions import APIException

class BadRequestException(APIException):
    '''
        Bad Request Exception.
    '''
    status_code = 400
    default_detail = "A Bad Request was made for the API. Revise input parameters."

class UserDoesNotExist(APIException):
    '''
        User does not exist error.
    '''
    status_code = 404
    default_detail = "The user_id provided does not refer to a user in this database."

class PublicationRequestDoesNotExist(APIException):
    '''
        PublicationRequest does not exist error.
    '''
    status_code = 404
    default_detail = "The publication_request_id provided does not refer to an publication request in this database."

class ImageDoesNotExist(APIException):
    '''
        Image does not exist error.
    '''
    status_code = 404
    default_detail = "The image id provided does not refer to an image in this database."

class OrganismDoesNotExist(APIException):
    '''
        Organism does not exist error.
    '''
    status_code = 404
    default_detail = "The organism_id provided does not refer to an organism in this database."

class ImageOrganismDoesNotExist(APIException):
    '''
        ImageOrganism does not exist error.
    '''
    status_code = 404
    default_detail = "The organism_id provided is not associated with the image_id provided in this database."

class TagGroupDoesNotExist(APIException):
    '''
        Tag Group does not exist error.
    '''
    status_code = 404
    default_detail = "The tag group id provided does not refer to a tag group in this database."

class TagDoesNotExist(APIException):
    '''
        Tag does not exist error.
    '''
    status_code = 404
    default_detail = "The tag id provided does not refer to a tag in this database."

class GeneLinkDoesNotExist(APIException):
    '''
        Gene Link does not exist error.
    '''
    status_code = 404
    default_detail = "The gene link id provided does not refer to a gene link in this database."

class FeatureDoesNotExist(APIException):
    '''
        Feature does not exist error.
    '''
    status_code = 404
    default_detail = "The information provided did not match any feature in this database."

class FeatureTypeDoesNotExist(APIException):
    '''
        Feature type does not exist error.
    '''
    status_code = 404
    default_detail = "The type indicated for the feature does not exist in this database or is invalid."

class CvDoesNotExist(APIException):
    '''
        Cv does not exist error.
    '''
    status_code = 404
    default_detail = "The requested controlled vocabulary does not seem to be installed in Chado. Please consult your system administrator."

class MultipleFeaturesReturned(APIException):
    def __init__(self, data):
        self.default_detail = data

    '''
        Error for when multiple features are returned when adding a gene link.
    '''
    status_code = 404

class DatabaseIntegrity(APIException):
    '''
        An error occurred while trying to write to the database.
    '''
    status_code = 500
    default_detail = 'An error occurred while trying to write to the database.'

class NotImplementedException(APIException):
    '''
        An error to throw when a form/view has not been implemented yet.
    '''
    status_code = 404
    default_detail = 'This method has not been implemented, and is thus missing.'

class OrthologDoesNotExist(APIException):
   '''
	TC_num does not exist
   '''
   status_code = 404
   default_deatil = 'An error occured because TC number does not exist in file.'


