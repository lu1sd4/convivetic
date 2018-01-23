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
		default = 'R'
	)
	views = models.PositiveIntegerField(
		default = 0
	)	
	tags = models.ManyToManyField(ThreadTag)


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
		default="Experience content"
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
		default = 'R'
	)
	views = models.PositiveIntegerField(
		default = 0
	)
	likes = models.PositiveIntegerField(
		default = 0
	)
	tags = models.ManyToManyField(ExperienceTag)


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


