'''
	Application for the Search Page of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from taxon_home.views.pagelets.public.ImageSearchPagelet import ImageSearchPagelet
from taxon_home.views.pagelets.public.GBrowseSearchPagelet import GBrowseSearchPagelet
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet
from taxon_home.models import Organism
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q

class Application(ApplicationBase):
	def doProcessRender(self, request):
		self.addPageletBinding('navBar', NavBarPagelet())
		
		numSearch = 0
		
		if (request.GET.has_key('search_photos') or request.GET.has_key('search_genomes')):
			query = request.GET['search_val']
			multiQuery = query.split('&')
			
			candidates = list()
			
			for subquery in multiQuery:
				splitQuery = subquery.strip().split(' ')	 

				if (len(splitQuery) == 1):
					try:
						candidate = Organism.objects.get(species=splitQuery[0])
						candidates.append({
							'error' : False,
							'subquery' : subquery,
							'matches' : [candidate]
						})
					except(MultipleObjectsReturned):
						candidate = Organism.objects.filter(species=splitQuery[0])
						candidates.append({
							'error' : False,
							'subquery' : subquery,
							'matches' : candidate
						})
					except(ObjectDoesNotExist):
						candidates.append({
							'error' : True,
							'subquery' : subquery
						})
				elif(len(splitQuery) == 2): 
					try:
						candidate = Organism.objects.get(Q(species=splitQuery[1]) & Q(genus=splitQuery[0]))		
						candidates.append({
							'error' : False,
							'subquery' : subquery,
							'matches' : [candidate]
						})
					except(MultipleObjectsReturned):
						candidate = Organism.objects.filter(Q(species=splitQuery[1]) & Q(genus=splitQuery[0]))
						candidates.append({
							'error' : False,
							'subquery' : subquery,
							'matches' : candidate
						})
					except(ObjectDoesNotExist):
						candidates.append({
							'error' : True,
							'subquery' : subquery
						})
				else:
					candidate = Organism.objects.filter(common_name=subquery)
					candidates.append({
						'error' : False,
						'subquery' : subquery,
						'matches' : candidate
					})
			
			search = {
				'candidates' : candidates,
			}
			
			if (request.GET.has_key('search_photos')):
				numSearch += 1
				self.addPageletBinding('center-' + str(numSearch), ImageSearchPagelet().setSearchParams(search))
			
			if (request.GET.has_key('search_genomes')):
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

