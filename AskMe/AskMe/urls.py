from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questoins, name = 'new_questoins'),
    path('ask/', views.create_ask, name = 'create_ask'),
    path('question/<int:pk>/', views.question, name = 'question'),
    path('hot/', views.hot_questions, name = 'hot_questions'),
    path('tag/python/', views.questions_by_tag, name = 'questions_by_tag'),
    path('settings/', views.settings, name = 'settings'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.signup, name = 'signup'),
]
