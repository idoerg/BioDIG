class WebServiceException(Exception):
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

class CustomWebServiceException(WebServiceException):
    def setCustom(self, custom):
        self.custom = custom
        return self
        
    def getMessage(self):
        if self.custom or self.custom == 0:
            return self.message % self.custom
        else:
            return self.message % 'Unknown'    

THROTTLED = CustomWebServiceException("Too many requests, please try again in: %s minute(s)", 429)