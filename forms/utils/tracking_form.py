
# Function which accepts a number of forms as kwargs and returns a list of those which are unbound
def get_unbound_forms(**kwargs):
    unbound_forms = []
    for form_name, form in kwargs.items():
        if hasattr(form, "instance"):
            if form.instance.pk == None:
                unbound_forms.append(form_name)
        if hasattr(form, "queryset"):
            if not form.queryset:
                unbound_forms.append(form_name)
    return unbound_forms