from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings_view, name='settings'),
]
