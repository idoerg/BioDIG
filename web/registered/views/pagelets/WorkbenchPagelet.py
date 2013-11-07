'''
    Pagelet for the user Workbench
    
    Author: Andrew Oberlin
    Date: July 23, 2012
'''
from web.renderEngine.PageletBase import PageletBase
from base.models import Picture, RecentlyViewedPicture, Tag, TagGroup, GeneLink

class WorkbenchPagelet(PageletBase):
    '''
        Renders the user workbench for the website        
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('registered/workbench.html')

        userImages = Picture.objects.filter(user__exact=request.user)

        myImages = []
                
        #
        for image in userImages:
            permissions = 'public'
            if image.isPrivate:
                permissions = 'private'
            myImages.append({
                'permissions' : permissions,
                'image' : image
            })
            
        recentImages = RecentlyViewedPicture.objects.filter(user__exact=request.user).order_by('lastDateViewed')[:10]
        
        userTags = Tag.objects.filter(user__exact=request.user).order_by('dateCreated')
        myTags = []
                
        #
        for tag in userTags:
            permissions = 'public'
            if tag.isPrivate:
                permissions = 'private'
            myTags.append({
                'permissions' : permissions,
                'tag' : tag
            })
        
        
        userTagGroups = TagGroup.objects.filter(user__exact=request.user).order_by('dateCreated')
        myTagGroups = []
                
        #
        for tagGroup in userTagGroups:
            permissions = 'public'
            if tagGroup.isPrivate:
                permissions = 'private'
            myTagGroups.append({
                'permissions' : permissions,
                'tagGroup' : tagGroup
            })
            
        userGeneLinks = GeneLink.objects.filter(user__exact=request.user).order_by('dateCreated')
        myGeneLinks = []
                
        #
        for geneLink in userGeneLinks:
            permissions = 'public'
            if geneLink.isPrivate:
                permissions = 'private'
            myGeneLinks.append({
                'permissions' : permissions,
                'geneLink' : geneLink
            })
            
        return {
            'myImages' : myImages,
            'recentImages' : recentImages,
            'myTags' : myTags,
            'myTagGroups' : myTagGroups,
            'myGeneLinks' : myGeneLinks
        }
