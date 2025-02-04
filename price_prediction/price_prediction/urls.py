from django.urls import path
from .views import predict_price_view

urlpatterns = [
    path('predict/', predict_price_view, name='predict_price'),
]
