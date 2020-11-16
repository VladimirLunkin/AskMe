from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions, name='new_questions'),
    path('ask/', views.create_ask, name='create_ask'),
    path('question/<int:pk>/', views.question_page, name='question'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('tag/<str:tag>/', views.questions_by_tag, name='questions_by_tag'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
