from django.views import View
from django.shortcuts import render, redirect
from django.forms import modelformset_factory, formset_factory

from core.models import Module
from forms.models import ModuleDescriptionFormVersion, FormFieldEntity
from forms.forms import FieldEntityForm

class AdminModuleDescriptionFormStructure(View):

    def get(self, request, **kwargs):
        newest_version = ModuleDescriptionFormVersion.objects.get_most_recent()
        newest_version_fields = FormFieldEntity.objects.get_most_recent_form()
        all_versions = ModuleDescriptionFormVersion.objects.get_version_list()
        context = {
            'form_version': newest_version,
            'form_fields': newest_version_fields,
            'all_versions': all_versions
        }
        return render(request, 'md_form_structure_view.html', context)

class AdminModuleDescriptionFormStructureOld(View):

    def get(self, request, **kwargs):
        version_pk = self.kwargs['pk']
        chosen_version = ModuleDescriptionFormVersion.objects.get(pk=version_pk)
        chosen_version_fields = FormFieldEntity.objects.get_form(chosen_version)
        all_versions = ModuleDescriptionFormVersion.objects.get_version_list()
        context = {
            'form_version': chosen_version,
            'form_fields': chosen_version_fields,
            'all_versions': all_versions
        }
        return render(request, 'md_form_structure_view.html', context)


class AdminModuleDescriptionFormModify(View):
    """
    View which handles the module description structure form
    """
    def __init__(self):
        self.template = 'module_description_form_control.html'
        self.field_formset_object = formset_factory(FieldEntityForm, extra=0)

    def get(self, request, **kwargs):
        newest_version_fields = FormFieldEntity.objects.get_most_recent_form()
        field_formset = self.field_formset_object(request.GET or None, initial=newest_version_fields)
        return render(request, self.template, {'field_formset': field_formset})

    def post(self, request, **kwargs):
        field_formset = self.field_formset_object(request.POST)
        
        if field_formset.is_valid():
            md_version = ModuleDescriptionFormVersion.objects.create_new_version()
            
            for form in field_formset:
                entity = form.save(commit=False)
                entity.module_description_version = md_version
                entity.save()

            return redirect('module_description_form_structure') # temp redirect

        print(field_formset.errors)
        return render(request, self.template, {
            'field_formset': field_formset,
            'formset_length': len(field_formset)
        })
        