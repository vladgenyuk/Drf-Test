from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import CarViewSet, RegisterView, home, BookViewSet, BookReaderViewSet

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('', home),
]

router = DefaultRouter()
router.register(r'CarApi', CarViewSet, basename='CarViewSet')
router.register(r'BookApi', BookViewSet, basename='BookViewSet')
router.register(r'BookReaderApi', BookReaderViewSet, basename='BookReaderViewSet')
urlpatterns += router.urls

