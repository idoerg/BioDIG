from django import template

register = template.Library()

@register.filter
def mod(value, arg):
    return value % arg == 0
    
@register.filter
def definesRect(values):
    if (len(values) == 2):
        return True
    else:
        return False

@register.filter
def noColor(value):
    if (value == "transparent"):
        return True
    else:
        return False
        
@register.filter
def isZero(value):
    return value == 0
    
@register.filter
def isLessThan(value, arg):
    return value < arg
    
@register.filter
def isGreaterThan(value, arg):
    return value > arg
    
@register.filter
def lastPageNums(value, arg):
    nums = list()
    i = 1
    while (i + value < arg + 1 and i < 5):
        nums.append(i + value)
        i += 1
    return nums

@register.filter    
def firstPageNums(value):
    nums = list()
    i = value - 1
    while (i > 0 and i > value - 5):
        nums.append(i)
        i -= 1
    return nums
    
@register.filter
def getRange(value, arg):
    lower =  (value - 1) * arg
    upper = lower + arg - 1
    return str(lower) + "_" + str(upper)
    
@register.filter
def getRangePrev(value, arg):
    lower =  (value - 2) * arg
    upper = lower + arg - 1
    return str(lower) + "_" + str(upper)
    
@register.filter
def getRangeNext(value, arg):
    lower =  (value) * arg
    upper = lower + arg - 1
    return str(lower) + "_" + str(upper)

@register.filter
def getCommonNames(value):
    retStr = ""
    for (counter, item) in enumerate(value):
        retStr = retStr + item[0]        
        if (counter < len(value) - 1):
            retStr = retStr +  ", "
    return retStr

@register.filter
def isEmptyString(value):
    return value == ""

@register.filter
def abbreviateCommonName(value):
    retStr = "M. "
    retStr += value.split(" ")[1]
    if (retStr == "M. entries"):
        retStr = value.split("No entries for ")[1]   
    return retStr  

@register.filter
def numRange(value):
    return range(1, value+1) 

@register.filter
def inList(value, arg):
    return value in arg
