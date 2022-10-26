from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import VacancyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vacancies', VacancyViewSet, basename='vacancies')

urlpatterns = router.urls
