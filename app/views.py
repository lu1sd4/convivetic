from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .forms import LoginForm
from .forms import UserForm
from .forms import ProfileForm

class Index(TemplateView):
	#context = {}
	#return render(request, 'app/index.html', context)
	template_name = 'app/index.html' 

class Login(LoginView):
	template_name = 'app/login.html'
	authentication_form = LoginForm
	redirect_authenticated_user = True

class Signup(FormView):
	template_name = 'app/signup.html'
	def get(self, request, *args, **kwargs):
		user_form = UserForm()
		user_form.prefix = 'user_form'
		profile_form = ProfileForm()
		profile_form.prefix = 'profile_form'
		return self.render_to_response(self.get_context_data(user_form = user_form, profile_form = profile_form)) 

	def post(self, request, *args, **kwargs):
		user_form = UserForm(self.request.POST, prefix='user_form')
		profile_form = SocialForm(self.request.POST, prefix='profile_form')
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()                       
			return HttpResponseRedirect('index')
		else:
			return self.form_invalid(user_form, profile_form , **kwargs)

	def form_invalid(self, user_form, profile_form, **kwargs):
		user_form.prefix = 'user_form'
		profile_form.prefix = 'profile_form'
		return self.render_to_response(self.get_context_data(user_form = user_form, profile_form = profile_form)) 
