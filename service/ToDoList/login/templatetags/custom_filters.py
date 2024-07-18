from django import template

register = template.Library()

@register.filter(name='mask_name')
def mask_name(value):
    if len(value) > 1:
        return '*' * (len(value) - 1) + value[-1]
    return value