from django.forms import Field
from django.core.exceptions import ValidationError
import dateutil.parser

class DateTimeRangeField(Field):
    default_error_messages = {
        'invalid' : 'Enter a date range.',
        'invalid_range' : 'A date filter was given with action "range" with less than two dates.',
        'invalid_date' : 'A date filter was given with incorrect date format. Please use iso-8601.'
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