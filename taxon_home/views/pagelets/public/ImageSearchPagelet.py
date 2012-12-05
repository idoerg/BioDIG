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
        
        num_items_row = 5
        num_items_col = 3
        picsPerPage = num_items_row * num_items_col
        
        candidateInfo = list()
        
        for candidate in self.searchParams['candidates']:
            if (not candidate['error']):
                for match in candidate['matches']:
                    numImages = PictureDefinitionTag.objects.filter(organism_id__exact=match.pk).count()
                    numPages = numImages/picsPerPage + 1
                    candidateInfo.append((match.common_name, str(match.pk), numPages, numImages))
            else:
                candidateInfo.append(("No entries for " + candidate['subquery'], -1, -1, -1))
        
        return {
            'candidateInfo': candidateInfo,
            'picsPerPage': picsPerPage
        }
