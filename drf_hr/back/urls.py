from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import VacancyViewSet, ResumeViewSet, FavoriteVacancies, ListSkills
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vacancies', VacancyViewSet, basename='vacancies')
router.register('resumes', ResumeViewSet, basename='resumes')

urlpatterns = [
    path('vacancies/to_favorite/', FavoriteVacancies.as_view()),
    path('skills/', ListSkills.as_view())
]

urlpatterns += router.urls