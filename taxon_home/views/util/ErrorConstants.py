from renderEngine.WebServiceException import WebServiceException, CustomWebServiceException
'''
         ---------------------------------------------------------
                        Constants for Web Services
         ---------------------------------------------------------

'''
INVALID_IMAGE_KEY = WebServiceException('Invalid Image Key Provided', 404)
NO_IMAGE_KEY = WebServiceException('No Image Key Provided', 400)
INVALID_TAG_GROUP_KEY = WebServiceException('Invalid Tag Group Key Provided', 404)
NO_TAG_GROUP_KEY = WebServiceException('No Tag Group Key Provided', 400)
NO_TAG_KEY = WebServiceException("No Tag Key Provided", 400)
NO_GENE_LINK_KEY = WebServiceException("No Gene Link Key Provided", 400)
INVALID_TAG_KEY = WebServiceException("Invalid Tag Key Provided", 404)
INVALID_GENE_LINK_KEY = WebServiceException("Invalid Gene Link Key Provided", 404)
AUTHENTICATION = WebServiceException("You are not authorized to view that information", 401)
INTERNAL_ERROR = WebServiceException("An unexpected error has occurred with your input. Please email the administrator of this BioDIG dite for help.", 500)
NOT_MODIFIED = WebServiceException("The requested object has not been modified", 200)

INVALID_METHOD = CustomWebServiceException("This method %s is not supported by this section of the API" , 405)
MISSING_PARAMETER = CustomWebServiceException("Missing required parameter: %s", 400)
INVALID_PARAMETER = CustomWebServiceException("Invalid input for parameter: %s", 404)
INVALID_SYNTAX = CustomWebServiceException("Incorrect syntax for argument: %s", 400)
INTEGRITY_ERROR = CustomWebServiceException("Database transaction error. Message: %s", 500)