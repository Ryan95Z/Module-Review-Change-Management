from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.views import View
from core.models import Module
from forms.forms import ModuleDescriptionForm
from forms.models import ModuleDescription, ModuleDescriptionEntry, ModuleDescriptionFormVersion, FormFieldEntity
from forms.utils.module_description import md_to_form

class LeaderModuleDescriptionView(View):
    """
    This view handles viewing and editing for the most recent 
    module description of a single module.
    """
    
    def get(self, request, **kwargs):
        """
        The page can be in view mode and edit mode. When in view mode,
        the form is rendered, but disabled, in edit mode it is enabled.
        If the current description was created using an older form, this
        is reflected. When switching to edit mode, the newer form will show.
        """
        # Assign user chosen factors to variables.
        module = Module.objects.get(pk=self.kwargs.get('pk'))
        form_type = kwargs.get('form_type', 'view')
        form_exists = True
        edit_form = True if form_type == 'new' else False
        
        # Retrieve the most recent description for this module, and
        # the form version it used. Convert it to form format.
        try:
            current_description = ModuleDescriptionEntry.objects.get_last_description(module)
            version_used = ModuleDescription.objects.get_most_recent(module).form_version
            existing_form = md_to_form(current_description)
        except ObjectDoesNotExist:
            form_exists = False

        # We need to check if the existing data was created using the
        # most recent form. If not, we set a flag and only render the
        # most recent form if the user is in edit mode.
        if form_exists and version_used == ModuleDescriptionFormVersion.objects.get_most_recent():
            new_form_version = False
            module_description_form = ModuleDescriptionForm(initial=existing_form)
        else:
            if not form_exists or edit_form:
                new_form_version = False
                module_description_form = ModuleDescriptionForm()
            else: 
                new_form_version = True
                module_description_form = ModuleDescriptionForm(md_version=version_used.pk, initial=existing_form)

        # Set the context with the form, and the user chosen stuff
        context = {
            'edit_form': edit_form,
            'form_exists': form_exists,
            'module': module,
            'form': module_description_form,
            'new_form_version': new_form_version
        }
        return render(request, 'module_description_view.html', context)
    
    def post(self, request, **kwargs):
        """
        When the form is posted, this function creates a new instance
        of the description for this module. Currently, it will create
        an entirely new version every time the form is submitted, 
        however I plan to change this later.
        """
        module = Module.objects.get(pk=self.kwargs.get('pk'))

        # In the future, the user may be able to update the description
        # using an older version of the form, therefore we get the form
        # version from the form so that we know what we are working with
        form_version_id = request.POST['form_version']
        form_version = ModuleDescriptionFormVersion.objects.get(pk=form_version_id)
        module_description_form = ModuleDescriptionForm(request.POST, md_version=form_version_id)

        # If the form data is valid, we create a new ModuleDescription
        # 'parent' object, and then create ModuleDescriptionEntry objects
        # for each of the fields in the form, associating them with the parent
        if module_description_form.is_valid():

            # Remove the form version from the cleaned data, as we don't need it
            del module_description_form.cleaned_data['form_version']

            md = ModuleDescription.objects.create_new(module, form_version)            
            for field, value in module_description_form.cleaned_data.items():
                # We only want the field id, so we strip 'field_entity_'
                field_entity = FormFieldEntity.objects.get(pk=field.strip('field_entity_'))
                ModuleDescriptionEntry.objects.create_new_entry(md, field_entity, value)
            return redirect('view_module_description', pk=module.pk)

        # If the form isn't valid, we rerender the page with the errors
        else:
            context = {
                'edit_form': True,
                'form_exists': True,
                'module': module,
                'form': module_description_form,
                'new_form_version': False
            }
            return render(request, 'module_description_view.html', context)
