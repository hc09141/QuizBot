from django.contrib import admin
from .models import UserProfile, Message, QuizQuestion

class UserProfileAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

class QuizAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(QuizQuestion, QuizAdmin)
