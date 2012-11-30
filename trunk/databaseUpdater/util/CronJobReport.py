'''
    An object to model a report for a cron job
    
    Author: Andrew Oberlin
    Date: August 31, 2012
'''
import time

ENDL = '\n'
class CronJobReport:
    '''
        Constructor for this report
    '''
    def __init__(self, jobName):
        self.jobName = jobName
        self.errors = ''
        self.log = ''
        self.header = ''
        self.footer = ''
        self.__initializeReportHeader()
        
    '''
        Creates the header for this report
    '''
    def __initializeReportHeader(self):
        self.startTime = time.asctime( time.localtime(time.time()) )
        self.header += '#######################################################' + ENDL + ENDL
        
        self.header += 'Cron Job Name: ' + self.jobName + ENDL
        self.header += 'Date/Time (EST): ' + self.startTime + ENDL + ENDL
        
        self.header += '#######################################################' + ENDL + ENDL
    
    '''
        Adds an error message to the report
    '''    
    def addError(self, e, customMessage=None):
        errorTime = time.asctime( time.localtime(time.time()) )
        self.errors += '\tERROR ' + errorTime + ': ' + str(e) + ENDL
        if (customMessage):
            self.errors += '\t\tMessage: ' + customMessage + ENDL
        self.errors += ENDL
        
    
    '''
    
    '''
    def addLogEntry(self, message):
        self.log += message + ENDL + ENDL
        
    '''
    
    '''
    def finalize(self, success):
        self.footer += ''
        print self.header
        print '---------------------- ERROR REPORT ----------------------' + ENDL
        print self.errors + ENDL
        print '---------------------- LOG REPORT ----------------------' + ENDL
        print self.log + ENDL
        print self.footer