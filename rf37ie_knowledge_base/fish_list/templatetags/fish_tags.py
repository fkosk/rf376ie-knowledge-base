from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary in template"""
    if dictionary is None:
        return ''
    return dictionary.get(key, key)

@register.filter
def get_attr(obj, attr):
    """Get attribute from object in template"""
    if obj is None:
        return ''
    return getattr(obj, attr, '')

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary"""
    if dictionary is None:
        return ''
    return dictionary.get(key, '')