from django import template

register = template.Library()


@register.filter(is_safe=True)
def add_css_class(field, css_class):
    """
    Adds CSS class to form field
    """
    return field.as_widget(attrs={
        "class": "".join((field.css_classes(), css_class))
    })


@register.filter(is_safe=True)
def form_type(field):
    """
    Tag to allow for html form field to be determined.
    Returns string of field type
    """
    return field.field.__class__.__name__
