from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import DepartmentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('departments', DepartmentViewSet, basename='departments')

urlpatterns = router.urls
