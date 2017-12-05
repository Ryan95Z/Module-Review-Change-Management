from django.shortcuts import redirect
from django.http import HttpResponseRedirect

class AdminTestMixin(object):

	def dispatch(self, request, *args, **kwargs):
		try:
			if not request.user.is_admin:
				return redirect('dashboard')
		except AttributeError:
			return redirect('login')
		return super(AdminTestMixin, self).dispatch(request, *args, **kwargs)

class LoggedInTestMixin(object):

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_authenticated():
				return redirect('dashboard')
		except AttributeError:
			return redirect('login')
		return super(LoggedInTestMixin, self).dispatch(request, *args, **kwargs)
