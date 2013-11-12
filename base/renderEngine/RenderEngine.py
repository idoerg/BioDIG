'''
    Render Engine for Django
    
    Author: Andrew Oberlin
    Date: July 21, 2012
'''
import re
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import simplejson as json

class RenderEngine:
    '''
        Initialize the rendering system
    '''
    def __init__(self, ):
        self.pageletMap = dict()
        self.status = 200
        self.layoutDir = settings.APPLICATION_LAYOUT_DIR
        if (self.layoutDir[len(self.layoutDir) - 1] != '/'):    
            self.layoutDir = self.layoutDir + '/'
        self.pageletDir = settings.PAGELET_LAYOUT_DIR
        if (self.pageletDir[len(self.pageletDir) - 1] != '/'):
            self.pageletDir = self.pageletDir + '/'
    
    
    '''
        Sets the status code
    '''
    def setStatus(self, status):
        self.status = status    
    
    '''
        Sets the application layout for this rendering engine
    '''
    def setApplicationLayout(self, applicationLayout, args=None):
        self.applicationLayout = applicationLayout
        tmpArgs = {
            'SITE_URL' : settings.SITE_URL,
            'STATIC_URL' : settings.STATIC_URL
        }
        
        if (args == None):
            self.applicationArgs = tmpArgs
        else:
            self.applicationArgs = dict(tmpArgs.items() + args.items())
                    
    '''
        Gets the Application layout for this rendering engine
    '''
    def getApplicationLayout(self):
        return self.applicationLayout
    
    '''
        Binds the pageletFile to the pageletName
    '''
    def addPageletBinding(self, pageletName, pageletObj):
        self.pageletMap[pageletName] = pageletObj
    
    def renderPagelet(self, pageletAttr, request, layout, pos, last):
        propertyPattern = re.compile(r'(?i)name="(.+?)"')
        pageletName = propertyPattern.search(pageletAttr).group(1)
        if (self.pageletMap.has_key(pageletName)):
            pagelet = self.pageletMap[pageletName]
            context = RequestContext(request, pagelet.doProcessRender(request))
            context.update(self.applicationArgs)
            pageletRendered = render_to_string(self.pageletDir + pagelet.getLayout(), context_instance=context)
            renderTile = layout[pos[2]:pos[0]] + pageletRendered
            if (last):
                renderTile += layout[pos[1]:]
            return renderTile
        else:
            return '<b>Pagelet ' + pageletName + ' has no binding</b>'
                
    def render(self, request):
        layout = render_to_string(self.layoutDir + self.applicationLayout, self.applicationArgs)
        renderSlotPattern = re.compile(r"(?i)<renderSlot(.+?)/>")
        patIter = renderSlotPattern.finditer(layout)
        matches = [match for match in patIter]  
    
        lastIndex = len(matches)
        lastEnd = 0
        tiles = list()
        lastIndex -= 1
        for (count, match) in enumerate(matches):
            last = count == lastIndex
            attr = match.group(1)
            pos = (match.start(0), match.end(0), lastEnd)
            tiles.append(self.renderPagelet(attr, request, layout, pos, last))
            lastEnd = match.end(0)
        
        
        layout = ''.join(tiles)
        
        return HttpResponse(layout)

    def renderJson(self, request):
        return HttpResponse(json.dumps(self.applicationLayout), status=self.status)
