from django.views.generic.detail import DetailView
from core.models import User


class UserProfileDetailView(DetailView):
    """
    View to access a user profile
    """
    model = User
    template_name = 'core/user_profile.html'
