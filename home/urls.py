from os import name
from django.urls import path
from .views import index_view

urlpatterns = [
    path('', index_view, name = "home"),
]