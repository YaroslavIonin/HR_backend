from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import proverca

urlpatterns = [
    path('', proverca)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)