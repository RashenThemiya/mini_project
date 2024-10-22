from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='ai_chat_support_index'),
]
