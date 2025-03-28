from django import template

register = template.Library()

@register.filter(name='split')
def split(value, delimiter=','):
    """
    Returns the string split by delimiter and removes underscores.
    Example usage: {{ value|split:"," }}
    """
    if value:
        # Split by delimiter, strip whitespace, and replace underscores with spaces
        return [x.strip().replace('_', ' ').title() for x in value.split(delimiter)]
    return []

@register.filter
def trim(value):
    return value.strip()
