import markdown
from django import template

register = template.Library()


@register.filter(is_safe=False)
def covert_markdown(md):
    return markdown.markdown(md)
