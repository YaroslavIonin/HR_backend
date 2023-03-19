from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import VacancyViewSet, ResumeViewSet, AddToFavoriteVacancies
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vacancies', VacancyViewSet, basename='vacancies')
router.register('resumes', ResumeViewSet, basename='resumes')

urlpatterns = [
    path('vacancies/to_favorite/', AddToFavoriteVacancies.as_view())
]

urlpatterns += router.urls