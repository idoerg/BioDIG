import re
from datetime import datetime
import biodig.base.util.ErrorConstants as Errors
from django.forms import Field
from django.core.exceptions import ValidationError
import dateutil.parser

class DateTimeRangeField(Field):
    default_error_messages = {
        'invalid': _('Enter a date range.'),
        'invalid_range' : _('A date filter was given with action "range" with less than two dates.'),
        'invalid_date' : _('A date filter was given with incorrect date format. Please use iso-8601.')
    }
    
    
    def __init__(self, *args, **kwargs):
        '''
            Constructs a DateTimeRangeField the same way that
            one would construct a Field
        '''
        super(Field, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        '''
            Converts this value if possible to a DateRange object.
        '''
        if value in self.empty_values:
            return None
        
        if isinstance(value, DateRange):
            return value
        
        action_dates = [item.strip() for item in value.split(':', 1)]
    
        action = action_dates[0].lower() # action: range, after, before (defaults to blank)
        
        # if the action is an accepted action then the remaining string represents
        # the dates, if not then we assume the whole string is the dates representation
        # and the action defaults to "range"
        if action in DateRange.accepted_actions:
            dates = action_dates[1] if len(action_dates) > 1 else ''
        else:
            action = ''
            dates = value
            
        # Parse the dates into two separate dates
        dates = [item.strip() for item in dates.split(',', 1)]
        if action == "range" and len(dates) < 2:
            raise ValidationError(message=self.error_messages['invalid_range'], code='invalid')
        
        try:    
            start = dateutil.parser.parse(dates[0])
            end = dateutil.parser.parse(dates[1]) if len(dates) >= 2 else None
        except Exception:
            raise ValidationError(message=self.error_messages['invalid_date'], code='invalid')
        
        return DateRange(action, start, end)
        
class DateRange:
    accepted_actions = set(['before', 'after', 'range'])
    
    def __init__(self, action, start, end):
        self.start = start
        self.end = end
        self.action = action
        
    def filterParams(self, paramName):
        '''
            Sets up a dictionary to be used as the keyword arguments
            for a filter to correctly filter by the date range.
        '''
        if self.action == 'after':
            return { paramName + '__gt' : self.start }
        elif self.action == 'before':
            return { paramName + '__lt' : self.start }
        elif self.action == 'range':
            return { paramName + '__range' : [self.start, self.end] }
        else: # on keyword or no keyword
            return {
                paramName + '__year' : self.start.year,
                paramName + '__month' : self.start.month,
                paramName + '__day' : self.start.day
            }
            

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
