from django import template

register = template.Library()


def add_css_class(field, css_class):
    return field.as_widget(attrs={
        "class": "".join((field.css_classes(), css_class))
    })

register.filter('add_css_class', add_css_class)
