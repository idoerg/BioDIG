from biodig.base.models import Organism
from biodig.base.renderEngine.WebServiceObject import WebServiceArray, LimitDict


class GetAPI:
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields

    '''
        Search for organisms based on text input
        
        @param organisms: Array of strings representing organisms to search for in the database
    '''
    def getOrganisms(self, organisms):
        metadata = WebServiceArray()
        candidates = []
       
        if not candidates:
            return metadata

        # search for each organism
        for organism in organisms:
            orgCandidates = Organism.objects.filter(common_name=organism)
            species = organism.split(None, 1)
            if len(species) > 1:
                species = species[1]
            else:
                species = species[0]
            orgCandidates = orgCandidates | Organism.objects.filter(species=species)
            if orgCandidates:
                candidates.extend(orgCandidates)
        
        closedSet = set()
        
        for candidate in candidates:
            if not candidate.pk in closedSet:
                metadata.put(LimitDict(self.fields, {
                    'id' : candidate.pk,
                    'commonName' : candidate.common_name,
                    'abbreviation' : candidate.abbreviation,
                    'genus' : candidate.genus,
                    'species' : candidate.species
                }))
                closedSet.add(candidate.pk)
                    
        return metadata
