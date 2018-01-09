from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.db import transaction

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

class Forums(TemplateView):
	template_name = 'app/forums.html'

@transaction.atomic
def register_user(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, prefix="user")
		profile_form = ProfileForm(request.POST, prefix="profile")
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)			
			user.save()			
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			return redirect('/')
	else:
		user_form = UserForm(prefix="user")
		profile_form = ProfileForm(prefix="profile")
	context = {
		"user_form": user_form,
		"profile_form": profile_form
	}
	return render(request, 'app/signup.html', context)