from django.forms import Field
from django.core.exceptions import ValidationError
import dateutil.parser
import json

class QueryBuilder:
    '''
        Used to build a proper filter for a given input after the
        data has been cleaned in a Django Form.
    '''
    
    def __init__(self, model):
        '''
            Creates a query builder for the given model. Calling the made
            QueryBuilder at any point will give you back the assembled query.
        
            @param model: The model on which to make the query.
        '''
        self.q = model.objects.all()
    
    def __call__(self):
        return self.q
    
    def filter(self, field, value, match='__exact'):
        if value:
            if isinstance(value, DateRange):
                keyargs = value.filterParams(field)
            else:
                keyargs = { field + match : value }
            self.q = self.q.filter(**keyargs)

class DateTimeRangeField(Field):
    '''
        Field for creating a date time range meaning before a date, after a date,
        or between dates.
    '''
    default_error_messages = {
        'invalid' : 'Enter a date range.',
        'invalid_range' : 'A date filter was given with action "range" with less than two dates.',
        'invalid_date' : 'A date filter was given with incorrect date format. Please use iso-8601.'
    }
        
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
            
            
class JsonField(Field):
    '''
        Field for creating a an object from json when receiving it encoded.
    '''
    default_error_messages = {
        'invalid' : 'Please provide valid json format'
    }
    
    def to_python(self, value):
        '''
            Converts this value if possible to a python object.
        '''
        if value in self.empty_values:
            return None
        try:
            return json.loads(value)
        except Exception:
            raise ValidationError(message=self.error_messages['invalid'], code='invalid')
    
