from django import template

register = template.Library()


@register.filter(is_safe=True)
def add_css_class(field, css_class: str):
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
    Returns string of field type.
    """
    return field.field.__class__.__name__


@register.filter(is_safe=True)
def pagination_range(current_page: int, end_page: int):
    """
    Tag that gets calculates the pagination range
    that is needed. Returns a dictionary containing
    boolean flags for showing start and end pages. It also provides
    the range for pagination
    """

    if type(current_page) is not int or type(end_page) is not int:
        raise TypeError("pagination_range - both parameters must be ints")

    # determine distance between start and end pages
    cp_start = current_page - 1
    cp_end = end_page - current_page

    # base ranges
    start = 1
    end = end_page

    # flags to determine to show first or last page
    # if we between them
    show_start = False
    show_end = False

    # only calculate pagination if we have more than 4 pages
    if end_page > 4:
        # if we are nowhere near the start or end pages
        if cp_start >= 3 and cp_end >= 3:
            start = current_page - 1
            end = current_page + 1

            show_start = True
            show_end = True

        # if we are near the start page
        if cp_start < 3:
            start = 1
            end = 4

            show_start = False
            show_end = True

        # if we are near to the end page
        if cp_end < 3:
            start = end_page - 3
            end = end_page

            show_start = True
            show_end = False

    r = range(start, end + 1)
    return {
        'show_start': show_start,
        'show_end': show_end,
        'pagination_range': r
    }


@register.filter(is_safe=True)
def range_last_item(_range):
    """
    Tag that allows the last value from an
    array or range to be extracted
    """
    return _range[-1]
