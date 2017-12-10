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


class UserOnlyMixin(object):
    """
    Mixing to prevent users accesing content that is
    for a certain users. For example, this wil be used
    to prvent al users accessing each other's change username
    or password pages.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Method to determine the route
        """
        try:
            user = request.user
            # check that they are logged in
            if user.is_authenticated():
                try:
                    # see if the slug has been set
                    slug = kwargs['slug']
                    if slug != user.username:
                        # slugs don't match then redirect
                        return redirect('dashboard')
                except KeyError:
                    return redirect('dashboard')
            else:
                # not logged in so back to login
                return redirect('login')
        except AttributeError:
            return redirect('login')

        # continue with the request
        return super(UserOnlyMixin, self).dispatch(request, *args, **kwargs)
