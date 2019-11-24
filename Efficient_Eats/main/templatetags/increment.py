from django import template

register = template.Library()
@register.filter
def increment(value):
    value+=1
    return value
