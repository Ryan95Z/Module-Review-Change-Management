def md_to_form(queryset):
    """
    Accepts a queryset of module description entries
    and converts them into the correct format to be
    displayed in a module description form.

    Only works if the given entries correlate to the
    form which is being rendered.
    """
    form_data = {}
    for entry in queryset:
        field = entry.field_id
        id_for_form = "field_entity_" + str(field.pk)
        field_type = field.entity_type
        if field_type == "text-input" or field_type == "text-area":
            form_data[id_for_form] = entry.string_entry
    return form_data

