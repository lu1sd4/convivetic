from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

PERSON_TITLE_CHOICES = [
	('Don', 'Don'),
	('Doña', 'Doña'),
	('Señor', 'Señor'),
	('Señora', 'Señora'),
	('Señorita', 'Señorita')
]

GENDER_CHOICES = [
	('M', 'Masculino'),
	('F', 'Femenino')
]

YES_NO_CHOICES = [
	(True, 'Si'),
	(False, 'No')
]

STATUS_CHOICES = [
	('P', 'Pendiente'),
	('A', 'Aprobado'),
	('R', 'Rechazado')
]

TEMPLATE_CHOICES = [
	('TEMP_INTRO', 'TEMP_INTRO'),
	('TEMP_TEST', 'TEMP_TEST'),
	('TEMP_TEST_IMAGE', 'TEMP_TEST_IMAGE'),
	('TEMP_TEXT', 'TEMP_TEXT'),
	('TEMP_ACTIVITY', 'TEMP_ACTIVITY'),
	('TEMP_TEST_MULTIPLE', 'TEMP_TEST_MULTIPLE'),
	('TEMP_CROSSWORD', 'TEMP_CROSSWORD'),
	('TEMP_FILL_THE_BLANKS', 'TEMP_FILL_THE_BLANKS')	
]

class UserProfile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE
	)
	title = models.CharField(
		choices = PERSON_TITLE_CHOICES,
		max_length = 50,
		blank=False,
		default='Don'
	)
	birth_date = models.DateField(
		null = True,
		blank = True
	)
	gender = models.CharField(
		choices = GENDER_CHOICES,
		max_length = 50,
		blank=False,
		default='M'
	)
	nationality = models.CharField(
		max_length = 50
	)
	country_of_residence = models.CharField(
		max_length = 50
	)
	phone_number = models.CharField(
		max_length = 15,
		blank = True,
		null=True
	)
	bio = models.TextField(
		default="",
		blank=True,
		null=True
	)
	is_conflict_participant = models.BooleanField(
		default=False,
		choices=YES_NO_CHOICES
	)
	is_conflict_victim = models.BooleanField(
		default=False,
		choices=YES_NO_CHOICES
	)
	is_living_in_conflict_zone = models.BooleanField(
		default=False,
		choices=YES_NO_CHOICES
	)

class ThreadTag(models.Model):
	name = models.CharField(max_length=20)

class Thread(models.Model):
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)
	title = models.CharField(
		max_length=100,
		blank=False,
		null=False
	)
	description = models.TextField(
		default='',
		blank=False,
		null=False
	)
	pub_date = models.DateField(
		default=date.today
	)
	video_url = models.CharField(
		max_length=50,
		null=True,
		blank=True
	)
	audio_url = models.CharField(
		max_length=100,
		null=True,
		blank=True
	)
	img = models.ImageField(
		upload_to="uploads/",
		null=True,
		blank=True
	)
	status = models.CharField(
		max_length = 20,
		choices = STATUS_CHOICES,
		default = 'P'
	)
	views = models.PositiveIntegerField(
		default = 0
	)	
	tags = models.ManyToManyField(ThreadTag, blank=True)


class Like(models.Model):
	thread = models.ForeignKey(
		Thread,
		on_delete=models.CASCADE
	)
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)

class Dislike(models.Model):
	thread = models.ForeignKey(
		Thread,
		on_delete=models.CASCADE
	)
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)


class Comment(models.Model):
	thread = models.ForeignKey(
		Thread,
		on_delete=models.CASCADE
	)
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)
	content = models.TextField(
		default='',
		blank=False,
		null=False
	)
	pub_date = models.DateField(
		default=date.today
	)
	video_url = models.CharField(
		max_length=50,
		null=True,
		blank=True
	)
	audio_url = models.CharField(
		max_length=100,
		null=True,
		blank=True
	)
	img = models.ImageField(
		upload_to="uploads/",
		null=True,
		blank=True
	)

class ExperienceTag(models.Model):
	name = models.CharField(max_length=20)


class Experience(models.Model):	
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)
	title = models.CharField(
		max_length = 100,
		default = ''
	)
	content = models.TextField(
		default="",
		blank=False,
		null=False
	)
	pub_date = models.DateField(
		default=date.today
	)
	video_url = models.CharField(
		max_length=50,
		null=True,
		blank=True
	)
	audio_url = models.CharField(
		max_length=100,
		null=True,
		blank=True
	)
	img = models.ImageField(
		upload_to="uploads/",
		null=True,
		blank=True
	)
	status = models.CharField(
		max_length = 20,
		choices = STATUS_CHOICES,
		default = 'P'
	)
	views = models.PositiveIntegerField(
		default = 0
	)
	likes = models.PositiveIntegerField(
		default = 0
	)
	tags = models.ManyToManyField(ExperienceTag, blank=True)


class ExperiencesLike(models.Model):
	experience = models.ForeignKey(
		Experience,
		on_delete=models.CASCADE
	)
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)

class ExperiencesDislike(models.Model):
	experience = models.ForeignKey(
		Experience,
		on_delete=models.CASCADE
	)
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)

class Toolbox(models.Model):
	name = models.CharField(
		max_length = 100,
		default = ''
	)
	description = models.CharField(
		max_length = 1000,
		default = ''
	)
	guide_n = models.PositiveIntegerField(
		default = 0
	)

class ToolboxUser(models.Model):
	toolbox = models.ForeignKey(
		Toolbox,
		on_delete = models.CASCADE
	)
	user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)
	comment = models.CharField(
		max_length = 500,
		blank=True,
		default=''
	)

class Question(models.Model):
	q_type = models.CharField(
		max_length = 20,
		choices = TEMPLATE_CHOICES,
		default = 'TEMP_TEST'
	)
	content = models.CharField(
		max_length = 1500,
		default = ''
	)
	content_templ = models.CharField(
		max_length = 1500,
		default = '',
		null=True,
		blank=True
	)
	img = models.CharField(
		max_length = 100,
		default = '',
		null = True,
		blank = True
	)
	title = models.CharField(
		max_length = 100,
		default = '',
		null = True,
		blank = True
	)
	is_html_content = models.BooleanField(
		default = False,
		choices = YES_NO_CHOICES
	)
	correct_answer = models.PositiveIntegerField(
		default = 0,
		null = True,
		blank = True
	)
	required = models.BooleanField(
		default=False,
		choices=YES_NO_CHOICES
	)
	answers_av = models.CharField(
		max_length = 100,
		default = '' ,
		null=True,
		blank=True
	)
	order = models.PositiveIntegerField(
		default = 0
	)
	toolbox = models.ForeignKey(
		Toolbox,
		on_delete=models.CASCADE,
		default=1
	)
	fill_answer = models.CharField(
		max_length = 700,
		default = '',
		null = True,
		blank = True
	)


class Answer(models.Model):
	question = models.ForeignKey(
		Question,
		on_delete=models.CASCADE,
		default=None
	)
	user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)
	answer = models.CharField(
		max_length = 600,
		default = '',
	)
	

class Guide(models.Model):
	pass



