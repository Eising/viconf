from django import template

register = template.Library()

@register.simple_tag
def indirect(variable, key):
    return variable[key]
