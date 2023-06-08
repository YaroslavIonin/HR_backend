from django.urls import path, include
from .views import DepartmentViewSet, RegisterView, ProfileView, RequestView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='departments')
router.register('requests', RequestView, basename='requests')


urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
]
