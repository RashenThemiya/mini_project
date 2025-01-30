from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Home app
    path('crop_recommendation/', include('crop_recommendation.urls')),  # Crop Recommendation app
    path('market_analysis/', include('market_analysis.urls')),  # Market Analysis app
    path('disease_identification/', include('disease_identification.urls')),  # Disease Identification app
    path('ai_chat_support/', include('ai_chat_support.urls')),  # AI Chat Support app
    path('market_place/', include('market_place.urls')),# Market Place app
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
