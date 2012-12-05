'''
    Pagelet for the Search Page
    
    Author: Andrew Oberlin
    Date: August 21, 2012
'''
from renderEngine.PageletBase import PageletBase
from django.core.exceptions import ObjectDoesNotExist

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
            if (not candidate['error']):
                for match in candidate['matches']:
                    candidateInfo.append((match.common_name, str(match.pk)))
            else:
                candidateInfo.append(("No entries for " + candidate['subquery'], -1, -1))      
            
        return {
            'candidateInfo' : candidateInfo
        }
