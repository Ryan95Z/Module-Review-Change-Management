from django.views import View
from django.shortcuts import render
from django.forms import formset_factory

from core.models import Module
from forms.forms import FieldEntityForm

class AdminModuleDescriptionFormStructure(View):
    def __init__(self):
        self.template = 'module_description_form_control.html'
        self.field_formset_object = formset_factory(FieldEntityForm, can_delete=True)
    def get(self, request, **kwargs):
        field_formset = self.field_formset_object(request.GET or None)
        return render(request, 'module_description_form_control.html', {'field_formset': field_formset})

class AdminModuleDescriptionFormModify(View):
    """
    View which handles the module description structure form
    """
    def __init__(self):
        self.template = 'module_description_form_control.html'
        self.field_formset_object = formset_factory(FieldEntityForm)

    def get(self, request, **kwargs):
        field_formset = self.field_formset_object(request.GET or None)
        return render(request, self.template, {'field_formset': field_formset})

    def post(self, request, **kwargs):
        field_formset = self.field_formset_object(request.POST or None)
        if field_formset.is_valid():
            for form in field_formset:
                form.save(commit=False)
            return redirect('view_module_tracking_form') # temp redirect
        return render(request, self.template_name, {
            'field_formset': field_formset,
            'formset_length': len(field_formset)
        })
        