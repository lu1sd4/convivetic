from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.template import loader

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView

from django.views.generic.detail import SingleObjectMixin

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

# Youtube Token Retrieval

from .tokens import youtube_token

from django.db import transaction
from .forms import LoginForm
from .forms import UserForm
from .forms import ProfileForm
from .forms import ThreadForm

from .models import *

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

class Index(ListView):
	template_name = 'app/index.html'
	context_object_name = 'thread_list'
	queryset = Thread.objects.order_by('pub_date')[:4]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['secondary_threads'] = Thread.objects.order_by('pub_date')[4:8] 
		context['experiences'] = Experience.objects.order_by('pub_date')[:9]
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

class Forums(FormView):
	template_name = 'app/forums.html'
	model = Thread
	form_class = ThreadForm
	success_url = '/forums'

	def get_context_data(request, **kwargs):
		context = super().get_context_data(**kwargs)
		context['thread_list'] = Thread.objects.all()
		return context

	def post(self, request, *args, **kwargs):		
		form = self.get_form()
		if form.is_valid():
			thread = form.save(commit=False)
			thread.author = request.user
			thread.save()
			return redirect('thread-detail', pk=thread.id)
		else:
			return self.form_invalid(form)

class ForumDetail(DetailView):
	model = Thread
	template_name = 'app/thread_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		thread_pk = self.kwargs['pk']
		author_id = self.request.user.id

		likes_c = Like.objects.filter(thread = thread_pk, author = author_id).count()
		dislike_c = Dislike.objects.filter(thread = thread_pk, author = author_id).count()

		if(likes_c == 0 and dislike_c == 0):
			context['user_can_vote'] = True 
		else:
			context['user_can_vote'] = False

		return context

class ForumLike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):
		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk=forum_id)
		author = request.user
		like = Like(thread = forum, author = author)
		like.save()
		likes_c = Like.objects.filter(thread = forum_id, author = author.id).count()
		dislike_c = Dislike.objects.filter(thread = forum_id, author = author.id).count()

		return HttpResponse(likes_c - dislike_c)

class ForumDislike(View):
	def get(self, request, *args, **kwargs):
		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk=forum_id)
		author = request.user
		dislike = Dislike(thread = forum, author = author)
		dislike.save()
		likes_c = Like.objects.filter(thread = forum_id, author = author.id).count()
		dislikes_c = Dislike.objects.filter(thread = forum_id, author = author.id).count()
		return HttpResponse(likes_c - dislikes_c)

class ForumView(View):
	def get(self, request, *args, **kwargs):
		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk = forum_id)
		forum.views = forum.views + 1
		forum.save()
		return HttpResponse(forum.views)

class ForumComment(View):
	
	def get(self,request, *args, **kwargs):
		forum_id = self.kwargs['pk']
		comment_content = self.kwargs['content']
		forum = get_object_or_404(Thread, pk = forum_id)
		author = request.user
		#comment = Comment(thread=forum, author=author, content=comment_content, )
		return HttpResponse()

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
		user_form = UserForm(prefix="user", initial={'group' : 1})
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

@csrf_exempt
def youtube_token_v(request):
	data = { 
		'token' : youtube_token.get_youtube_token(),
		'apiKey' : settings.API_KEY
	}
	return(JsonResponse(data))

class YoutubeUploadTest(TemplateView):
	template_name = 'app/test_youtube.html'

class DriveUploadTest(TemplateView):
	template_name = 'app/test_drive.html'

class ProfileView(TemplateView):
	template_name = 'app/profile.html'

class ExperiencesView(ListView):
	template_name = 'app/experiences.html'
	context_object_name = 'experiences'
	queryset = Experience.objects.order_by('pub_date')
	paginate_by = 8

class ExperienceDetailView(DetailView):
	model = Experience
	template_name = 'app/experience_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		experience_pk = self.kwargs['pk']
		user = self.request.user.id

class MyForumsView(ListView):
	template_name = 'app/my_forums.html'
	context_object_name = 'user_threads'
	paginate_by = 8

	def get_queryset(self):
		user_id = self.request.user.id
		return Thread.objects.filter(author = user_id)

class MyExperiencesView(TemplateView):
	template_name = 'app/my_experiences.html'

class MyCommentsView(TemplateView):
	template_name = 'app/my_comments.html'