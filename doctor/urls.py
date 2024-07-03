from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('available_times', views.AvailableTimeViewSet)
router.register('designations', views.DesignationViewSet)
router.register('reviews', views.ReviewViewSet)
router.register('list', views.DoctorViewSet)
router.register('specializations', views.SpecializationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
