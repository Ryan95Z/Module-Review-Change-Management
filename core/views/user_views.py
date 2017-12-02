from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)

from core.forms import LoginForm

class LoginView(View):
	def get(self, request):
		context = {'form' :  LoginForm() }
		return render(request, 'core/login.html', context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth = authenticate(username=username, password=password)
			if auth is not None:
				login(request, auth)
				request.session['username'] = username
				return redirect('dashboard')
			else:
				return redirect('login')
		return redirect('login')


class LogoutView(View):
	def get(self, request):
		try:
			del request.session['username']
		except KeyError:
			pass
		logout(request)
		return redirect('login')