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
         path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
   path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
       path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
           path('add_address/', views.add_address, name='add_address'),
            path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),

]  