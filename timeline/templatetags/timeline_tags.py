import markdown
from django import template

register = template.Library()


@register.filter(is_safe=False)
def covert_markdown(md):
    """
    Filter method that will convert a markdown
    string into html.
    """
    return markdown.markdown(md)
