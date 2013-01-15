'''
    Pagelet for the Search Page
    
    Author: Andrew Oberlin
    Date: August 21, 2012
'''
from renderEngine.PageletBase import PageletBase
from taxon_home.models import PictureDefinitionTag

class ImageSearchPagelet(PageletBase):
    '''
        Used to set the extra parameters for executing the search simply
        
        @param: searchParams -- parameters for searching the image database
        
        @return: self object to allow for easy chaining
    '''
    def setSearchParams(self, searchParams):
        self.searchParams = searchParams
        return self
        
    '''
        Renders the navigation bar for the website        
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('public/imageSearch.html')
        
        limit = 8
        
        candidateInfo = list()
        
        for candidate in self.searchParams['candidates']:
            for match in candidate:
                numImages = PictureDefinitionTag.objects.filter(organism__exact=match.pk).count()
                pages = numImages/limit + 1
                candidateInfo.append((match.common_name, match.abbreviation, str(match.pk), pages, numImages))
    
        return {
            'candidateInfo': candidateInfo,
            'limit': limit,
            'imagesPerRow' : 4,
            'query' : self.searchParams['query']
        }
