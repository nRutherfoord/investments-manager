from rest_framework.routers import DefaultRouter

from investments.views import InvestmentPlatformAccountViewSet, InvestmentPlatformViewSet, InvestmentViewSet, TradeViewSet

router = DefaultRouter()
router.register(r'platform', InvestmentPlatformViewSet, basename='investment-platform')
router.register(r'trades', TradeViewSet, basename='trades')
router.register(r'accounts', InvestmentPlatformAccountViewSet, basename='accounts')
router.register(r'', InvestmentViewSet, basename='investment')
urlpatterns = router.urls