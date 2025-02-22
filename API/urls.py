from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from . import views

router = DefaultRouter()
router.register('subjects', views.SubjectViewSet, basename="Subject")
router.register('users', views.UserViewSet, basename="User")
router.register('groups', views.GroupViewSet, basename="Group")
router.register('pupils', views.PupilViewSet, "Pupil")
router.register('payments', views.PaymentViewSet, basename="Payment")

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
