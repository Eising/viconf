from django import template
from util.validators import ViconfValidators
import sys

register = template.Library()

@register.simple_tag
def indirect(variable, key):
    return variable[key]

@register.simple_tag
def validatorclass(name):
    validators = ViconfValidators.VALIDATORS
    if name == 'none':
        return ""

    if name in validators:
        return validators[name]['css_class']
    else:
        return ""
