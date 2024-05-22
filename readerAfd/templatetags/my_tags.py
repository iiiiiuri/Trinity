from django import template

register = template.Library()

@register.simple_tag
def dict_key_lookup(the_dict, key):
    return the_dict.get(key, '')