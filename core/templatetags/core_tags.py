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


@register.filter(is_safe=True)
def page_neighbours(current_page, end_page):
    start = 1
    end = 4

    if end_page < 6:
        return range(1, end_page+1)

    if current_page >= 4:
        start = current_page - 1
        end = current_page + 1

    if end >= end_page:
        start = current_page - 2
        end = end_page

    return range(start, end + 1)


@register.filter(is_safe=True)
def page_neighbours2(current_page, end_page):
    cp_start = 1 - current_page
    cp_end = end_page - current_page

    start, end = 1, end_page

    show_start = False
    show_end = False

    if cp_start >= 3 and cp_end >= 3:
        start = current_page - 1
        end = current_page + 1

        show_start = True
        show_end = True

    if cp_start < 3:
        start = 1
        end = 4

        show_start = False
        show_end = True

    if cp_end < 3:
        start = end_page - 3
        end = end_page

        show_start = True
        show_end = False

    return (show_start, show_end, range(start, end + 1))


@register.filter(is_safe=True)
def range_last_item(_range):
    return _range[-1]
