from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import DepartmentViewSet, RegisterView, ProfileView, RequestViewForVacancy
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='departments')

urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('send_mail/', RequestViewForVacancy.as_view())
]
