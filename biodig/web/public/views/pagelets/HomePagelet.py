'''
    Pagelet for the Home Page
    
    Author: Andrew Oberlin
    Date: July 23, 2012
'''
from biodig.base.renderEngine.PageletBase import PageletBase
from biodig.base.models import Organism, Feature, ImageOrganism, TagGroup, Tag

class HomePagelet(PageletBase):
    '''
        Renders the center of the home page     
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('public/home.html')

        allMycoplasma = Organism.objects.all().order_by('species')
        #allGenomes = Organism.objects.values_list('organism_id', flat=True).order_by('organism_id')
        #allImages = OrganismWithImages.objects.values_list('organism_id', flat=True).order_by('organism_id')
        #allTags = OrganismWithTags.objects.values_list('organism_id', flat=True).order_by('organism_id')
        
        allGenomes = list(Feature.objects.values_list('organism', flat=True).distinct())
        allImages = list(ImageOrganism.objects.values_list('organism', flat=True).distinct())
        if not allImages:
            allTags = []
        else:
            allTaggedImages = TagGroup.objects.filter(pk__in=Tag.objects.all().values_list('group')).values_list('picture').distinct()
            allTags = list(ImageOrganism.objects.filter(picture__in=allTaggedImages).values_list('organism').distinct())
        return {
            'all_mycoplasma' : allMycoplasma,
            'all_genomes' : allGenomes,
            'all_images' : allImages,
            'all_tags' : allTags
        }
