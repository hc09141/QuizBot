from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz', views.create)
]

# router = routers.SimpleRouter()
# router.register(r'quiz', views.QuizViewSet, basename='quiz')
