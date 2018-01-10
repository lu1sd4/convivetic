from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.template import loader

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView


from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.models import User

# Email verification

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.db import transaction
from .forms import LoginForm
from .forms import UserForm
from .forms import ProfileForm

from .models import *


class Index(ListView):
	template_name = 'app/index.html'
	context_object_name = 'thread_list'
	queryset = Thread.objects.order_by('pub_date')[:4]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['secondary_threads'] = Thread.objects.order_by('pub_date')[4:8] 
		context['experiences'] = Experience.objects.all()
		context['th_quantity'] = Thread.objects.all().count()
		return context


class Login(LoginView):
	template_name = 'app/login.html'
	authentication_form = LoginForm
	redirect_authenticated_user = True

class UsernameCheck(View):
	def get(self, request, *args, **kwargs):
		username = self.kwargs['user_id']
		if username_present(username):
			return HttpResponse()
		return HttpResponseBadRequest()

def username_present(username):
	if User.objects.filter(username=username).exists():
		return True
	return False

class Forums(ListView):
	template_name = 'app/forums.html'
	context_object_name = 'thread_list'
	queryset = Thread.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		return context


class ForumDetail(DetailView):
	model = Thread
	template_name = 'app/thread_detail.html'


@transaction.atomic
def register_user(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, prefix="user")
		profile_form = ProfileForm(request.POST, prefix="profile")
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)			
			user.is_active = False
			user.save()			
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			current_site = get_current_site(request)
			mail_subject = 'Activa tu cuenta de ConviveTIC'
			message = render_to_string('app/acc_activation_email.html', {
				'user' : user,
				'domain' : current_site.domain,
				'uid' : force_text(urlsafe_base64_encode(force_bytes(user.pk))),
				'token': account_activation_token.make_token(user)
			})
			to_email = user_form.cleaned_data.get('email')
			email = EmailMessage(
				mail_subject, message, to=[to_email]
			)
			email.send()
			return redirect('/')
	else:
		user_form = UserForm(prefix="user")
		profile_form = ProfileForm(prefix="profile")
	context = {
		"user_form": user_form,
		"profile_form": profile_form
	}
	return render(request, 'app/signup.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return HttpResponse('Gracias por confirmar tu correo. Ahora puedes iniciar sesión.')
    else:
        return HttpResponse('Tu enlace de activación no es válido.')

class PasswordReset(PasswordResetView):
	template_name = 'app/password_reset_request.html'
	email_template_name = 'app/password_reset_email.html'
	subject_template_name = 'app/password_reset_subject.txt'

class PasswordResetDone(PasswordResetDoneView):
	template_name = 'app/password_reset_request_done.html'	

class PasswordResetConfirm(PasswordResetConfirmView):
	template_name = 'app/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
	template_name = 'app/password_reset_complete.html'

