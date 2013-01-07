import re

def getMultiListPost(request, name, default):
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
    if parts:
        for part in parts:
            dic[int(part['key'])] = request.POST.getlist(part['entire'] + '[]')
            
        return dic
    else:
        return default

def getInt(queryDict, key, default):
    value = queryDict.get(key, '')
    if value.isdigit():
        value = int(value)
    else:
        value = default
        
    return value

def getDelimitedList(queryDict, key, delimiter=','):
    value = queryDict.get('fields', None)
    if value:
        value = "".join(value.split())
        value = value.split(',')
    return value