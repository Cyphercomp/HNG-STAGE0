from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenderizeViewSet

router = DefaultRouter()
router.register(r'', GenderizeViewSet, basename='classify')

urlpatterns = [
    path('api', include(router.urls)),
    ]