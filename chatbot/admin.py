from django.contrib import admin
from .models import UserProfile, Message

class UserProfileAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Message, MessageAdmin)
