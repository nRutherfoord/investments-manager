from rest_framework.routers import DefaultRouter

from investments.views import InvestmentPlatformViewSet, InvestmentViewSet, TradeViewSet

router = DefaultRouter()
router.register(r'', InvestmentViewSet, basename='investment')
router.register(r'platform', InvestmentPlatformViewSet, basename='investment-platform')
router.register(r'trades', TradeViewSet, basename='trades')

urlpatterns = router.urls