from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='market_place_index'),
        path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    path('add-item/', views.add_item, name='add_item'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('place-order/', views.place_order, name='place_order'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
      path('add-item/', views.add_item, name='add_item'),
     
]
