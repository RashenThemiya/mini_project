from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ai_chat_support_index'),
]
