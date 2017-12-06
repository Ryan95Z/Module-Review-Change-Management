from django.shortcuts import redirect
from django.http import HttpResponseRedirect


class AdminTestMixin(object):
    """
    Mixin class that is used to determine
    where to route the user if they are an admin.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Method to determine where to route the user
        """
        try:
            if not request.user.is_admin:
                return redirect('dashboard')
        except AttributeError:
            return redirect('login')
        return super(AdminTestMixin, self).dispatch(request, *args, **kwargs)


class LoggedInTestMixin(object):
    """
    Mixin class that is used to determine
    where to route the user if they are
    already logged in.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Method to determine where to route the user
        """
        try:
            if request.user.is_authenticated():
                return redirect('dashboard')
        except AttributeError:
            return redirect('login')
        return super(
            LoggedInTestMixin, self).dispatch(request, *args, **kwargs)
