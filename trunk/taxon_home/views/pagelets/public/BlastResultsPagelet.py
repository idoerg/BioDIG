'''
	Pagelet for the Home Page
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.PageletBase import PageletBase
from mycoplasma_home.models import BlastUpload, Landmark
import os
from tempfile import NamedTemporaryFile
from django.conf import settings

class BlastResultsPagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/blast.html')
		if (request.method == "POST"):
			fileDict = request.FILES
			response = ""
			if (request.POST.has_key('blast_db')):	
				database = request.POST['blast_db']
				
				root = settings.STATIC_ROOT
				media_root = settings.MEDIA_ROOT
				
				landmark = Landmark.objects.get(organism_id__exact=int(database))
				#os.system("formatdb -p F -i " + root + "/" + str(landmark.name).lower() + ".fasta")
				sequence = request.POST['sequence']
				
				if (sequence != ""):
					tmp_fasta_file = NamedTemporaryFile(mode='w+b', suffix='.fasta', dir='/tmp', delete=False)
					tmp_fasta_file.write(sequence)
					tmp_fasta_file.close()
					
					blast_result = os.popen("blastall -p blastn -d " + root + "/" + str(landmark.name).lower() + ".fasta -T T -i " + root + "/tmp.fasta")
					response = "<pre>" + " ".join(blast_result.readlines()) + "</pre>"
										
					os.remove(tmp_fasta_file.name)
					
				elif (fileDict.has_key('file')):
					uploadedFile = fileDict['file']
					fasta = BlastUpload(fasta_file=uploadedFile, name=uploadedFile.name)
					fasta.save()
					
					blast_result = os.popen("blastall -p blastn -d " + root + "/" + str(landmark.name).lower() + ".fasta -T T -i " + media_root + "/" + str(fasta.fasta_file))
					response = "<pre>" + " ".join(blast_result.readlines()) + "</pre>"
										
					os.system("rm " + root + "/" + str(landmark.name).lower() + ".fasta.n*")
					os.system("rm " + media_root + "/" + str(fasta.fasta_file))
					fasta.delete()
		return {
			'response' : response
		}
