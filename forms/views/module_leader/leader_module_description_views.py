from django.shortcuts import render, redirect

from django.views import View
from core.models import Module
from forms.forms import ModuleDescriptionForm
from forms.models import ModuleDescription, ModuleDescriptionEntry, ModuleDescriptionFormVersion, FormFieldEntity

class LeaderModuleDescriptionView(View):
    """
    View a module description
    """
    
    def get(self, request, **kwargs):
        """
        GET method which provides the module description form
        """
        form_type = kwargs.get('form_type', 'view')
        form_exists = True
        edit_form = True if form_type == 'new' else False

        module_description_form = ModuleDescriptionForm(request.GET or None)

        module = Module.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'edit_form': edit_form,
            'form_exists': form_exists,
            'module': module,
            'form': module_description_form
        }
        return render(request, 'module_description_view.html', context)
    
    def post(self, request, **kwargs):
        module = Module.objects.get(pk=self.kwargs.get('pk'))

        form_version_id = request.POST['form_version']
        form_version = ModuleDescriptionFormVersion.objects.get(pk=form_version_id)
        module_description_form = ModuleDescriptionForm(request.POST, md_version=form_version_id)

        if module_description_form.is_valid():
            md = ModuleDescription.objects.create_new(module, form_version)
            del module_description_form.cleaned_data['form_version']
            for field, value in module_description_form.cleaned_data.items():
                field_entity = FormFieldEntity.objects.get(pk=field.strip('field_entity_'))
                ModuleDescriptionEntry.objects.create_new_entry(md, field_entity, value)
            return redirect('view_module_description', pk=module.pk)
        else:
            context = {
                'edit_form': True,
                'form_exists': True,
                'module': module,
                'form': module_description_form
            }
            return render(request, 'module_description_view.html', context)
