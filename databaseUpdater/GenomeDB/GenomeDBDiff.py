'''
    Used as a data structure for performing and holding the information
    resulting from doing a difference operation on the NEW and OLD directory
    of the mycoplasma genomic hard database
    
    Author: Andrew Oberlin
    Date: September 4, 2012
'''
import os
from filecmp import cmp as diff
import GenomeDBUtil
from django.conf import settings 

class GenomeDBDiff:
    '''
        Initializes and runs the difference operation on the directory
    '''
    def __init__(self, NEW_GENOMIC_DATA_DIR, CUR_GENOMIC_DATA_DIR, report):
        self.NEW_GENOMIC_DATA_DIR = NEW_GENOMIC_DATA_DIR
        self.CUR_GENOMIC_DATA_DIR = CUR_GENOMIC_DATA_DIR
        self.report = report
        self.__diff()
        
    '''
        Finds the difference between the old genomic data directory
        and the current genomic data directory
    '''
    def __diff(self):
        allNewDirs = set(os.walk(self.NEW_GENOMIC_DATA_DIR).next()[1])
        allCurrentDirs = set(os.walk(self.CUR_GENOMIC_DATA_DIR).next()[1])

        needComparison = allNewDirs.intersection(allCurrentDirs)
        
        # find directories that need to be copied over to the new directories
        self.deletedOrganisms =list(allCurrentDirs.difference(allNewDirs))
        
        # find directories that are new to the data set
        self.newOrganisms = list(allNewDirs.difference(allCurrentDirs))
        
        # for subdirectories and file in suspect directories
        self.fastaFiles = {
            'unchanged' : [],
            'changed'   : []
        }
        
        self.gffFiles = {
            'unchanged' : [],
            'changed'   : []
        }
        
        self.gbkFiles = {
            'unchanged' : [],
            'changed'   : []
        }
        
        for mycoDir in needComparison:
            # finds all the files in this subdirectory of both the new and old
            newMycoFiles = set(os.walk(self.NEW_GENOMIC_DATA_DIR + mycoDir).next()[2])
            oldMycoFiles = set(os.walk(self.CUR_GENOMIC_DATA_DIR + mycoDir).next()[2])          
                        
            # finds the files that are the same in both directories
            filesToCompare = newMycoFiles.intersection(oldMycoFiles)
            for fileComp in filesToCompare:
                extensionPlace = fileComp.rfind(".")
                extension = fileComp[extensionPlace + 1:]
                # only gbk and gff should be considered
                # (they should also be the only ones downloaded in the first place)
                if (extension == 'gbk'):
                    if (self.__compareGenbank(mycoDir, fileComp)):
                        self.gbkFiles['changed'].append(mycoDir + '/' + fileComp)
                    else:
                        self.gbkFiles['unchanged'].append(mycoDir + '/' + fileComp)
                elif (extension == 'gff'):
                    if (self.__compareGFFOrFasta(mycoDir, fileComp)):
                        self.gffFiles['changed'].append(mycoDir + '/' + fileComp)
                    else:
                        self.gffFiles['unchanged'].append(mycoDir + '/' + fileComp)
                elif(extension == 'ffn' or extension == 'faa'):
                    if (self.__compareGFFOrFasta(mycoDir, fileComp)):
                        self.fastaFiles['changed'].append(mycoDir + '/' + fileComp)
                    else:
                        self.fastaFiles['unchanged'].append(mycoDir + '/' + fileComp)
                else:
                    self.report.addLogEntry("File " + mycoDir + '/' + fileComp + " was downloaded from NCBI, but the extension is unrecognized..")
                    
    '''
        Compares two genbank files with the same name in order to check the
        date given in the genbank file as verification that anything has changed
        
        @param mycoDir: The subdirectory in which this file resides
        @param fileComp: A file to be compared between new version and old
        
        @return: Returns true if the files are different
    '''
    def __compareGenbank(self, mycoDir, fileComp):
        newFile = open(self.NEW_GENOMIC_DATA_DIR + mycoDir + '/' + fileComp)
        newDate = newFile.readline().split()[-1]
        newFile.close()
        
        oldFile = open(self.CUR_GENOMIC_DATA_DIR + mycoDir + '/' + fileComp)
        oldDate = oldFile.readline().split()[-1]
        oldFile.close()
        
        return oldDate != newDate
    
    '''
        Compares two GFF files with the same name in order to check the
        date given in the GFF file as verification that anything has changed
        
        @param mycoDir: The subdirectory in which this file resides
        @param fileComp: A file to be compared between new version and old
        
        @return: Returns true if the files are different
    '''
    def __compareGFForFasta(self, mycoDir, fileComp):
        return not diff(
            self.NEW_GENOMIC_DATA_DIR + mycoDir + '/' + fileComp,
            self.CUR_GENOMIC_DATA_DIR + mycoDir + '/' + fileComp
        )  

    '''
        Returns a list of all the unchanged fasta files between the
        old and new data sets
    '''
    def getUnchangedFastaFiles(self):
        return self.fastaFiles['unchanged']
    
    '''
        Returns a list of all the changed fasta files between the
        old and new data sets
    '''
    def getChangedFastaFiles(self):
        return self.fastaFiles['changed']
    
    '''
        Returns a list of all the unchanged gff files between the
        old and new data sets
    '''
    def getUnchangedGffFiles(self):
        return self.gffFiles['unchanged']
    
    '''
        Returns a list of all the changed gff files between the
        old and new data sets
    '''
    def getChangedGffFiles(self):
        return self.gffFiles['changed']
    
    '''
        Returns a list of all the unchanged genbank files between the
        old and new data sets
    '''
    def getUnchangedGenbankFiles(self):
        return self.gffFiles['unchanged']
    
    '''
        Returns a list of all the changed genbank files between the
        old and new data sets
    '''
    def getChangedGenbankFiles(self):
        return self.gffFiles['changed']
    
    '''
        Returns the list of directories for the newly added organisms
    '''
    def getNewOrganisms(self):
        return self.newOrganisms
    
    '''
        Returns the list of directories for the deleted organisms
    '''
    def getDeletedOrganisms(self):
        return self.deletedOrganisms
        
if (__name__ == '__main__'):
    dbDiff = GenomeDBDiff(
        '/var/www/BioDIG/taxon_home/static/genomicFiles/new/',
        '/var/www/BioDIG/taxon_home/static/genomicFiles/current/'
    )
    
    print 'Changed files: ' + str(dbDiff.changedFiles)
    print 'New directories in suspect: ' + str(dbDiff.newDirsInSuspect)
    print 'Old directories in suspect: ' + str(dbDiff.oldDirsInSuspect)
    print 'Old directories not in new: ' + str(dbDiff.oldDirsNotInNew)
    print 'New directories not in old: ' + str(dbDiff.newDirsNotInOld)
                    