'''
	Pagelet for the Home Page
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from base.renderEngine.PageletBase import PageletBase
from base.models import Organism, OrganismWithImages, OrganismWithGenome, OrganismWithTags

class HomePagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/home.html')

		allMycoplasma = Organism.objects.all().order_by('species')
		allGenomes = OrganismWithGenome.objects.values_list('organism_id', flat=True).order_by('organism_id')
		allImages = OrganismWithImages.objects.values_list('organism_id', flat=True).order_by('organism_id')
		allTags = OrganismWithTags.objects.values_list('organism_id', flat=True).order_by('organism_id')
		
		return {
			'all_mycoplasma' : allMycoplasma,
			'all_genomes' : allGenomes,
			'all_images' : allImages,
			'all_tags' : allTags
		}
