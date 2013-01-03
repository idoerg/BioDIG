'''
	Ajax Application for the Image Pagination
	URL: /image/editor/submit
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxRegisteredApplicationBase import AjaxRegisteredApplicationBase
from django.views.decorators.csrf import csrf_exempt
from taxon_home.models import GeneLink, Tag, Feature, Organism
from django.core.exceptions import ObjectDoesNotExist

class Application(AjaxRegisteredApplicationBase):
	def doProcessRender(self, request):
		errorMessage = ""
		if (request.method == "POST"):
			try:
				geneName = request.POST['geneName']
				organismId = request.POST['organismId']
				tagKeys = request.POST.getlist('tagKeys[]')
				uniqueName = None
				if (request.POST.has_key('geneUniqueName') and request.POST['geneUniqueName']):
					uniqueName = request.POST['geneUniqueName']
				organism = None
				feature = None
				multiFeatures = False
				errorTagKeys = []
				try:
					organism = Organism.objects.get(organism_id__exact=organismId)
				except ObjectDoesNotExist:
					errorMessage = "No organism with the id: " + organismId
					
				if (organism != None):
					if (uniqueName):
						feature = Feature.objects.get(organism=organism, uniquename=uniqueName)
					else:
						features = Feature.objects.filter(organism=organism, name=geneName)
						if (not features):
							try:
								feature = Feature.objects.get(organism=organism, uniquename=geneName)
							except ObjectDoesNotExist:
								errorMessage = "No gene, " + str(geneName) + ", exists for the organism " + str(organism.common_name)
						elif(len(features) == 1):
							feature = features[0]
						else:
							multiFeatures = True
					if (feature != None):
						featureJson = None
						for tagKey in tagKeys:
							try:
								tag = Tag.objects.get(pk__exact=tagKey)
								newGeneLink, created = GeneLink.objects.get_or_create(tag=tag, feature=feature)
								if (created):
									if (featureJson == None):
										featureJson = {
											'uniquename' : feature.uniquename,
											'name' : feature.name
										}
								else:
									errorTagKeys.append([tagKey, 'Gene link with this key already exists for the gene ' + str(feature.name)])
							except ObjectDoesNotExist:
								errorTagKeys.append([tagKey, 'Tag with this key does not exist'])
								
						if (featureJson != None):
							self.setJsonObject({
								'error' : False,
								'feature' : featureJson,
								'errorTagKeys' : errorTagKeys,
								'errorMessage' : 'Success'
							})
						else:
							self.setJsonObject({
								'error' : True,
								'errorTagKeys' : errorTagKeys,
								'errorMessage' : 'No changes were made to the database'
							})
					else:
						if multiFeatures:
							self.setJsonObject({
								'error' : True,
								'errorMessage' : 'No changes were made to the database. Multiple features have the name ' + str(geneName) + 
									'. Try again with one of the following: ' + ', '.join([val.uniquename for val in features])
							})
						else:
							errorMessage = "No matching features for the name: " + str(geneName)
			except KeyError as e:
				errorMessage = "Error on key " + str(e)
		else:
			errorMessage = "Incorrect method for adding a new gene link"
		
		if (errorMessage != ""):
			self.setJsonObject({
				'error' : True,
				'errorMessage' : errorMessage
			})

		
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt			
def renderAction(request):
	return Application().render(request)
