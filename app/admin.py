from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from app.models import *

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
admin.site.register(Experience)
admin.site.register(ThreadTag)
admin.site.register(ExperienceTag)
admin.site.register(UserProfile)
admin.site.register(ExperiencesLike)
admin.site.register(ExperiencesDislike)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Toolbox)
admin.site.register(ToolboxUser)
admin.site.register(Question)
admin.site.register(Answer)