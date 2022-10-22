from django.urls import path, include
from .views import proverca

urlpatterns = [
    path('', proverca)
]