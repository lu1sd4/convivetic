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
		max_length = 50
	)
	birth_date = models.DateField()
	gender = models.CharField(
		choices = GENDER_CHOICES,
		max_length = 50
	)
	nationality = models.CharField(
		max_length = 50
	)
	country_of_residence = models.CharField(
		max_length = 50
	)
	phone_number = models.CharField(
		max_length = 15,
		blank = True
	)
	bio = models.TextField(
		default="User bio",
		blank=True
	)
	is_conflict_participant = models.BooleanField(
		default=False
	)
	is_conflict_victim = models.BooleanField(
		default=False
	)
	is_living_in_conflict_zone = models.BooleanField(
		default=False
	)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ThreadTag(models.Model):
	name = models.CharField(max_length=20)

class Thread(models.Model):
	author = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True
	)
	title = models.CharField(max_length=100)
	description = models.TextField(
		default="Thread description"
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
	tags = models.ManyToManyField(ThreadTag)

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
		default="Comment content"
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