from django.views.generic import TemplateView
from core.models import Module


class DashboardView(TemplateView):
    """
    Generic view to display dashboard
    """
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_modules'] = Module.objects.filter(module_leader=self.request.user)
        context['all_modules'] = Module.objects.all()
        return context

    
