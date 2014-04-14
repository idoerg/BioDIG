'''
    Pagelet for the Search Page
    
    Author: Andrew Oberlin
    Date: August 21, 2012
'''
from biodig.base.renderEngine.PageletBase import PageletBase
from biodig.base.models import OrganismWithGenome

class GBrowseSearchPagelet(PageletBase):
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
        self.setLayout('public/genomeSearch.html')
        
        candidateInfo = list()
        
        for candidate in self.searchParams['candidates']:
            for match in candidate:
                isGenome = True if OrganismWithGenome.objects.filter(organism_id__exact=match.pk).count() else False
                candidateInfo.append((match.common_name, match.abbreviation, str(match.pk), isGenome))     
            
        return {
            'candidateInfo' : candidateInfo,
            'query' : self.searchParams['query']
        }
