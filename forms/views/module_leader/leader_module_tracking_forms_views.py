from django.views.generic.detail import DetailView

from core.models import Module

class LeaderModuleTrackingFormView(DetailView):
    """
    View a module tracking form
    """
    
    model = Module
    template_name="module_tracking_form_view.html"