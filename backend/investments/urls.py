from rest_framework.routers import DefaultRouter

from investments.views import InvestmentPlatformViewSet, InvestmentViewSet

router = DefaultRouter()
router.register(r'', InvestmentViewSet, basename='investment')
router.register(r'platform', InvestmentPlatformViewSet, basename='investment-platform')

urlpatterns = router.urls