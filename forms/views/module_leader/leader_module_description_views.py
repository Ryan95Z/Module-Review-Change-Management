from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.views import View
from core.models import Module
from forms.forms import ModuleDetailForm, ModuleDescriptionForm
from forms.models import ModuleDescription, ModuleDescriptionEntry, ModuleDescriptionFormVersion, FormFieldEntity
from forms.utils.module_description import *

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

        edit_form = True if form_type == 'new' else False
        form_version_exists = True
        form_exists = True

        # Populate the ModuleDetails form
        details_form = ModuleDetailForm(instance=module)

        # Get the most recent form version. If one does not exist,
        # set a flag
        try:
            newest_form_version = ModuleDescriptionFormVersion.objects.get_most_recent()
        except ObjectDoesNotExist:
            form_version_exists = False
        
        # Retrieve the most recent description for this module, and
        # the form version it used. Convert it to form format.
        try:
            current_description = CurrentModuleDescriptionWrapper(module)
            version_used = current_description.form_master
        except ObjectDoesNotExist:
            form_exists = False

        # We need to check if the existing data was created using the
        # most recent form. If not, we set a flag and only render the
        # most recent form if the user is in edit mode.
        if form_version_exists and form_exists and version_used == newest_form_version:
            new_form_version = False
            module_description_form = current_description.get_form()
        else:
            if not form_version_exists:
                new_form_version = False
                module_description_form = None
            elif not form_exists or edit_form:
                new_form_version = False
                module_description_form = ModuleDescriptionForm()
            else: 
                new_form_version = True
                module_description_form = current_description.get_form()

        # Set the context with the form, and the user chosen stuff
        context = {
            'edit_form': edit_form,
            'form_version_exists': form_version_exists,
            'form_exists': form_exists,
            'module': module,
            'details_form': details_form,
            'form': module_description_form,
            'new_form_version': new_form_version
        }
        return render(request, 'module_description_view.html', context)
    
    def post(self, request, **kwargs):
        """
        When the form is posted, this function creates a new instance
        of the description for this module.
        """
        module = Module.objects.get(pk=self.kwargs.get('pk'))

        # Get the module details form 
        module_details_form = ModuleDetailForm(request.POST, instance=module)

        # In the future, the user may be able to update the description
        # using an older version of the form, therefore we get the form
        # version from the form so that we know what we are working with
        form_version_id = request.POST['form_version']
        form_version = ModuleDescriptionFormVersion.objects.get(pk=form_version_id)
        module_description_form = ModuleDescriptionForm(request.POST, md_version=form_version_id)

        # If the form data is valid, we create a new ModuleDescription
        # 'parent' object, and then create ModuleDescriptionEntry objects
        # for each of the fields in the form, associating them with the parent.
        # We also update the module details
        if module_description_form.is_valid() and module_details_form.is_valid():

            # Save any changes to the details
            module_details_form.save()

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
                'details_form': module_details_form,
                'form': module_description_form,
                'new_form_version': False
            }
            return render(request, 'module_description_view.html', context)
