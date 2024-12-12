from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get an item from a dictionary using its key."""
    return dictionary.get(key, 0)  # Return 0 if key not found
