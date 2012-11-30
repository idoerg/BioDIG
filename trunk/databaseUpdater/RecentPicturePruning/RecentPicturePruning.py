'''
    Author: Andrew Oberlin
    Date: October 18, 2012
'''
from mycoplasma_home.models import RecentlyViewedPicture

class RecentPicturePruning:
    '''
        For each user this will prune off all but the top 20 pictures that have
        recently been viewed to save images
    '''
    @staticmethod
    def prune():
        allUsers = RecentlyViewedPicture.objects.values_list('user').distinct()
        
        for user in allUsers:
            recentlyViewedPictures = RecentlyViewedPicture.objects.filter(user__exact=user).order_by('-lastDateViewed')
            for picToDel in recentlyViewedPictures[20:]:
                picToDel.delete()
       
if (__name__ == "__main__"):
    RecentPicturePruning.prune()