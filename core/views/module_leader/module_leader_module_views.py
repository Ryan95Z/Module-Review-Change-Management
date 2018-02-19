from django.urls import reverse
from django.views.generic.list import ListView

from core.models import Module


class ModuleLeaderModuleList(ListView):
    """
    View for listing all modules for a module leader
    """
    model = Module
    paginate_by = 10

    def get_queryset(self):
        """
        Returns all modules that are assinged
        to the module leader.
        """
        object_list = self.model.objects.filter(
            module_leader=self.request.user
        )
        return object_list
