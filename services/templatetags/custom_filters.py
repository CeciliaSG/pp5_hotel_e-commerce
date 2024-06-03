from django import template
import datetime

register = template.Library()

@register.filter(name='format_duration')
def format_duration(value):
    print("Value:", value)
    print("Type of value:", type(value))
    if isinstance(value, datetime.timedelta):
        hours = value.seconds // 3600
        minutes = (value.seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return "0m"
    return value