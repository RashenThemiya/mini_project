from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='ai_chat_support_index'),
]
