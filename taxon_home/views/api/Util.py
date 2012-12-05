import re

def getMultiListPost(request, name):
    dic = {}
    parts = []
    namePattern = re.compile(name + r'\[([0-9]+)\]')
    for k in request.POST.keys():
        match = namePattern.search(k)
        if (match):    
            parts.append({
                'entire' : match.group(0),
                'key' : match.group(1)
            })

    for part in parts:
        dic[int(part['key'])] = request.POST.getlist(part['entire'] + '[]')

    return dic