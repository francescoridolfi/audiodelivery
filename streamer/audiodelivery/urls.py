from django.urls import path, include

from rest_framework.routers import DefaultRouter

from audiodelivery.api.views import AudioViewSet


router = DefaultRouter()
router.register(r"audio", AudioViewSet, basename="audio")

urlpatterns = [
    path('', include(router.urls))
]