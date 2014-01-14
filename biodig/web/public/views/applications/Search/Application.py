'''
	Application for the Search Page of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.public.views.pagelets.ImageSearchPagelet import ImageSearchPagelet
from biodig.web.public.views.pagelets.GBrowseSearchPagelet import GBrowseSearchPagelet
from biodig.web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from biodig.web.public.views.pagelets.FooterPagelet import FooterPagelet
from biodig.base.models import Organism
from django.db.models import Q
from biodig.base.util import Util

class Application(ApplicationBase):
	def doProcessRender(self, request):
		self.addPageletBinding('navBar', NavBarPagelet())
		
		numSearch = 0
		searchImages = str(request.GET.get('searchImages', '')).lower() == "true"
		searchGenomes = str(request.GET.get('searchGenomes', '')).lower() == "true"
		
		if searchImages or searchGenomes:
			query = Util.getDelimitedList(request.GET,'query')
			organismId = Util.getDelimitedList(request.GET, 'organismId')
			candidates = []
			
			if organismId:
				organisms = Organism.objects.filter(pk__in=organismId)
				candidates.append(organisms)
			if query:
				for subquery in query:
					splitQuery = subquery.strip().split(' ')
					
					if (len(splitQuery) == 1):
						if organismId:
							candidate = Organism.objects.filter(species=splitQuery[0]).exclude(organism_id__in=organismId)
						else:
							candidate = Organism.objects.filter(species=splitQuery[0])
						candidates.append(candidate)
					elif(len(splitQuery) == 2):
						if organismId:
							candidate = Organism.objects.filter(Q(species=splitQuery[1]) & Q(genus=splitQuery[0])).exclude(organism_id__in=organismId)
						else:
							candidate = Organism.objects.filter(Q(species=splitQuery[1]) & Q(genus=splitQuery[0]))
						candidates.append(candidate)
					else:
						if organismId:
							candidate = Organism.objects.filter(common_name=subquery).exclude(organism_id__in=organismId)
						else:
							candidate = Organism.objects.filter(common_name=subquery)
						candidates.append(candidate)
			
			formatQuery = ""
			if query:
				formatQuery += 'General Query: "' + ", ".join(query) + '"'
			if organismId:
				amp = " & " if query else ""
				formatQuery += amp + 'Organism Id Query: "' + ", ".join(organismId) + '"'
			
			search = {
				'candidates' : candidates,
				'query' : formatQuery
			}
			
			if searchImages:
				numSearch += 1
				self.addPageletBinding('center-' + str(numSearch), ImageSearchPagelet().setSearchParams(search))
			
			if searchGenomes:
				numSearch += 1
				self.addPageletBinding('center-' + str(numSearch), GBrowseSearchPagelet().setSearchParams(search))
		
		args = {
			'title' : 'Search',
			'numPagelets' : numSearch
		}
		self.setApplicationLayout('public/search.html', args)
		
		self.addPageletBinding('footer', FooterPagelet())

'''
	Used for mapping to the url in urls.py
'''			
def renderAction(request):
	return Application().render(request)

