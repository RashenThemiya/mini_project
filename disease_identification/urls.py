# disease_identification/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('disease-identification/', views.disease_identification, name='disease_identification_index'),
]


