from os import name
from django.urls import path
from .views import index_view, ajax_prediction

urlpatterns = [
    path('', index_view, name = "home"),
    path('ajax_prediction', ajax_prediction, name = "ajax_prediction")
]