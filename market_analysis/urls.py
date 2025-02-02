from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_price_view, name='market_analysis_index'),
    path('predict/', views.predict_price_view, name='predict_price'),
  

]
