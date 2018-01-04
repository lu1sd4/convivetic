from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from app.models import Thread
from app.models import Comment
from app.models import UserProfile

# Register your models here.

class ProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
	inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Thread)
admin.site.register(Comment)