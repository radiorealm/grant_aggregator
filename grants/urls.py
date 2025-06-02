from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('grant/<int:grant_id>/', views.detail, name='detail'),
]