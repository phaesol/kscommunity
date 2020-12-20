from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CommunityUser

admin.site.register(CommunityUser)
