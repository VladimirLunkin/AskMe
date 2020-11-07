from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list_ask/', views.list_ask),
    path('add_ask/', views.add_ask),
    path('ask/', views.ask),
    path('list_ask_tag/', views.list_ask_tag),
    path('settings/', views.settings),
    path('log_in/', views.log_in),
    path('register/', views.register),
]
