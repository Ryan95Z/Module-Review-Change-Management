from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """
    Generic view to display dashboard
    """
    template_name = 'core/dashboard.html'
