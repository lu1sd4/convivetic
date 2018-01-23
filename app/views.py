from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.template import loader

from django.urls import reverse

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView

from django.views.generic.detail import SingleObjectMixin

from django.views.generic.edit import CreateView
from django.views.generic.edit import FormMixin

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.models import User
from django.contrib import messages

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
from .forms import *

from .models import *

from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
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

class ForumsOrdered(ListView):
	template_name = 'app/forums.html'
	paginate_by = 8

	def get_queryset(self):
		criterium = self.kwargs['order']
		if(criterium == 'popular' or criterium == 'new'):
			return self.get_query_criterium(criterium)
		else:
			return Experience.objects.none()


	def get_query_criterium(self, criterium):

		
		return {
			'popular': Thread.objects.order_by('-title'),
			'new': Thread.objects.order_by('-pub_date'),
		}[criterium]


class ForumDetail(DetailView):
	model = Thread
	template_name = 'app/thread_detail.html'
	form_class = ThreadCommentForm

	def get_success_url(self):
		return reverse('thread-detail', kwargs={'pk':self.object.id})

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

		context['thread_pk'] = thread_pk
		context['form'] = ThreadCommentForm(instance=Comment(
				thread=self.object
			)
		)

		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			messages.success(request, 'Comentario publicado con éxito')
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.author = self.request.user
		comment.save()
		return super(ForumDetail, self).form_valid(form)



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

@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'app/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

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

class CreateExperience(CreateView):
	template_name = 'app/create_experience.html'
	model = Experience
	fields = ['title', 'content', 'video_url', 'audio_url', 'img']

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

		#likes_c = ExperiencesLike.objects.count()
		#dislike_c = Dislikes.objects.count()

		# if(likes_c == 0 and dislike_c == 0):
		# 	context['user_can_vote'] = True 
		# else:
		# 	context['user_can_vote'] = True

		context['experience_pk'] = experience_pk
		context['user_can_vote'] = True
		return context

class ExperiencesOrdered(ListView):
	template_name = 'app/experiences.html'
	context_object_name = 'experiences'
	paginate_by = 8

	def get_queryset(self):
		criterium = self.kwargs['order']
		if(criterium == 'popular' or criterium == 'new'):
			return self.get_query_criterium(criterium)
		else:
			return Experience.objects.none()

	def get_query_criterium(self, criterium):
		return {
			'popular': Experience.objects.order_by('-title'),
			'new': Experience.objects.order_by('-pub_date'),
		}[criterium]

class ExperienceView(View):
	def get(self, request, *args, **kwargs):
		experience_id = self.kwargs['pk']
		experience = get_object_or_404(Experience, pk = experience_id)
		experience.views = experience.views + 1
		experience.save()
		return HttpResponse(experience.views)

class ExperiencesLike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):
		experience_id = self.kwargs['pk']
		experience = get_object_or_404(Experience, pk=experience_id)
		author = request.user
		like = ExperiencesLike(experience = experience, author = author)
		like.save()
		likes_c = ExperiencesLike.objects.filter(experience = experience_id, author = author.id).count()
		dislike_c = ExperiencesDislike.objects.filter(experience = experience_id, author = author.id).count()

		return HttpResponse(likes_c - dislike_c)

class ExperiencesDislike(View):
	def get(self, request, *args, **kwargs):
		experience_id = self.kwargs['pk']
		experience = get_object_or_404(Experience, pk=experience_id)
		author = request.user
		dislike = ExperienceDislike(experience = Experience, author = author)
		dislike.save()
		likes_c = ExperiencesLike.objects.filter(experience = experience_id, author = author.id).count()
		dislikes_c = ExperiencesDislike.objects.filter(experience = experience_id, author = author.id).count()
		return HttpResponse(likes_c - dislikes_c)


class MyForumsView(ListView):
	template_name = 'app/my_forums.html'
	context_object_name = 'user_threads'
	paginate_by = 8

	def get_queryset(self):
		user_id = self.request.user.id
		return Thread.objects.filter(author = user_id)

class MyExperiencesView(ListView):
	template_name = 'app/my_experiences.html'
	context_object_name = 'user_experiences'
	paginate_by = 4

	def get_queryset(self):
		user_id = self.request.user.id
		return Experience.objects.filter(author = user_id)

class MyCommentsView(ListView):
	template_name = 'app/my_comments.html'
	paginate_by = 8
	context_object_name = 'my_comments'

	def get_queryset(self):
		user_id = self.request.user.id
		return Comment.objects.filter(author = user_id)

	
