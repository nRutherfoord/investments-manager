from etoro_api.services import get_total_invested
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from investments.models import Investment, InvestmentPlatform
from investments.serializer import InvestmentPlatformSerializer, InvestmentsSerializer

# Create your views here.

class InvestmentViewSet (viewsets.ModelViewSet):
      queryset = Investment.objects.only("id", "stock_symbol", "value").all()
      serializer_class = InvestmentsSerializer


class InvestmentPlatformViewSet(viewsets.ViewSet):
      queryset = InvestmentPlatform.objects.only("id", "stock_symbol", "value").all()
      serializer_class = InvestmentPlatformSerializer
      
      @action(detail=False, methods=["get"])
      def getEtoroValue(self,request):
            return Response({get_total_invested()})