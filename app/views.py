from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .forms import LoginForm

class Index(TemplateView):
	#context = {}
	#return render(request, 'app/index.html', context)
	template_name = 'app/index.html' 

class Login(LoginView):
	template_name = 'app/login.html'
	authentication_form = LoginForm
	redirect_authenticated_user = True