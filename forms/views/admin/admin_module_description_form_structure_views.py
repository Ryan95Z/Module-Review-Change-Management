from django.views import View
from django.shortcuts import render, redirect
from django.forms import modelformset_factory, formset_factory
from django.core.exceptions import ObjectDoesNotExist

from core.models import Module
from forms.models import ModuleDescriptionFormVersion, FormFieldEntity
from forms.forms import FieldEntityForm

class AdminModuleDescriptionFormStructure(View):
    """
    The view renders the most recent ModuleDescriptionFormVersion
    """
    def get(self, request, **kwargs):
        try:
            newest_version = ModuleDescriptionFormVersion.objects.get_most_recent()
            newest_version_fields = FormFieldEntity.objects.get_most_recent_form()
            all_versions = ModuleDescriptionFormVersion.objects.get_version_list()
            context = {
                'form_exists': True,
                'form_version': newest_version,
                'form_fields': newest_version_fields,
                'all_versions': all_versions
            }
        except ObjectDoesNotExist:
            context = {'form_exists': False}
        return render(request, 'md_form_structure_view.html', context)

class AdminModuleDescriptionFormStructureOld(View):
    """
    Renders a ModuleDescriptionFormStructure which is chosen by the user.
    """
    def get(self, request, **kwargs):
        try:
            version_pk = self.kwargs['pk']
            chosen_version = ModuleDescriptionFormVersion.objects.get(pk=version_pk)
            chosen_version_fields = FormFieldEntity.objects.get_form(version_pk)
            all_versions = ModuleDescriptionFormVersion.objects.get_version_list()
            context = {
                'form_exists': True,
                'form_version': chosen_version,
                'form_fields': chosen_version_fields,
                'all_versions': all_versions
            }
        except ObjectDoesNotExist:
            context = {'form_exists': False}
        return render(request, 'md_form_structure_view.html', context)


class AdminModuleDescriptionFormModify(View):
    """
    View which handles the module description structure form
    """
    # Setting the template and generating a formset object on initialization
    def __init__(self):
        self.template = 'md_form_structure_edit.html'
        self.field_formset_object = formset_factory(FieldEntityForm, extra=1, max_num=1)

    # When the user GETs the page, the most recent form structure is retrieved,
    # and used to populate the form. In the event that there is no existing form
    # it is left empty.
    def get(self, request, **kwargs):
        try:
            newest_version_fields = FormFieldEntity.objects.get_most_recent_form()
            field_formset = self.field_formset_object(request.GET or None, initial=newest_version_fields, prefix='structure_form')
        except ObjectDoesNotExist :
            field_formset = self.field_formset_object(request.GET or None)

        return render(request, self.template, {'field_formset': field_formset})

    # When the form is POSTed a new ModuleDescription 'parent' object is created,
    # and then each of the fields is stored in a FormFieldEntity object, and 
    # linked to the 'parent' with a foreign key.
    def post(self, request, **kwargs):
        field_formset = self.field_formset_object(request.POST, prefix='structure_form')
        
        if field_formset.is_valid():
            md_version = ModuleDescriptionFormVersion.objects.create_new_version()
            
            for form in field_formset:
                entity = form.save(commit=False)
                entity.module_description_version = md_version
                entity.save()

            return redirect('module_description_form_structure') # temp redirect
        return render(request, self.template, {
            'field_formset': field_formset,
            'formset_length': len(field_formset)
        })
        