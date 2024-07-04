from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, UserRegistrationAPIview, activate_account, UserLoginAPIview, UserLogoutAPIview


router = DefaultRouter()

router.register('list', PatientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIview.as_view(), name="register"),
    path('login/', UserLoginAPIview.as_view(), name="login"),
    path('logout/', UserLogoutAPIview.as_view(), name="logout"),
    path('active/<uuid64>/<token>/',
         activate_account, name="activate_account"),
]
