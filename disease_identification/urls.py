# disease_identification/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='disease_identification_index'),
    # Add other paths here
]
