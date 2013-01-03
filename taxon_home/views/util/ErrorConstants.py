'''
         ---------------------------------------------------------
                        Constants for Web Services
         ---------------------------------------------------------

'''
class WebServiceConstant:
    '''
        Creates the constant
    '''
    def __init__(self, message, code):
        self.code = code
        self.message = message
        
    '''
        Returns the error messages
    '''
    def getMessage(self):
        return self.message
    
    '''
        Returns the error code for HTTP
    '''
    def getCode(self):
        return self.code
               

INVALID_IMAGE_KEY = WebServiceConstant('Invalid Image Key Provided', 404)
NO_IMAGE_KEY = WebServiceConstant('No Image Key Provided', 400)
INVALID_TAG_GROUP_KEY = WebServiceConstant('Invalid Tag Group Key Provided', 404)
NO_TAG_GROUP_KEY = WebServiceConstant('No Tag Group Key Provided', 400)
NO_TAG_KEY = WebServiceConstant("No Tag Key Provided", 400)
INVALID_TAG_KEY = WebServiceConstant("Invalid Tag Key Provided", 404)
AUTHENTICATION = WebServiceConstant("You are not authorized to view that information.", 401)

class InvalidMethodConstant(WebServiceConstant):
    def setMethod(self, method):
        self.method = method
        return self
        
    def getMessage(self):
        return self.message % self.method

INVALID_METHOD = InvalidMethodConstant("This method %s is not supported by this section of the API" , 405)