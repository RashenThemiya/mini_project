from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='crop_recommendation_index'),
    
]
