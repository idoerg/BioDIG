'''
    Utility functions that can be reused across the website such as running formatdb
    on a new fasta file or hooking up a gff file to Chado and GBrowse. 
    
    Author: Andrew Oberlin
    Date: September 10, 2012
'''
from databaseUpdater.util.SubProcess import runProgram
import shutil
from BCBio.GFF import GFFExaminer

import os
import sys

path = '/var/www/BioDIG'
otherpath = '/var/www'
sys.path.append(path)

sys.path.append(otherpath)

os.environ['DJANGO_SETTINGS_MODULE'] = 'BioDIG.settings'

from django.conf import settings
from taxon_home.models import Organism
from django.core.exceptions import ObjectDoesNotExist

GBROWSE_DIR='/etc/gbrowse2/'

'''
    Runs formatdb on the fasta file given. The output of the formatdb operation
    will be stored in either loc + '/proteinDB' or loc + '/nucleotideDB'
    
    @param fastaName: the basename of the fasta file
    @param loc: the organism directory of the fasta file
    @param protein: whether or not this is a protein database
''' 
def runFormatDB(fastaName, loc, protein=False):
        option = 'F'
        dbDir = 'nucleotideDB'
        if (protein):
            option = 'T'
            dbDir = 'proteinDB'
            
        # must move the file into the new directory to correctly place the
        # formatdb information
        newLoc = os.path.join(loc, dbDir)
        originalFile = os.path.join(loc, fastaName)
        newFile = os.path.join(newLoc, fastaName)
        
        os.mkdir(newLoc)
        shutil.move(originalFile, newLoc)
             
        args = ['-p', option, '-i', newFile]
        runProgram('formatdb', args)
        
        shutil.move(newFile, loc)

'''

'''
def addOrganismToChado(gff, organismName):
    try:                   
        organism = Organism.objects.get(common_name=organismName)                  
    except ObjectDoesNotExist:
        organisms = Organism.objects.order_by('-organism_id')
        nextId = 0
        if (len(organisms) > 0):  
            nextId = organisms[0].organism_id + 1
        organismNameArr = organismName.split()
        if (len(organismNameArr) < 2):
            raise Exception('Organism name does not have enough tokens to find a genus and species: ' + organismName)
        genus = organismNameArr[0]
        species = organismNameArr[1]
        organism = Organism(organism_id=nextId, abbreviation=genus[0] + '. ' + species, genus=genus, species=species, common_name=organismName)                    
        organism.save()
            
    args= ['--organism', organismName, "--gfffile", gff, " ", settings.DATABASES['default']['NAME'], "--dbuser", settings.DATABASES['default']['USER'], "--dbpass", settings.DATABASES['default']['PASSWORD'], "--random_tmp_dir"]
    runProgram('gmod_bulk_load_gff3.pl', args)
    
    return nextId
        
'''
    Changes a current entry in GBrowse for this gffFile
    
    @param gffFile: the absolute path of the gff file
    @param dbName: the basename of the database name file
    @param organismName: the name of the organism being added
'''
def editGBrowseEntry(gffFile, dbName, organismDir, organismName):
    examiner = GFFExaminer()
    gffHandle = open(gffFile)
    landmark = examiner.available_limits(gffHandle)['gff_id'].keys()[0][0]
    gbrowseConf = os.path.join(GBROWSE_DIR, organismDir.lower() + '.conf')
    if (os.path.isfile(gbrowseConf)):
        conf = open(gbrowseConf, 'r')
        confLines = conf.readlines()
        conf.close()
        changedInitial = False
        changedExample = False
        for(counter, line) in enumerate(confLines):
            if (line[:15] == 'initial landmark'):
                initialLandmarkArr = line.split("=")
                initialLandmarkArr[1] = ' ' + landmark + ':1..50,000\n'
                confLines[counter] = '='.join(initialLandmarkArr)
                changedInitial = True
            elif(line[:8] == 'examples'):
                exampleArr = line.split("=")
                exampleArr[1] = ' ' + landmark + '\n'               
                confLines[counter] = '='.join(exampleArr)
                changedExample = True
            if (changedInitial and changedExample):
                break
        conf = open(gbrowseConf, 'w+b')
        conf.writelines(confLines)
        conf.close()             
    else:
        dataSource = os.path.join(os.path.dirname(gffFile), dbName)
        createNewGBrowseEntry(landmark, dataSource, organismDir, organismName)
        
'''
    Uses the template file in the GBrowse directory to create a new
    GBrowse configuration file for this organism
    
    @param landmark: the initial landmark of the gff for GBrowse
    @param dataSource: the absolute path of the data source (sqlite database)
    @param organismName: the name of the organism being added to GBrowse
'''
def createNewGBrowseEntry(landmark, dataSource, organismDir, organismName, uri):
    try:
        templateConfFile = open(os.path.join(GBROWSE_DIR, 'taxonTemplate.conf'), 'r')
        templateConf = templateConfFile.readlines()
        templateConfFile.close()
    except:
        raise GBrowseEntryCreationException("Could not find the template file for adding the new entry to GBrowse")
    
    changedDBArgs = False
    changedInitial = False
    changedExample = False
    for(counter, line) in enumerate(templateConf):
        if (line[:16] == 'initial landmark'):
            print line[:16]
            initialLandmarkArr = line.split("=")
            initialLandmarkArr[1] = ' ' + landmark + ':1..50,000\n'
            templateConf[counter] = '='.join(initialLandmarkArr)
            changedInitial = True
        elif(line[:8] == 'examples'):
            exampleArr = line.split("=")
            exampleArr[1] = ' ' + landmark + '\n'               
            templateConf[counter] = '='.join(exampleArr)
            changedExample = True
        else:
            dataSourceLoc = line.find('-dsn')
            if (dataSourceLoc != -1):
                dataSourceLoc += 4
                templateConf[counter] = line[:dataSourceLoc] + " '" + dataSource + "'\n"
                changedDBArgs = True
        if (changedInitial and changedExample and changedDBArgs):
            break

    try:
        newConf = open(os.path.join(GBROWSE_DIR, organismDir.lower() + ".conf"), 'w')
        newConf.writelines(templateConf)
        newConf.close()
    except:
        raise GBrowseEntryCreationException("Could not create a new configuration file for " + organismName)

    try:
        gbrowseConf = open(os.path.join(GBROWSE_DIR, 'GBrowse.conf'), 'a')
        appendStr = "\n[" + str(uri) + "]\ndescription  = " + organismName + "\npath         = " + organismDir.lower() + ".conf\n"

        gbrowseConf.write(appendStr)
        gbrowseConf.close()
    except:
        raise GBrowseEntryCreationException("Could not add the entry for " + organismName + " to the main GBrowse configuration.")

class GBrowseEntryCreationException(Exception):
    pass
