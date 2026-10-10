from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', InvestmentViewSet, basename='investment')\
urlpatterns = router.urls