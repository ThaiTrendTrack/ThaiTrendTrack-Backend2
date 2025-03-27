from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """ Returns the value of a dictionary key, defaulting to 0 if the key doesn't exist """
    return dictionary.get(key, 0)
