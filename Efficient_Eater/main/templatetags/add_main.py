from django import template
register = template.Library()
@register.filter
def add_main(value):
    return str(f'main/{value}')