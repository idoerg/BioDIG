'''
    An object to handle creating subprocesses in a safe way so that
    no one gets access to a shell
    
    Author: Andrew Oberlin
    Date: September 7, 2012
'''
import subprocess

class SubProcessOutput:
    '''
        Constructs the output for sub process
    '''
    def __init__(self, returnCode, output):
        self.returnCode = returnCode
        self.output = output
    
    '''
        Determines whether this process was run successfully or if it was an
        error
    '''
    def isError(self):
        return self.returnCode != 0 
    
    '''
        Gets the error messages caught by this process printed
        to stderr
    '''
    def getErrorMessage(self):
        return self.output[1]
    
    '''
        Gets the messages caught by this process printed
        to stdout
    '''
    def getMessage(self):
        return self.output[0]
    
    
'''
    Runs a program using execvp, waits for the process to return and returns the output
    This command should not be vulnerable to shell injection
    
    @param name: the name of the program to run
    @param args: the arguments to the program to be run
'''
def runProgram(name, args):
    args.insert(0, name)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()
    
    return SubProcessOutput(proc.returncode, output)
    