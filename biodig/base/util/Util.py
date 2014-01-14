import re
from datetime import datetime
import biodig.base.util.ErrorConstants as Errors

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
    value = queryDict.get(key, None)
    if value:
        value = [item.strip() for item in value.split(delimiter)]
    return value

def getFilterByDate(dateString, paramName):
    action_dates = [item.strip() for item in dateString.split(':', 1)]
    
    action = action_dates[0]
    dates = action_dates[1] if len(action_dates) > 1 else ''
    
    try:
        if action == 'after':
            return { paramName + '__gt' : parseDate(dates) }
        elif action == 'before':
            return { paramName + '__lt' : parseDate(dates) }
        elif action == 'range':
            dates = [item.strip() for item in dates.split(',', 1)]
            for i, date in enumerate(dates):
                dates[i] = parseDate(date)
            return { paramName + '__range' : dates }
        else: # on keyword or no keyword
            date = parseDate(action + ':' + dates if dates else action)
            return {
                paramName + '__year' : date.year,
                paramName + '__month' : date.month,
                paramName + '__day' : date.day
            }
    except ValueError:
        raise Errors.INVALID_SYNTAX.setCustom(paramName)
    
def parseDate(dateString):
    date_time = dateString.split(' ', 1)
    if len(date_time) < 2:
        date_time.append("00:00:00")
    date = datetime.strptime(date_time[0] + " " + date_time[1], "%Y-%m-%d %H:%M:%S")
    return date
