'''
	Script to update the database to be run as a cron job
	
	Author: Andrew Oberlin
	Date: August 28, 2012
'''
import ftplib
import re
import sys
sys.path.append('/var/www/mycoplasma_site/')
from databaseUpdater.util.CronJobReport import CronJobReport
import os
import shutil
from GenomeDBDiff import GenomeDBDiff
import GenomeDBUtil
from databaseUpdater.util.SubProcess import runProgram
from Bio import GenBank
from BCBio.GFF import GFFExaminer
from django.conf import settings
from GFFRewriter import GFFRewriter

NCBI = 'ftp.ncbi.nlm.nih.gov'
MYCOPLASMA_DIR = 'genomes/Bacteria'
NEW_GENOMIC_DATA_DIR = '/var/www/mycoplasma_site/mycoplasma_home/static/genomicFiles/new/'
CUR_GENOMIC_DATA_DIR = '/var/www/mycoplasma_site/mycoplasma_home/static/genomicFiles/current/'
ACCEPTED_FILE_FORMATS = ['gbk', 'faa', 'ffn']

class GenomeDBUpdater:
	'''
		Creates the GenomeUpdater object
		to allow for its methods to be used
	'''
	def __init__(self):
		self.report = CronJobReport('Mycoplasma - Genome Database Updater')

		
	'''
		The function that should be run to check if an update on 
		the local mirror of NCBI's database needs to be performed. 
		If so, it will execute that update script and the database
	'''
	def update(self):
		# connect to the location of the Mycoplasma genomes
		#self.__connectToNCBI()
		
		# get the new files list of this directory
		#newMycoDirs = self.__findMycoplasmaDirs()
			
		# download the new Mycoplasma files
		#self.__remoteSync(newMycoDirs)
		
		#self.ftp.quit()
		
		# perform a simple diff function to find files that have changed
		dbDiff = self.__findLocalDiffList()
		
		#self.__createGFFFiles(dbDiff.getNewOrganisms())
		
		#self.report.addLogEntry('New organisms found: ' + str(dbDiff.getNewOrganisms()))
		
		# process the files that have changed for Blast results
		#self.__processFastaFilesNotNew(dbDiff.getUnchangedFastaFiles(), dbDiff.getChangedFastaFiles())
		
		# process the files that have changed for GBrowse and Chado updates
		#self.__processGffFilesNotNew(dbDiff.getChangedGffFiles())
		
		# process the files that a
		self.__processGffFilesNew(dbDiff.getNewOrganisms())
		
		self.report.finalize(True)
				
	'''
		Connects to NCBI's ftp connection
	'''
	def __connectToNCBI(self):
		try:
			self.ftp = ftplib.FTP(NCBI)
			self.ftp.login()
			self.ftp.cwd(MYCOPLASMA_DIR)
		except Exception as e:
			self.report.addError(e, 'There was a problem connecting to NCBI: Update aborted..')
			self.report.finalize(False)
			sys.exit(1)

	'''
		Uses regex to find the dirs that start with Mycoplasma
		within the list given
		
		@param allDirs: a list of all the files in the directory searched
	'''
	def __findMycoplasmaDirs(self):
		mycoFiles = []
		try:
			allDirs = self.ftp.nlst()
			
			for curDir in allDirs:
				if (re.search('^Mycoplasma', curDir)):
					mycoFiles.append(curDir)
		
		except Exception as e:
			self.report.addError(e, 'There was a problem getting the list of directories in ' + 
				MYCOPLASMA_DIR + ': Update aborted..')
			self.report.finalize(False)
			sys.exit(1)
		
		return mycoFiles
	
	'''
		Gets the Mycoplasma files and creates them locally on the server for server
		operations to find a diff between the new files and the old files
		
		@param newMycoDirs: The dirs that need to be searched on the remote server and created here
	'''
	def __remoteSync(self, newMycoDirs):
		for (counter, mycoDir) in enumerate(newMycoDirs):
			fileList = []
			try:
				# change directory to next mycoplasma organism
				if (counter != 0):
					self.ftp.cwd('..')
					
				self.ftp.cwd(mycoDir)
				
				# find the gff and genbank files for this organism
				fileList = self.ftp.nlst()   
				
			except Exception as e:
				self.report.addError(e, 'Problem with remote directory: ' + str(mycoDir) + ', ignoring..')
				continue
			
			try:
				gbkGffFiles = []
				
				# get all files with gff or gbk extensions
				for filename in fileList:
					extensionPlace = filename.rfind(".")
					extension = filename[extensionPlace + 1:]
					if (extension in ACCEPTED_FILE_FORMATS):
						gbkGffFiles.append(filename)
				
				os.mkdir(NEW_GENOMIC_DATA_DIR + mycoDir)
				
				# download all the files over ftp for this directory
				for filename in gbkGffFiles:
					self.__download(filename, NEW_GENOMIC_DATA_DIR + mycoDir)
					
			except Exception as e:
				self.report.addError(e, 'Problem with local directory: ' + mycoDir + ', ignoring..')
				continue
			
	
	'''
		Downloads a file from the NCBI stores and saves it in the directory given locally
		
		@param filename: The remote filename to download (we assume that we have already changed into its directory)
		@param localFileLoc: The place locally to save the file being downloaded 
	'''
	def __download(self, filename, localFileLoc):
		try:
			outFile = open(localFileLoc + '/' + filename, 'w+b')
			self.ftp.retrbinary('RETR ' + filename, outFile.write)
			self.report.addLogEntry('Downloaded remote file ' + filename + ' to the new directory successfully...')
		except Exception as e:
			self.report.addError(e, 'Problem downloading file ' + filename + ' from NCBI, ignoring..')
			
	'''
		Finds a list of files that have changed since the last update of the
		database, which require this program's attention
	'''
	def __findLocalDiffList(self):
		return GenomeDBDiff(NEW_GENOMIC_DATA_DIR, CUR_GENOMIC_DATA_DIR, self.report)
	
	'''
		Moves the old directories that should not be deleted in the new
		
		@param unchanged: The list of files that have been unchanged since the last update
		@param changed: The list of files that have been changed since the last update
	'''
	def __processFastaFilesNotNew(self, unchanged, changed):
		for fasta in changed:
			extension = os.path.splitext(fasta)[1]
			fileDir = os.path.dirname(fasta)
			
			if (extension == 'ffn'):
				GenomeDBUtil.runFormatDB(os.path.basename(fasta), fileDir, NEW_GENOMIC_DATA_DIR, protein=False)
				self.report.addLogEntry('Created BLASTn database for ' + fasta + '(replaced old file)...')
			elif (extension == 'faa'):
				GenomeDBUtil.runFormatDB(os.path.basename(fasta), fileDir, NEW_GENOMIC_DATA_DIR, protein=True)
				self.report.addLogEntry('Created BLASTp database for ' + fasta + ' (replaced old file)...')
		
		for fasta in unchanged:
			fileDir = os.path.dirname(fasta)
			prefix = CUR_GENOMIC_DATA_DIR + fileDir
			
			extension = os.path.splitext(fasta)[1]
			
			if (extension == 'ffn'):
				# check to see if the nucleotideDB directory exists
				# for this organism already
				nucleotideDB = os.path.join(prefix, 'nucleotideDB')
				nucleotideExists = os.path.isdir(nucleotideDB)
				
				# since these are unchanged files we wish to simply move the old directories over
				# to save cpu time, if they do not exist previously then we will make them in the
				# new directory
				if (nucleotideExists):
					shutil.copytree(nucleotideDB, NEW_GENOMIC_DATA_DIR + fileDir)
				else:
					GenomeDBUtil.runFormatDB(os.path.basename(fasta), NEW_GENOMIC_DATA_DIR + fileDir, protein=False)
			elif(extension == 'faa'):			
				# check to see if the proteinDB directory exists
				# for this organism already
				proteinDB = os.path.join(prefix, 'proteinDB')
				proteinExists = os.path.isdir(proteinDB)
								
				# since these are unchanged files we wish to simply move the old directories over
				# to save cpu time, if they do not exist previously then we will make them in the
				# new directory
				if (proteinExists):
					shutil.copytree(proteinDB, NEW_GENOMIC_DATA_DIR + fileDir)
				else:
					GenomeDBUtil.runFormatDB(os.path.basename(fasta), fileDir, NEW_GENOMIC_DATA_DIR, protein=True)
	
	'''
		Adds the GFF files information to the GBrowse instance and then to
		Chado for overarching queries later on
	'''
	def __processGffFilesNotNew(self, changed):
		for gff in changed:
			loc = os.path.dirname(gff)
			dbName = os.path.splitext(os.path.basename(gff))[0] + '.db'
			dbName = os.path.join(loc, dbName)
			
			gffRewriter = GFFRewriter(filename=gff, outfile=gff+".sorted.prepared" , accession=genbank_id)
	
			gffRewriter.addUnknownCvTerms({
				'user' : settings.DATABASES['default']['USER'], 
				'password' : settings.DATABASES['default']['PASSWORD'], 
				'db' : settings.DATABASES['default']['NAME']
			})
		
			gffRewriter.addColor({
				'user' : settings.DATABASES['default']['USER'],
				'password' : settings.DATABASES['default']['PASSWORD'],
				'db' : 'MyGO'
			})
		
			error = gffRewriter.getError()
			
			# run the sqlite database loader to be able to add it to GBrowse
			# since the name should be preserved, no changes need to be made
			# to the GBrowse configuration file
			args = ['-a', 'DBI::SQLite', '-c', '-f', '-d', dbName, gff]
			runProgram('bp_seqfeature_load.pl', args)
			
			parser = GenBank.RecordParser()
			gbk = os.path.join(os.path.splitext(gff)[0], '.gbk')
			record = parser.parse(open(gbk))
			organismName = record.organism
			organismDir = os.path.basename(loc)
			
			GenomeDBUtil.editGBrowseEntry(gff, dbName, organismDir, organismName)
			
			# now edit the record in Chado
			args= ['--organism', organismName, "--gfffile", gff, "--dbname", settings.DATABASES['default']['NAME'], "--dbuser", settings.DATABASES['default']['USER'], "--dbpass", settings.DATABASES['default']['PASSWORD'], "--random_tmp_dir"]
			runProgram('gmod_bulk_load_gff3.pl', args)
	
	'''
		Adds new organisms to the Chado and GBrowse and creates the BLAST databases
	'''		
	def __processGffFilesNew(self, newOrganismDirs):
		for newOrganism in newOrganismDirs:
			# start by creating the BLAST database
			newOrganism = os.path.join(NEW_GENOMIC_DATA_DIR, newOrganism)
			print newOrganism
			organismFiles = os.walk(newOrganism).next()[2]
			faa = None
			ffn = None
			gff = None
			gbk = None
			for organismFile in organismFiles:
				extension = os.path.splitext(organismFile)[1]
				if (extension == '.ffn'):
					ffn = organismFile
				elif (extension == '.faa'):
					faa = organismFile
				elif (extension == '.gff'):
					gff = organismFile
				elif (extension == '.gbk'):
					gbk = organismFile
				if (faa and ffn and gff and gbk):
					break
			
			if (faa):
				GenomeDBUtil.runFormatDB(os.path.basename(faa), newOrganism, protein=True)
				self.report.addLogEntry('Ran formatdb successully on ' + faa)
			if (ffn):
				GenomeDBUtil.runFormatDB(os.path.basename(ffn), newOrganism, protein=False)
				self.report.addLogEntry('Ran formatdb successully on ' + ffn)
				
			# process the gff and genbank files for creating the databases
			if (gff and gbk):
				# create the sqlite database for GBrowse and create the configuration file
				# for GBrowse hook up
				dbName = os.path.splitext(os.path.basename(gff))[0] + '.db'
				dbName = os.path.join(newOrganism, dbName)
				gff = os.path.join(newOrganism, gff)
				
				parser = GenBank.RecordParser()
				gbk = os.path.join(newOrganism, gbk)
				record = parser.parse(open(gbk))
				organismName = record.organism
				accession = record.accession[0]
				self.report.addLogEntry('Found organism name ' + organismName)
				
				# create a brand new GBrowse configuration file
				examiner = GFFExaminer()
				gffHandle = open(gff)
				landmark = examiner.available_limits(gffHandle)['gff_id'].keys()[0][0]
				
				gffRewriter = GFFRewriter(filename=gff, outfile=gff+".sorted.prepared" , accession=accession)
	
				'''gffRewriter.addUnknownCvTerms({
					'user' : settings.DATABASES['default']['USER'], 
					'password' : settings.DATABASES['default']['PASSWORD'], 
					'db' : settings.DATABASES['default']['NAME']
				})'''
			
				gffRewriter.addColor({
					'user' : settings.DATABASES['default']['USER'],
					'password' : settings.DATABASES['default']['PASSWORD'],
					'db' : 'MyGO'
				})
			
				error = gffRewriter.getError()
				print error
				
				gff = gff + ".sorted.prepared"
				
				args = ['-a', 'DBI::SQLite', '-c', '-f', '-d', dbName, gff]
				runProgram('bp_seqfeature_load.pl', args)
				self.report.addLogEntry('Successfully created sqlite database for ' + str(gff))
				
				organismDir = os.path.basename(newOrganism)
				self.report.addLogEntry('Added new GBrowse entry for ' + organismName)
				
				# now edit the record in Chado by first adding the organism and then adding
				# bulk loading the information from gff3
				id = GenomeDBUtil.addOrganismToChado(gff, organismName)
				GenomeDBUtil.createNewGBrowseEntry(landmark, dbName, organismDir, organismName, id)
		
	def __createGFFFiles(self, newOrganisms):
		for newOrganism in newOrganisms:
			newOrganism = os.path.join(NEW_GENOMIC_DATA_DIR, newOrganism)
			organismFiles = os.walk(newOrganism).next()[2]
			
			gbk = None
			for organismFile in organismFiles:
				extension = os.path.splitext(organismFile)[1]
				if (extension == '.gbk'):
					gbk = organismFile
					break
				
			if (gbk):
				runProgram("bp_genbank2gff3.pl",  ["-noCDS", "-s", "-o", newOrganism, os.path.join(newOrganism, gbk)])

		
if __name__== "__main__":
	GenomeDBUpdater().update()
		
		