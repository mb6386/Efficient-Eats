from django import template
register = template.Library()
@register.filter
def blurbify(text):
    if len(text) > 500:
        blurb = text[:500]+"..."
    else:
        blurb = text
    return blurb