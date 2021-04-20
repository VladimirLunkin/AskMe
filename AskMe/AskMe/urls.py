from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions, name='new_questions'),
    path('ask/', views.create_ask, name='create_ask'),
    path('question/<int:pk>/', views.question_page, name='question'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('tag/<str:tag>/', views.questions_by_tag, name='questions_by_tag'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('votes/', views.votes, name='votes'),
    path('correct/', views.is_correct, name='correct'),
    path('static_page/', views.static_page, name='static_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
