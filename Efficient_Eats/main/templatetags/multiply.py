from django import template

register = template.Library()
@register.filter
def multiply(num1, num2, *args, **kwargs):
    # you would need to do any localization of the result here
    return num1 * num2