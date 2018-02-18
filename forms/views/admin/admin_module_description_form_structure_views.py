from django.views.generic.detail import DetailView

from core.models import Module

class AdminModuleDescriptionFormStructure(DetailView):
    """
    View a module description
    """
    
    model = Module
    template_name="module_description_view.html"