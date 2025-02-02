from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home_index'),
    path('reel/', views.reel_index, name='reel_index'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]

# ✅ Append static URL patterns correctly
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
