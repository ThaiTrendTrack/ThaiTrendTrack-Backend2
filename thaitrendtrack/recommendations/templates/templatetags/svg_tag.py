import os
from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def inline_svg(filename):
    path = static(filename)
    full_path = os.path.join('templates/static', filename)
    try:
        with open(full_path, 'r') as f:
            return mark_safe(f.read())
    except FileNotFoundError:
        return f"<!-- SVG file {filename} not found -->"
