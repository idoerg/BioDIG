import taxon_home.views.util.ErrorConstants as Errors

'''

'''
class WebServiceObject:
    '''
        Constructs the default web service object for returning
    '''    
    def __init__(self):
        self.obj = {}
        self.fields = None
        self.errorObj = Errors.WebServiceException('', 200)
        self.error = False
        
    '''
        Puts a value into the object
        
        @param key: Key for adding to the inner object
        @param obj: Dictionary to add to this object
    '''
    def put(self, key, obj):
        if (self.fields == None or key in self.fields):
            self.obj[key] = obj
        
    '''
        Sets this web service to be errored
        
        @param message: Error message for this error
        @param code: HTTP code for this error (default 404) 
    '''
    def setError(self, errorObj):
        self.errorObj = errorObj
        self.error = True
    
    '''
        Checks to see if this object is currently errored
    '''
    def isError(self):
        return self.error
    
    '''
    
    '''
    def getErrorMessage(self):
        return self.errorObj.getMessage()
        
    
    '''
        Returns the HTTP code for this request
    '''
    def getCode(self):
        return self.errorObj.getCode()
        
    '''
        Gets the error object
    '''
    def getError(self):
        return self.errorObj
    
    '''
        Gets the dictionary for returning to the user
    '''
    def getObject(self):
        if (not self.isError()):
            return self.obj
        else:
            return {
                'status' : self.getCode(),
                'message' : self.getErrorMessage()
            }
            
    '''
        Says whether this metadata allows a certain field
    '''
    def allowsField(self, field):
        return self.fields == None or field in self.fields
            
            
    '''
        Limits the fields that can be added to this object
    '''
    def limitFields(self, fields):
        if (fields != None):
            self.fields = set(fields)

class WebServiceArray(WebServiceObject):
    '''
    
    '''
    def __init__(self):
        self.obj = []
        self.fields = None
        self.errorObj = Errors.WebServiceException('', 200)
        self.error = False
        
    def put(self, obj):
        self.obj.append(obj)
        
def LimitDict(fields, initialDict):
    limitDict = {}
    if fields and len(fields) > 0:
        fields = set(fields)
    else:
        fields = None
        
    for key, value in initialDict.iteritems():
        if (fields == None or key in fields):
            limitDict[key] = value
    
    return limitDict
            
            
            
            
        