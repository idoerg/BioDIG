'''
	--------------------------------------------------
		Static API functions for dealing with Images
	--------------------------------------------------
'''
from mycoplasma_home.models import Picture, PictureDefinitionTag, Organism, TagGroup, Tag, TagPoint, GeneLink
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

NO_ERROR = 'Success'
INVALID_IMAGE_KEY = 'Invalid Image Key Provided'
NO_IMAGE_KEY = 'No Image Key Provided'
INVALID_TAG_GROUP_KEY = 'Invalid Tag Group Key Provided'
NO_TAG_GROUP_KEY = 'No Tag Group Key Provided'
NO_TAG_KEY = "No Tag Key Provided"
INVALID_TAG_KEY = "Invalid Tag Key Provided"


'''
	Gets the metadata associated with an image given the image key
	
	@param imageKey: The primary key for the image or the image
	@param user: a Django auth_user object necessary for images
	that are still private
	@param isKey: Whether the first argument is a key object or not (default: true)
	
	@return: A dictionary containing organisms associated with the image and all 
	of the images attributes. The dictionary will also contain error information
	stored in the errorMessage and error fields
'''
def getImageMetadata(imageKey, user=None, isKey=True):
	organisms = []
	errorMessage = NO_ERROR
	
	try:
		if (isKey):
			image = Picture.objects.get(pk__exact=imageKey) 
		else:
			image = imageKey
		
		authenticated = True
		if (image.isPrivate):
			if (user and user.is_authenticated()):
				authenticated = image.user == user
			else:
				authenticated = False
				
		if (authenticated):
			defTags = PictureDefinitionTag.objects.filter(picture__exact=image)
			
			for tag in defTags:
				try:
					organisms.append(model_to_dict(Organism.objects.get(pk__exact=tag.organism_id), fields=['organism_id', 'common_name']))
				except ObjectDoesNotExist:
					None					
		else:
			errorMessage = INVALID_IMAGE_KEY
	except ObjectDoesNotExist:
		errorMessage = INVALID_IMAGE_KEY	
	
	metadata = None
		
	if (errorMessage == NO_ERROR):
		metadata = {
			'error' : False,
			'errorMessage' : errorMessage,
			'organisms' : organisms,
			'description' : image.description,
			'uploadedBy' : image.user.username,
			'uploadDate' : image.uploadDate.strftime("%Y-%m-%d %H:%M:%S"),
			'url' : image.imageName.url
		}
	else:
		metadata = {
			'error' : True,
			'errorMessage' : errorMessage
		}
	
	return metadata

'''
	Gets the tag group for the given image
	
	@param imageKey: The primary key for the image or the image
	@param user: a Django auth_user object necessary for images
	that are still private
	@param getTags: Whether or not to get the tags in these groups also
	@param isKey: Whether the first argument is a key object or not (default: true)
'''
def getImageTagGroups(imageKey, user=None, getTags=False, getLinks=False, isKey=True):
	errorMessage = NO_ERROR
	tagGroups = []
	
	try:
		if (isKey):
			image = Picture.objects.get(pk__exact=imageKey)
		else:
			image = imageKey
			
		authenticated = True
		if (image.isPrivate):
			if (user and user.is_authenticated()):
				authenticated = image.user == user
			else:
				authenticated = False
				
		if (authenticated):
			groups = TagGroup.objects.filter(picture__exact=image)
			
			for group in groups:
				newGroup = {
					'pk' : group.pk,
					'name' : group.name,
					'dateCreated' : group.dateCreated.strftime("%Y-%m-%d %H:%M:%S"),
					'lastModified' : group.lastModified.strftime("%Y-%m-%d %H:%M:%S")
				}
				
				if (getTags):
					tags = getImageTags(group, user=user, getLinks=getLinks, isKey=False)
					if (tags['error']):
						errorMessage = tags['errorMessage']
					
					del tags['errorMessage']
					del tags['error']
					newGroup['tags'] = tags['tags']
				tagGroups.append(newGroup)
		else:
			errorMessage = INVALID_IMAGE_KEY
	except ObjectDoesNotExist:
		errorMessage = INVALID_IMAGE_KEY
		
	tagGroupsList = {
		'error' : errorMessage != NO_ERROR,
		'errorMessage' : errorMessage,
		'tagGroups' : tagGroups
	}
	
	return tagGroupsList
		
'''
	Gets the tags associated with the given tag group
	
	@param tagGroupKey: The primary key for the tag group or the tag group
''' 
def getImageTags(tagGroupKey, user=None, getLinks=False, isKey=True):
	tagTuples = []
	errorMessage = NO_ERROR
	
	try:
		if (isKey):
			tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
		else:
			tagGroup = tagGroupKey
		
		authenticated = True
		
		if (tagGroup.picture.isPrivate):
			if (user and user.is_authenticated()):
				authenticated = tagGroup.user == user
			else:
				authenticated = False
				
		if (authenticated):
			tags = Tag.objects.filter(group__exact=tagGroup)
			
			for tag in tags:
				tagPoints = TagPoint.objects.filter(tag__exact = tag).order_by('rank')
				points = []
				
				for tagPoint in tagPoints:
					points.append([
						tagPoint.pointX, 
						tagPoint.pointY
					])
				
				color = [tag.color.red, tag.color.green, tag.color.blue]
				
				tagTuple = {
					'id' : tag.pk,
					'color' : color,
					'points' : points,
					'description' : tag.description
				}
				
				if (getLinks):
					geneLinks = getGeneLinks(tag, user=user, isKey=False)
					if (geneLinks['error']):
						errorMessage = geneLinks['errorMessage']
					
					del geneLinks['errorMessage']
					del geneLinks['error']
					tagTuple['geneLinks'] = geneLinks['geneLinks']
				
				tagTuples.append(tagTuple)
		else:
			errorMessage = INVALID_TAG_GROUP_KEY
	except ObjectDoesNotExist:
		errorMessage = INVALID_TAG_GROUP_KEY

	if (errorMessage == NO_ERROR):
		return {
			'error' : False,
			'errorMessage': errorMessage,
			'tags': tagTuples
		}
	else:
		return {
			'error' : True,
			'errorMessage': errorMessage,	
		}
'''
	Gets the gene links registered to the tag key provided
	
	@param tagKey: Key or tag object used to retrieve the gene links
'''		
def getGeneLinks(tagKey, user=None, isKey=True):
	geneLinks = []
	errorMessage = NO_ERROR
	
	try:
		if (isKey):
			tag = Tag.objects.get(pk__exact=tagKey)
		else:
			tag = tagKey
		
		authenticated = True
		
		if (tag.group.picture.isPrivate):
			if (user and user.is_authenticated()):
				authenticated = tag.group.user == user
			else:
				authenticated = False
				
		if (authenticated):
			geneLinkResults = GeneLink.objects.filter(tag=tag)
			
			for geneLink in geneLinkResults:
				geneLinks.append({
					'uniquename' : geneLink.feature.uniquename,
					'name' : geneLink.feature.name,
					'organismId' : geneLink.feature.organism.organism_id		
				})
		else:
			errorMessage = INVALID_TAG_KEY
	except ObjectDoesNotExist:
		errorMessage = INVALID_TAG_KEY
		
	if (errorMessage == NO_ERROR):
		return {
			'error' : False,
			'errorMessage': errorMessage,
			'geneLinks': geneLinks
		}
	else:
		return {
			'error' : True,
			'errorMessage': errorMessage,	
		}
	
	
	
	