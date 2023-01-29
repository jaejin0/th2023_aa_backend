from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/<str:date>/<int:flightNumber>', views.members, name='members')
]